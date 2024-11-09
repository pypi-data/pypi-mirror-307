import torch.nn as nn

def make_factory(factory_name):
    """
    Dynamically create layer factories.

    For example, `ty.linear_bn_relu_layer()` is a factory that yields a linear 
    layer, followed by a batch normalization layer, followed by a ReLU.  The 
    rules for creating a factory are as follows:

    - The function name must end in "_layer".

    - The rest of the function name is a underscore-separated list of modules 
      to include in the layer.  The following modules can be specified:

      ========  =============
      Name      Module
      ========  =============
      linear    nn.Linear
      conv1     nn.Conv1d
      conv2     nn.Conv2d
      conv3     nn.Conv3d
      maxpool   nn.MaxPool*
      avgpool   nn.AvgPool*
      relu      nn.ReLU
      bn        nn.BatchNorm*
      dropout   nn.DropOut
      ========  =============

      *The dimensionality of any pooling/batch norm layers depends on the 
      dimensionality of a preceding convolution/linear layer.

    - The resulting factory will accept arguments for each module it creates.  
      For linear and convolutional modules, the argument names are the same as 
      for the corresponding modules [1].  For all other modules, the argument 
      names are prefixed by the name of the module (e.g. a dropout rate can be 
      specified as: `linear_dropout(dropout_p=0.1)`) [2,3].

      [1] The input and output dimensions for linear layers are specified via 
          *in_channels* and *out_channels* arguments, not *in_features* and 
          *out_features* as expected by `nn.Linear`.  This is just for 
          consistency with the convolutional layers, and to make the 
          `channels()` helper function easier to use.

      [2] Arguments for the pooling modules are just prefixed by `pool_`, not 
          `maxpool_` or `avgpool_`.  This is just for the sake of brevity.

      [3] The `inplace` argument for `nn.ReLU` isn't prefixed, and defaults to 
          True rather than False.

    Special considerations:

    - If a convolutional or linear layer is followed immediately by a batch 
      norm layer, the bias will be disabled by default.  Since the batch norm 
      will re-center the output on 0 anyways, there's no reason to calculate a 
      bias in such cases.
    """
    if not factory_name.endswith('_layer'):
        raise AttributeError(factory_name)

    module_names = factory_name.split('_')[:-1]

    def factory(**kwargs):
        state = {
                'factory_name': factory_name,
                'module_names': module_names,
                'kwargs': kwargs,
                'used_kwargs': set(),
        }

        assert set(FACTORY_GETTERS) == set(FACTORY_KWARGS_GETTERS)

        for i, module_name in enumerate(module_names):
            state['module_name'] = module_name
            state['i'] = i

            try:
                factory_getter = FACTORY_GETTERS[module_name]
            except KeyError:
                from difflib import get_close_matches
                did_you_mean = get_close_matches(module_name, FACTORY_GETTERS, n=1)
                suffix = f"\n• did you mean: {did_you_mean[0]!r}" if did_you_mean else ""
                raise AttributeError(f"{factory_name}() includes unknown module {module_name!r}{suffix}") from None

            factory = factory_getter(state)

            factory_kwargs = {}
            for f in FACTORY_KWARGS_GETTERS[module_name]:
                factory_kwargs |= f(state)

            if state.get('skip_module', False):
                del state['skip_module']
                continue

            yield factory(**factory_kwargs)

            try:
                state['curr_dimension'] = DIMENSIONS[module_name]
            except KeyError:
                pass

        unused_kwargs = set(kwargs) - state['used_kwargs']
        if unused_kwargs:
            raise TypeError(f"{factory_name}() got unexpected keyword argument(s): {','.join(map(repr, unused_kwargs))}")

    factory.__name__ = factory_name
    factory.__qualname__ = f'torchyield.{factory_name}'
    factory.__module__ = 'torchyield'

    return factory


def get_channels(in_key='in_channels', out_key='out_channels'):
    def _get_channels(state):
        if 'channel_module' in state:
            raise ValueError("{factory_name}() has {module_name!r} after {channel_module!r}\n✖ both of these modules need exclusive access to the `in_channels` and `out_channels` arguments".format_map(state))

        kwargs = state['kwargs']

        try:
            in_channels = kwargs['in_channels']
            out_channels = kwargs['out_channels']
        except KeyError as err:
            raise TypeError(f"{state['factory_name']}() missing required argument: {err}") from None

        state['curr_channels'] = out_channels
        state['channel_module'] = state['module_name']
        state['used_kwargs'].update(['in_channels', 'out_channels'])

        return {
                in_key: in_channels,
                out_key: out_channels,
        }

    return _get_channels

def get_curr_channels(key):
    def _get_curr_channels(state):
        try:
            curr_channels = state['curr_channels']
        except KeyError:
            raise ValueError("'{module_name}' must come after 'linear' or 'conv'".format_map(state))

        return {key: curr_channels}

    return _get_curr_channels
        
def get_bias(state):
    state['used_kwargs'].add('bias')
    kwargs = state['kwargs']

    try:
        bias = kwargs['bias']
    except KeyError:
        try:
            bias = state['module_names'][state['i'] + 1] != 'bn'
        except IndexError:
            bias = True

    return dict(bias=bias)

def get_pool_size(state):
    kwargs = get_kwargs(pool_size='kernel_size')(state)
    state['skip_module'] = kwargs and kwargs['kernel_size'] <= 1
    return kwargs

def get_inplace(state):
    state['used_kwargs'].add('inplace')

    kwargs = state['kwargs']

    try:
        inplace = kwargs['inplace']
    except KeyError:
        inplace = True

    return dict(inplace=inplace)

def get_kwargs(*kwarg_list, **kwarg_map):
    kwarg_map = {x: x for x in kwarg_list} | kwarg_map

    def _get_kwargs(state):
        state['used_kwargs'].update(kwarg_map)
        return {
                kwarg_map[k]: state['kwargs'][k]
                for k in state['kwargs']
                if k in kwarg_map
        }

    return _get_kwargs

def get_module(module):
    return lambda _: module

def get_module_by_dim(modules):

    def _get_module_by_dim(state):
        try:
            curr_dimension = state['curr_dimension']
        except KeyError:
            raise ValueError("'{module_name}' must come after 'linear' or 'conv'".format_map(state)) from None

        return modules[curr_dimension]

    return _get_module_by_dim

FACTORY_GETTERS = {
        'linear': get_module(nn.Linear),
        'conv1': get_module(nn.Conv1d),
        'conv2': get_module(nn.Conv2d),
        'conv3': get_module(nn.Conv3d),
        'maxpool': get_module_by_dim({
            1: nn.MaxPool1d,
            2: nn.MaxPool2d,
            3: nn.MaxPool3d,
        }),
        'avgpool': get_module_by_dim({
            1: nn.AvgPool1d,
            2: nn.AvgPool2d,
            3: nn.AvgPool3d,
        }),
        'relu': get_module(nn.ReLU),
        'bn': get_module_by_dim({
            1: nn.BatchNorm1d,
            2: nn.BatchNorm2d,
            3: nn.BatchNorm3d,
        }),
        'dropout': get_module(nn.Dropout),
}
FACTORY_KWARGS_GETTERS = {
        'linear': [
            get_channels('in_features', 'out_features'),
            get_bias,
        ],
        'conv1': (_conv := [
            get_channels(),
            get_bias,
            get_kwargs(
                'kernel_size',
                'stride',
                'padding',
                'dilation',
                'groups',
                'padding_mode',
            ),
        ]),
        'conv2': _conv,
        'conv3': _conv,
        'maxpool': [
            get_pool_size,
            get_kwargs(
                pool_stride='stride',
                pool_padding='padding',
                pool_dilation='dilation',
                pool_ceil_mode='ceil_mode',
            ),
        ],
        'avgpool': [
            get_pool_size,
            get_kwargs(
                pool_stride='stride',
                pool_padding='padding',
                pool_ceil_mode='ceil_mode',
                pool_count_include_pad='count_include_pad',
                pool_divisor_override='divisor_override',
            ),
        ],
        'relu': [
            get_inplace,
        ],
        'bn': [
            get_curr_channels('num_features'),
            get_kwargs(
                bn_eps='eps',
                bn_momentum='momentum',
                bn_affine='affine',
                bn_track_running_stats='track_running_stats',
            ),
        ],
        'dropout': [
            get_kwargs(
                dropout_p='p',
            ),
        ],
}
DIMENSIONS = {
        'linear': 1,
        'conv1': 1,
        'conv2': 2,
        'conv3': 3,
}

