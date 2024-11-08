<img src="./lvsm.png" width="500px"></img>

<img src="./lvsm-finding.png" width="400px"></img>

<img src="./plucker-ray.png" width="400px"></img>

## LVSM - Pytorch (wip)

Implementation of [LVSM](https://haian-jin.github.io/projects/LVSM/), SOTA Large View Synthesis with Minimal 3d Inductive Bias, from Adobe Research

We will focus only on the Decoder-only architecture in this repository.

This paper lines up with <a href="https://openreview.net/forum?id=A8Vuf2e8y6">another</a> from ICLR 2025

## Install

```bash
$ pip install lvsm-pytorch
```

## Usage

```python
import torch
from lvsm_pytorch import LVSM

rays = torch.randn(2, 4, 6, 256, 256)
images = torch.randn(2, 4, 3, 256, 256)

target_rays = torch.randn(2, 6, 256, 256)
target_images = torch.randn(2, 3, 256, 256)

model = LVSM(
    dim = 512,
    max_image_size = 256,
    patch_size = 32,
    depth = 2,
)

loss = model(
    input_images = images,
    input_rays = rays,
    target_rays = target_rays,
    target_images = target_images
)

loss.backward()

# after much training

pred_images = model(
    input_images = images,
    input_rays = rays,
    target_rays = target_rays,
) # (2, 3, 256, 256)

assert pred_images.shape == target_images.shape
```

Or from the raw camera intrinsic / extrinsics (please submit an issue or pull request if you see an error. new to view synthesis and out of my depths here)

```python
import torch
from lvsm_pytorch import LVSM, CameraWrapper

input_intrinsic_rotation = torch.randn(2, 4, 3, 3)
input_extrinsic_rotation = torch.randn(2, 4, 3, 3)
input_translation = torch.randn(2, 4, 3)
input_uniform_points = torch.randn(2, 4, 3, 256, 256)

target_intrinsic_rotation = torch.randn(2, 3, 3)
target_extrinsic_rotation = torch.randn(2, 3, 3)
target_translation = torch.randn(2, 3)
target_uniform_points = torch.randn(2, 3, 256, 256)

images = torch.randn(2, 4, 4, 256, 256)
target_images = torch.randn(2, 4, 256, 256)

lvsm = LVSM(
    dim = 512,
    max_image_size = 256,
    patch_size = 32,
    channels = 4,
    depth = 2,
)

model = CameraWrapper(lvsm)

loss = model(
    input_intrinsic_rotation = input_intrinsic_rotation,
    input_extrinsic_rotation = input_extrinsic_rotation,
    input_translation = input_translation,
    input_uniform_points = input_uniform_points,
    target_intrinsic_rotation = target_intrinsic_rotation,
    target_extrinsic_rotation = target_extrinsic_rotation,
    target_translation = target_translation,
    target_uniform_points = target_uniform_points,
    input_images = images,
    target_images = target_images,
)

loss.backward()

# after much training

pred_target_images = model(
    input_intrinsic_rotation = input_intrinsic_rotation,
    input_extrinsic_rotation = input_extrinsic_rotation,
    input_translation = input_translation,
    input_uniform_points = input_uniform_points,
    target_intrinsic_rotation = target_intrinsic_rotation,
    target_extrinsic_rotation = target_extrinsic_rotation,
    target_translation = target_translation,
    target_uniform_points = target_uniform_points,
    input_images = images,
)

```

## Citations

```bibtex
@inproceedings{Jin2024LVSMAL,
    title   = {LVSM: A Large View Synthesis Model with Minimal 3D Inductive Bias},
    author  = {Haian Jin and Hanwen Jiang and Hao Tan and Kai Zhang and Sai Bi and Tianyuan Zhang and Fujun Luan and Noah Snavely and Zexiang Xu},
    year    = {2024},
    url     = {https://api.semanticscholar.org/CorpusID:273507016}
}
```

```bibtex
@article{Zhang2024CamerasAR,
    title     = {Cameras as Rays: Pose Estimation via Ray Diffusion},
    author    = {Jason Y. Zhang and Amy Lin and Moneish Kumar and Tzu-Hsuan Yang and Deva Ramanan and Shubham Tulsiani},
    journal   = {ArXiv},
    year      = {2024},
    volume    = {abs/2402.14817},
    url       = {https://api.semanticscholar.org/CorpusID:267782978}
}
```
