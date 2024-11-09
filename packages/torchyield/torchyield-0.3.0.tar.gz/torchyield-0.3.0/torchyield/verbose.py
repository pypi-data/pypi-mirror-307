import torch.nn as nn

BRIGHT_WHITE = '\033[97m'
RESET_COLOR = '\033[0m'
DEFAULT_VERBOSE_TEMPLATE = f'{BRIGHT_WHITE}{{}}\nin: {{}}{RESET_COLOR}\n{79*"─"}'

class VerboseModuleWrapper(nn.Module):

    def __init__(self, module, template=DEFAULT_VERBOSE_TEMPLATE, **kwargs):
        super().__init__()
        self.module = module
        self.template = template
        self.print_kwargs = kwargs

    def forward(self, x, *args, **kwargs):
        print(self.template.format(self.module, x.shape), **self.print_kwargs)
        return self.module(x, *args, **kwargs)

def verbose(layers):
    yield from map(VerboseModuleWrapper, layers)


