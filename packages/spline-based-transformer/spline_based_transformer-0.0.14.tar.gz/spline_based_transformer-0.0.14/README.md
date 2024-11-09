<img src="./spline-based-transformer.png" width="400px"></img>

## Spline-Based Transformer

Implementation of the proposed <a href="https://www.youtube.com/watch?v=AzolLlIbKhg">Spline-Based Transformer</a> ([paper](https://la.disneyresearch.com/wp-content/uploads/SBT.pdf)) from Disney Research

This is basically a transformer based autoencoder, but they cleverly use a set of latent tokens, where that set of tokens are the (high dimensional) control points for a spline.

## Install

```bash
$ pip install spline-based-transformer
```

## Usage

```python
import torch
from spline_based_transformer import SplineBasedTransformer

model = SplineBasedTransformer(
    dim = 512,
    enc_depth = 6,
    dec_depth = 6
)

data = torch.randn(1, 1024, 512)

loss = model(data, return_loss = True)
loss.backward()

# after much training

recon, control_points = model(data, return_latents = True)
assert data.shape == recon.shape

# mess with the control points, which should preserve continuity better

control_points += 1

controlled_recon = model.decode_from_latents(control_points, num_times = 1024)
assert controlled_recon.shape == data.shape
```

For an example of an image autoencoder

```python
import torch

from spline_based_transformer import (
    SplineBasedTransformer,
    ImageAutoencoderWrapper
)

model = ImageAutoencoderWrapper(
    image_size = 256,
    patch_size = 32,
    spline_transformer = SplineBasedTransformer(
        dim = 512,
        enc_depth = 6,
        dec_depth = 6
    )
)

images = torch.randn(2, 3, 256, 256)

loss = model(images, return_loss = True)
loss.backward()

# after much training

recon_images, control_points = model(images, return_latents = True)
assert images.shape == recon_images.shape

# changing the control points

control_points += 1

controlled_recon_images = model.decode_from_latents(control_points)

assert controlled_recon_images.shape == images.shape
```

## Citations

```bibtex
@misc{Chandran2024,
    author  = {Prashanth Chandran, Agon Serifi, Markus Gross, Moritz Bächer},
    url     = {https://la.disneyresearch.com/publication/spline-based-transformers/}
}
```
