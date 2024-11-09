from __future__ import annotations
import math

import torch
from torch import nn, Tensor, tensor
import torch.nn.functional as F
from torch.nn import Module, ModuleList
from torch.utils._pytree import tree_flatten, tree_unflatten

from einops import rearrange, repeat, pack, unpack
from einops.layers.torch import Rearrange

from x_transformers import Encoder
from x_transformers.x_transformers import AlibiPositionalBias

# helpers

def exists(v):
    return v is not None

def default(v, d):
    return v if exists(v) else d

def divisible_by(num, den):
    return (num % den) == 0

def lens_to_mask(lens, max_length):
    assert (lens >= 2).all()

    seq = torch.arange(max_length, device = lens.device)
    return rearrange(lens, 'b -> b 1') > seq

def pack_with_inverse(t, pattern):
    t, packed_shape = pack(t, pattern)

    def inverse(t, inverse_pattern = None):
        inverse_pattern = default(inverse_pattern, pattern)
        return unpack(t, packed_shape, inverse_pattern)

    return t, inverse

# a simple mlp for encoding data and decoding

def MLP(dim, dim_out = None, expand_factor = 2):
    dim_out = default(dim_out, dim)
    dim_inner = dim_out * expand_factor

    return nn.Sequential(
        nn.Linear(dim, dim_inner),
        nn.GELU(),
        nn.Linear(dim_inner, dim_out)
    )

# uniform cubic b-spline

class BSpline(Module):
    def __init__(
        self,
        learned = False
    ):
        super().__init__()

        matrix = tensor([
            [-1,  3, -3,  1],
            [ 3, -6,  3,  0],
            [-3,  0,  3,  0],
            [ 1,  4,  1,  0]
        ]) / 6

        self.coeff = nn.Parameter(matrix, requires_grad = learned)

    def forward(
        self,
        control_points: Tensor,
        num_times: int,
        lens: Tensor | None = None
    ):
        batch, device = control_points.shape[0], control_points.device
        assert control_points.shape[1] == 4

        # uniform times from 0 - 1

        if exists(lens):
            times = torch.arange(num_times, device = device, dtype = torch.float)
            times = rearrange(times, 't -> 1 t') / rearrange(lens - 1, 'b -> b 1')
            times = times.clamp(max = 1.)
            times = rearrange(times, 'b t -> b t')
        else:
            times = torch.linspace(0, 1, num_times, device = device)
            times = repeat(times, 't -> b t', b = batch)

        # following https://en.wikipedia.org/wiki/B-spline
        # open an issue if you see some obvious error

        powers = torch.arange(4, device = device).flip(dims = (0,))

        times = rearrange(times, '... -> ... 1') ** powers

        return times @ self.coeff @ control_points

# class

class SplineBasedTransformer(Module):
    def __init__(
        self,
        dim,
        enc_depth,
        model_dim = None,
        dec_depth = None,
        dim_head = 64,
        heads = 8,
        dropout = 0.,
        num_control_points = 4,
        always_mlp_project = False,
        encoder_kwargs: dict | None = None,
        decoder_kwargs: dict | None = None,
    ):
        super().__init__()
        self.dim = dim

        encoder_kwargs = default(encoder_kwargs, {})
        decoder_kwargs = default(decoder_kwargs, {})

        model_dim = default(model_dim, dim)
        dec_depth = default(dec_depth, enc_depth)

        self.num_control_points = num_control_points
        self.control_point_latents = nn.Parameter(torch.zeros(num_control_points, model_dim))

        self.bspliner = BSpline()

        self.mlp_in = MLP(dim, model_dim) if always_mlp_project or dim != model_dim else nn.Identity()

        self.alibi = AlibiPositionalBias(heads) # todo - figure out if the paper accounted for asymmetric slopes given alibi weakness in non-causal setting

        self.encoder = Encoder(
            dim = model_dim,
            heads = heads,
            depth = enc_depth,
            attn_dim_head = dim_head,
            attn_dropout = dropout,
            ff_dropout = dropout,
            **encoder_kwargs
        )

        self.to_control_points = nn.Linear(model_dim, model_dim)

        self.decoder = Encoder(
            dim = model_dim,
            heads = heads,
            depth = dec_depth,
            attn_dim_head = dim_head,
            attn_dropout = dropout,
            ff_dropout = dropout,
            **decoder_kwargs
        )

        self.mlp_out = MLP(model_dim, dim) if always_mlp_project or dim != model_dim else nn.Identity()

    def decode_from_latents(
        self,
        control_points: Tensor,
        num_times: int,
        mask: Tensor | None = None,
        lens: Tensor | None = None,
        attn_bias = None
    ):
        assert num_times >= 2

        device = control_points.device

        splined_from_latent_controls = self.bspliner(control_points, num_times, lens = lens)

        if exists(lens) and not exists(mask):
            mask = lens_to_mask(lens, num_times)

        if not exists(attn_bias):
            attn_bias = self.alibi(num_times, num_times)

        decoded = self.decoder(splined_from_latent_controls, attn_bias = attn_bias, mask = mask)

        recon = self.mlp_out(decoded)
        return recon

    def forward(
        self,
        data: Tensor,
        lens: Tensor | None = None,
        return_loss = False,
        return_latents = False
    ):
        batch, num_points, device = *data.shape[:2], data.device

        x = self.mlp_in(data)

        # mask

        mask = None
        if exists(lens):
            mask = lens_to_mask(lens, num_points)

        # prepare control point latents across all batch samples

        latents = repeat(self.control_point_latents, 'l d -> b l d', b = batch)

        encoder_input, unpack_fn = pack_with_inverse([latents, x], 'b * d')

        # prepare alibi attention bias, but encoder is a bit different, as there should be no relative distance to the control latents

        attn_bias = self.alibi(num_points, num_points)
        encoder_attn_bias = F.pad(attn_bias, (self.num_control_points, 0, self.num_control_points, 0), value = 0.) # there is no relative distance between the latents and all the data points

        # adjust mask for control points

        mask_with_latents = mask

        if exists(mask_with_latents):
            mask_with_latents = F.pad(mask_with_latents, (self.num_control_points, 0), value = True)

        # encode

        encoded = self.encoder(encoder_input, attn_bias = encoder_attn_bias, mask = mask_with_latents)

        # splice out control latents

        latents, encoded = unpack_fn(encoded)

        control_points = self.to_control_points(latents)

        # reconstruct data from the bottleneck

        recon = self.decode_from_latents(control_points, num_times = num_points, attn_bias = attn_bias, mask = mask, lens = lens)

        if not return_loss:
            if not return_latents:
                return recon

            return recon, control_points

        recon_loss = F.mse_loss(recon, data)
        return recon_loss

# image autoencoder wrapper

class ImageAutoencoderWrapper(Module):
    def __init__(
        self,
        image_size,
        patch_size,
        spline_transformer: SplineBasedTransformer,
        channels = 3,
    ):
        super().__init__()
        assert divisible_by(image_size, patch_size)

        self.num_times = (image_size // patch_size) ** 2

        image_patch_dim = channels * patch_size ** 2

        dim = spline_transformer.dim

        self.patch_to_tokens = nn.Sequential(
            Rearrange('b c (h p1) (w p2) -> b h w (p1 p2 c)', p1 = patch_size, p2 = patch_size),
            nn.Linear(image_patch_dim, dim)
        )

        self.spline_transformer = spline_transformer

        self.tokens_to_patch = nn.Sequential(
            nn.Linear(dim, image_patch_dim),
            Rearrange('b h w (p1 p2 c) -> b c (h p1) (w p2)', p1 = patch_size, p2 = patch_size),
        )

    def decode_from_latents(
        self,
        control_points: Tensor,
    ):
        recon_tokens = self.spline_transformer.decode_from_latents(control_points, self.num_times)

        seq_len = recon_tokens.shape[-2]
        recon_tokens = rearrange(recon_tokens, 'b (h w) d -> b h w d', h = int(math.sqrt(seq_len)))

        recon_images = self.tokens_to_patch(recon_tokens)
        return recon_images

    def forward(
        self,
        images: Tensor,
        return_loss = False,
        return_latents = False
    ):

        tokens = self.patch_to_tokens(images)
        tokens, inverse_pack = pack_with_inverse([tokens], 'b * d')

        out = self.spline_transformer(tokens, return_loss = return_loss, return_latents = return_latents)

        if return_loss:
            return out

        (recon_tokens, *rest), tree_spec = tree_flatten(out)

        recon_tokens, = inverse_pack(recon_tokens)

        recon_images = self.tokens_to_patch(recon_tokens)

        output = tree_unflatten((recon_images, *rest), tree_spec)
        return output