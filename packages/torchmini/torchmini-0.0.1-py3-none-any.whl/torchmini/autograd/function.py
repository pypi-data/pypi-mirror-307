import torchmini

class add_backward:
    def __init__(self, x, y):
        self.input = [x, y]
    
    def backward(self, grad):
        return [grad, grad]

class sub_backward:
    def __init__(self, x, y):
        self.input = [x, y]
    
    def backward(self, grad):
        return [grad, -1 * grad]

class mul_backward:
    def __init__(self, x, y):
        self.input = [x, y]
    
    def backward(self, grad):
        return [grad * self.input[1], grad * self.input[0]]

class matmul_backward:
    def __init__(self, x, y):
        self.input = [x, y]
    
    def backward(self, grad):
        return [grad @ self.input[1].transpose(), self.input[0].transpose() @ grad]

class sum_backward:
    def __init__(self, x, axis = None, keepdim = False):
        self.input = [x]
        self.axis = axis
        self.keepdim = keepdim
    
    def backward(self, grad):
        # todo
        pass 

def reshape_backward(x, new_shape):
    def __init__(self, x):
        self.input = [x]

    def backward(self, grad):
        return [grad.reshape(self.input[0].shape)]

def transpose_backward(x):
    def __init__(self, x):
        self.input = [x]

    def backward(self, grad):
        return [grad.transpose()]

def sigmoid_backward(x):
    def __init__(self, x):
        self.input = [x]

    def backward(self, grad):
        return [grad * (1 - self.input[0].sigmoid()) * self.input[0].sigmoid()]

def relu_backward(x):
    def __init__(self, x):
        self.input = [x]

    def backward(self, grad):
        return [grad * (self.input[0] > 0).float()]

class cross_entropy_loss_backward:
    def __init__(self, logits, targets):
        self.input = [logits, targets]
    
    def backward(self, gradient):
        logits, targets = self.input

        if logits.ndim == 1:
            softmax = torchmini.softmax(logits, dim=0)
            grad_logits = (softmax - targets)
                
        elif logits.ndim == 2:
            # batched 
                batch_size = logits.shape[0]
                softmax = torchmini.softmax(logits, dim=1)

                grad_logits = (softmax - targets) / batch_size

        return [grad_logits, None]  # targets do not have a gradient


class log_backward:
    def __init__(self, x):
        self.input = [x]
    
    def backward(self, grad):
        return [grad / self.input[0]]

class pow_backward:
    def __init__(self, base, exponent):
        self.input = [base, exponent]
    
    def backward(self, grad):
        base, exponent = self.input
        grad_base = grad * exponent * (base ** (exponent - 1))
        grad_exponent = grad * (base ** exponent) * base.log()
        return [grad_base, grad_exponent]

class div_backward:
    def __init__(self, x, y):
        self.input = [x, y]
    
    def backward(self, grad):
        x, y = self.input
        return [grad / y, -1 * grad * x / (y ** 2)]

class scalar_mul_backward:
    def __init__(self, x, scalar):
        self.input = [x]
        self.scalar = scalar
    
    def backward(self, grad):
        return [grad * self.scalar]
    
class max_backward:
    def __init__(self, x, axis, keepdim):
        self.input = [x]
        self.axis = axis
        self.keepdim = keepdim
    
    def backward(self, grad):
        # todo
        pass