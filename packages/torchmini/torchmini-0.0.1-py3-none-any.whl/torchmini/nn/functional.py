import math
from torchmini.tensor import Tensor

def sigmoid(x):
    z = x.sigmoid()
    return z

def softmax(x, dim=None):
    if dim is not None and dim < 0:
        dim = x.ndim + dim
            
    x_max, _ = x.max(axis=dim, keepdim=True)
    expanded_x_max = Tensor([[val] * x.shape[1] for val in x_max.tensor.data])  # Assuming `x_max` has a `.data` attribute
    exp_x = math.e ** (x - expanded_x_max)

    epsilon = 1e-12
    if dim is not None:
        sum_exp_x = exp_x.sum(axis=dim, keepdim=True)
        expanded_sum_exp_x = Tensor([[val] * exp_x.shape[1] for val in sum_exp_x.tensor.data])  
        sum_exp_x = expanded_sum_exp_x
        return exp_x / sum_exp_x + epsilon
    else:
        sum_exp_x = exp_x.sum()
        return exp_x / sum_exp_x + epsilon
    
def one_hot_encode(x, num_classes):
    one_hot = [[0] * num_classes for _ in range(x.tensor.size)]

    # Set the appropriate elements to 1
    for i in range(x.tensor.size):
        target_idx = int(x[i])
        one_hot[i][target_idx] = 1

    return Tensor(one_hot)