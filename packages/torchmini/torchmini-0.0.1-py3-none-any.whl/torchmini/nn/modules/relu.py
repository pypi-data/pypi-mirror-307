from torchmini.nn.module import Module

class ReLU(Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return x.relu()