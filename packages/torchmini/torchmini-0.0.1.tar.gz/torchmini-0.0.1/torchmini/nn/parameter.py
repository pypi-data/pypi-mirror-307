from torchmini.tensor import Tensor
import random

class Parameter(Tensor):
    def __init__(self, shape):
        data = self.random_init(shape)
        super().__init__(data, requires_grad=True)
    
    def random_init(self, shape):
        if len(shape) == 0:
            return []
        else:
            inner_shape = shape[1:]
            if len(inner_shape) == 0:
                return [random.uniform(-1, 1) for _ in range(shape[0])]
            else:
                return [self.random_init(inner_shape) for _ in range(shape[0])]

