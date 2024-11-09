import torch.nn as nn

from more_itertools import zip_broadcast, pairwise, unzip
from itertools import cycle

from collections.abc import Iterable, Callable
from typing import TypeAlias

Layer: TypeAlias = Iterable[nn.Module] | nn.Module
LayerFactory: TypeAlias = Callable[..., Layer]

class FrozenSequential(nn.Module):
    """
    Execute the given layers in sequential order.

    Once constructed, the layers cannot be modified.  This makes inheriting 
    from this class a bit more convenient.  Since no API for modifying 
    the layers is exposed, subclasses do not have their namespaces polluted 
    with potentially dangerous methods.
    """

    def __init__(self, *layers: Layer):
        super().__init__()
        for i, child in enumerate(modules_from_layers(*layers)):
            self.add_module(str(i), child)

    def forward(self, x):
        for module in self.children():
            x = module(x)
        return x

def module_from_layers(*layers: Layer, verbose: bool = False) -> nn.Module:
    layers = modules_from_layers(*layers)

    if verbose:
        from .verbose import verbose as _verbose
        layers = _verbose(layers)

    layers = list(layers)

    if len(layers) == 0:
        return nn.Identity()
    elif len(layers) == 1:
        return layers[0]
    else:
        return nn.Sequential(*layers)

def modules_from_layers(*layers: Layer) -> Iterable[nn.Module]:
    for layer in layers:
        if isinstance(layer, nn.Module):
            yield layer
        else:
            yield from layer


def make_layers(layer_factory: LayerFactory, **params) -> Iterable[Layer]:
    # Normally we want to be strict, but `itertools.cycle()` is useful enough 
    # to merit an exception.
    strict = not any(isinstance(x, cycle) for x in params.values())

    for values in zip_broadcast(*params.values(), strict=strict):
        kwargs = dict(zip(params.keys(), values))
        layer = layer_factory(**kwargs)

        if isinstance(layer, nn.Module):
            yield layer
        else:
            yield from layer

def channels(
        channels: Iterable[int],
        keys: tuple[str, str] = ('in_channels', 'out_channels'),
) -> dict[str, list[int]]:
    values = map(list, unzip(pairwise(channels)))
    return dict(zip(keys, values))


def mlp_layer(layer_factory, in_channels, out_channels, **kwargs):
    yield from make_layers(
            layer_factory,
            in_channels=in_channels[:-1],
            out_channels=out_channels[:-1],
            **kwargs,
    )
    yield nn.Linear(in_channels[-1], out_channels[-1], bias=True)

