from torchmini.nn.module import Module
from torchmini.nn.parameter import Parameter

class Linear(Module):
    def __init__(self, in_features, out_features, bias=False):
        super(Linear, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = Parameter(shape=[in_features, out_features])
        if bias:
            self.bias = Parameter(shape=[out_features, 1])
        else:
            self.bias = None
    
    def forward(self, x):
        if self.bias is not None:
            # print(x.shape)
            # print(self.weight.shape)
            return x @ self.weight + self.bias
        else:
            return x @ self.weight
    