from torchmini.optim.optimizer import Optimizer
from torchmini.tensor import Tensor

class Adam(Optimizer):
    def __init__(self, parameters, lr=1e-3, beta1=0.9, beta2=0.999, eps=1e-8):
        super().__init__(parameters)
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self._cache = {'m': [p.zeros_like() for (_, _, p) in self.parameters],
                       'v': [p.zeros_like() for (_, _, p) in self.parameters],
                       't': 0}

    def step(self):
        self._cache['t'] += 1
        for i, (module, name, _) in enumerate(self.parameters):
            parameter = getattr(module, name)
            if not isinstance(parameter.grad, Tensor):
                continue

            m = self._cache['m'][i]
            v = self._cache['v'][i]

            # print(parameter.grad_fn)
            # print(parameter.requires_grad)

            m = self.beta1 * m + (1 - self.beta1) * parameter.grad
            v = self.beta2 * v + (1 - self.beta2) * (parameter.grad ** 2)

            m_hat = m / (1 - self.beta1 ** self._cache['t'])
            v_hat = v / (1 - self.beta2 ** self._cache['t'])

            updated_parameter = parameter - self.lr * m_hat / (v_hat ** 0.5 + self.eps)
            setattr(module, name, updated_parameter)

            self._cache['m'][i] = m
            self._cache['v'][i] = v

            parameter.detach()
            m.detach()
            v.detach()