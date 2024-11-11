from torchmini.nn.module import Module


class Dropout(Module):
    def __init__(self, p=0.5):
        super(Dropout, self).__init__()
        self.p = p

    def forward(self, x):
        if self.training:
            mask = x.rand_like() > self.p
            return x * mask
        else:
            return x