Torch Yield
===========

[![Last release](https://img.shields.io/pypi/v/torchyield.svg)](https://pypi.python.org/pypi/torchyield)
[![Python version](https://img.shields.io/pypi/pyversions/torchyield.svg)](https://pypi.python.org/pypi/torchyield)
[![Documentation](https://img.shields.io/readthedocs/torchyield.svg)](https://torch-fuel.readthedocs.io/en/latest/)
[![Test status](https://img.shields.io/github/actions/workflow/status/kalekundert/torchyield/test.yml?branch=master)](https://github.com/kalekundert/torchyield/actions)
[![Test coverage](https://img.shields.io/codecov/c/github/kalekundert/torchyield)](https://app.codecov.io/github/kalekundert/torchyield)
[![Last commit](https://img.shields.io/github/last-commit/kalekundert/torchyield?logo=github)](https://github.com/kalekundert/torchyield)

*Torch Yield* is a library that makes it easier to create custom models in 
PyTorch. The key idea is to write models as generator functions, where each 
module is yielded in the order it should be invoked. This approach leads to 
very modular, flexible, and succinct code.  In turn, this makes it much easier 
and faster to experiment with different model architectures.  Here's an example 
of what this might look like:

```python
import torch
import torch.nn as nn
import torchyield as ty

def conv_relu(
        in_channels,
        out_channels,
        kernel_size=3,
        stride=1,
        padding=0,
):
    yield nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
    )
    yield nn.ReLU()

def conv_relu_pool(
        pool_size=3,
        pool_stride=2,
        **hparams,
):
    yield from conv_relu(**hparams)
    yield nn.MaxPool2d(
            kernel_size=pool_size,
            stride=pool_stride,
    )

def linear_relu_dropout(
        in_features,
        out_features,
        drop_rate=0.5,
):
    yield nn.Linear(
            in_features=in_features,
            out_features=out_features,
    )
    yield nn.ReLU()
    yield nn.Dropout(p=drop_rate)

def alexnet():
    yield from conv_relu_pool(
            in_channels=3,
            out_channels=96,
            kernel_size=11,
            stride=4,
    )
    yield from conv_relu_pool(
            in_channels=96,
            out_channels=256,
            kernel_size=5,
            padding=2,
    )
    yield from conv_relu(
            in_channels=256,
            out_channels=384,
            padding=1,
    )
    yield from conv_relu(
            in_channels=384,
            out_channels=384,
            padding=1,
    )
    yield from conv_relu_pool(
            in_channels=384,
            out_channels=256,
            padding=1,
    )

    yield nn.Flatten()

    yield from linear_relu_dropout(
            in_features=36 * 256,
            out_features=4096,
    )
    yield from linear_relu_dropout(
            in_features=4096,
            out_features=4096,
    )
    yield nn.Linear(
            in_features=4096,
            out_features=1000,
    )

# Convert the generator into an instance of `torch.nn.Sequential`:
f = ty.module_from_layers(alexnet())

# Demonstrate that the model works, i.e. it can make a prediction 
# given random input:
x = torch.randn(1, 3, 227, 227)
y = f(x)
print(torch.argmax(y))  # tensor(388)
```

[Model visualization](demos/alexnet_1.pdf)

Note how using generators makes it easy to compose complex models from simple 
building blocks.  In particular, this example starts by defining a simple
convolution-ReLU layer.  It then uses that layer to define a slightly more 
complex convolution-ReLU-pool layer.  Those two layers are ultimately used, 
along with another simple linear-ReLU-dropout layer, to define the full AlexNet 
model.

It would've been possible to define all the same building blocks as normal 
PyTorch modules (i.e. without using generators).  However, that approach 
would've been much more verbose.  We would've had to create a class for each 
layer, and then we would've had to worry about getting the hyperparameters from 
`__init__()` to `forward()`.

That said, the above example is still pretty verbose.  The reason why is that 
we didn't actually use `torchyield` much at all!  There are two big 
improvements we can make:

- All of the "simple" layers we need for this model are provided by 
  `torchyield`, so we can just import them rather than writing our own 
  functions.
- The bulk of the code consists of calling the same functions multiple times 
  with different arguments.  One of the most important helper functions 
  provided by `torchyield` is `make_layers()`, which automates this process.

```python
import torch.nn as nn
import torchyield as ty

def alexnet():
    # `make_layers()` zips together all the keyword arguments 
    # (including any scalar ones), then calls the same factory 
    # function on each set of arguments.  The `channels()` helper 
    # is useful: it breaks a list of channels into separate lists 
    # of input and output channels.  Also note that this factory 
    # function is smart enough to skip the pooling module when the 
    # `pool_size` parameter is 1 (or less).
    yield from ty.make_layers(
            ty.conv2_relu_maxpool_layer,
            **ty.channels([3, 96, 256, 384, 384, 256]),
            kernel_size=[11, 5, 3, 3, 3],
            stride=[4, 1, 1, 1, 1],
            padding=[0, 2, 1, 1, 1],
            pool_size=[3, 3, 1, 1, 3],
            pool_stride=2,
    )

    yield nn.Flatten()

    # `mlp_layer()` is very similar to `make_layers()`.  The only 
    # difference is that instead of using the given factory to 
    # make the last layer, it just makes a plain linear layer. 
    # This is because you typically don't want any nonlinear/ 
    # regularization layers after the last linear layer.
    yield from ty.mlp_layer(
            ty.linear_relu_dropout_layer,
            **ty.channels([36 * 256, 4096, 4096, 1000])
    )
```

[Model visualization](demos/alexnet_2.pdf)

Hopefully you can see how powerful this code is:

- It only took a few lines to define the whole model.
- Every hyperparameter is easy to see and modify.  This includes more 
  "structural" hyperparameters like the number of layers, and the 
  specific modules used in each layer.
- The `alexnet()` function is itself a generator, so it can be used to 
  build more complex models in the same way that we built it.

# Installation

Install *Torch Yield* from PyPI:

```console
$ pip install torchyield
```
