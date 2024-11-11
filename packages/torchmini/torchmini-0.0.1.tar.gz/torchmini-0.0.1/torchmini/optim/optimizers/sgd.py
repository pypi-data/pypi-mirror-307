from torchmini.optim.optimizer import Optimizer
from torchmini.tensor import Tensor

class SGD(Optimizer):
    def __init__(self, parameters, lr=1e-1, momentum=0):
        super().__init__(parameters)
        self.lr = lr
        self.momentum = momentum
        self._cache = {'velocity': [p.zeros_like() for (_, _, p) in self.parameters]}

    
    def step(self):
        for i, (module, name, _) in enumerate(self.parameters):
            parameter = getattr(module, name)

            if not isinstance(parameter.grad, Tensor):
                continue
            
            velocity = self._cache['velocity'][i]

            velocity = self.momentum * velocity - self.lr * parameter.grad

            updated_parameter = parameter + velocity
            # updated_parameter.hooks = parameter.hooks.copy()

            setattr(module, name, updated_parameter)

            self._cache['velocity'][i] = velocity

            parameter.detach()
            velocity.detach()
            del parameter
