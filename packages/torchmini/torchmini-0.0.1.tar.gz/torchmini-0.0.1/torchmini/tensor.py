import tensor_cpp
import numpy as np
from torchmini.autograd import *
# import torch

class Tensor:

    def __init__(self, data = None, device = 'cpu', requires_grad = False):
        if data is not None:
            if isinstance(data, (int, float)):
                data = [data]
            data, shape = self.__flatten(data)
            self.set_tensor(tensor_cpp.Tensor(data, shape, device))
            self.requires_grad = requires_grad
            self.grad = None
            self.grad_fn = None
        else:
            self.tensor = None
            self.shape = None
            self.ndim = None
            self.device = device
            self.requires_grad = requires_grad
            self.grad = None
            self.grad_fn = None
    

    def __hash__(self):
        return id(self)

    def set_tensor(self, tensor):
        self.tensor = tensor
        self.shape = tensor.shape
        self.ndim = tensor.ndim
        self.device = tensor.device


    def __flatten(self, nested_list):
        def flatten_recursively(nested_list):
            flat_data = []
            shape = []
            if isinstance(nested_list, list):
                for sublist in nested_list:
                    inner_data, inner_shape = flatten_recursively(sublist)
                    flat_data.extend(inner_data)
                shape.append(len(nested_list))
                shape.extend(inner_shape)
            else:
                flat_data.append(nested_list)
            return flat_data, shape
        
        flat_data, shape = flatten_recursively(nested_list)
        return flat_data, shape


    def __getitem__(self, indices):
        if isinstance(indices, int):
            indices = [indices]
        if len(indices) != self.tensor.ndim:
            raise ValueError("Number of indices must match number of dimensions")
        return self.tensor.get_item(indices)
    

    def __str__(self):
        def print_recursively(tensor, depth, index):
            if depth == tensor.ndim - 1:
                result = ""
                for i in range(tensor.shape[-1]):
                    index[-1] = i
                    result += str(tensor[tuple(index)]) + ", "
                return result.strip()
            else:
                result = ""
                if depth > 0:
                    result += "\n" + " " * ((depth - 1) * 4)
                for i in range(tensor.shape[depth]):
                    index[depth] = i
                    result += "["
                    result += print_recursively(tensor, depth + 1, index) + "],"
                    if i < tensor.shape[depth] - 1:
                        result += "\n" + " " * (depth * 4)
                return result.strip(",")

        index = [0] * self.ndim
        result = "tensor(["
        result += print_recursively(self, 0, index)
        result += f"""], device="{self.device}", requires_grad={self.requires_grad})"""
        return result

    
    def __repr__(self):
        return self.__str__()
    

    def __add__(self, other):
        if isinstance(other, (int, float)):
            result = Tensor()
            result.set_tensor(self.tensor.add_scalar(other))

            result.requires_grad = self.requires_grad
            if self.requires_grad:
                self.grad_fn = add_backward(self, other)

            return result
        if isinstance(other, Tensor):
            if self.shape != other.shape:
                raise ValueError("Tensor shapes must match for addition")
            result = Tensor()
            result.set_tensor(self.tensor.add(other.tensor))

            result.requires_grad = self.requires_grad or other.requires_grad
            if self.requires_grad:
                self.grad_fn = add_backward(self, other)

            return result
        else:
            raise TypeError(f'Unsupported operand type(s) for +: "{type(self)}" and "{type(other)}"')
    

    def __sub__(self, other):
        if isinstance(other, Tensor):
            if self.shape != other.shape:
                raise ValueError("Tensor shapes must match for subtraction")
            result = Tensor()
            result.set_tensor(self.tensor.sub(other.tensor))

            result.requires_grad = self.requires_grad or other.requires_grad
            if self.requires_grad:
                self.grad_fn = sub_backward(self, other)

            return result
        else:
            raise TypeError(f'Unsupported operand type(s) for -: "{type(self)}" and "{type(other)}"')
   

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result = Tensor()
            result.set_tensor(self.tensor.scalar_mul(other))

            result.requires_grad = self.requires_grad
            if self.requires_grad:
                self.grad_fn = scalar_mul_backward(self, other)
            return result

        if isinstance(other, Tensor):
            if self.shape != other.shape:
                raise ValueError("Tensor shapes must match for multiplication")
            result = Tensor()
            result.set_tensor(self.tensor.elementwise_mul(other.tensor))

            result.requires_grad = self.requires_grad or other.requires_grad
            if self.requires_grad:
                self.grad_fn = mul_backward(self, other)
            return result

        else: 
            raise TypeError(f'Unsupported operand type(s) for *: "{type(self)}" and "{type(other)}"')
    
    def __rmul__(self, other):
        return self.__mul__(other)


    def __matmul__(self, other):
        if isinstance(other, Tensor):
            if self.ndim != 2 or other.ndim != 2:
                raise ValueError("Both tensors must be 2D for matrix multiplication")
            if self.shape[1] != other.shape[0]:
                raise ValueError("Inner dimensions of matrices must match")
            result = Tensor()
            result.set_tensor(self.tensor.matmul(other.tensor))

            result.requires_grad = self.requires_grad or other.requires_grad
            if self.requires_grad:
                self.grad_fn = matmul_backward(self, other)
            return result

        else:
            raise TypeError(f'Unsupported operand type(s) for @: "{type(self)}" and "{type(other)}"') 


    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            result = Tensor()
            result.set_tensor(self.tensor.tensor_div_scalar(other))

            result.requires_grad = self.requires_grad
            if self.requires_grad:
                self.grad_fn = div_backward(self, other)

            return result
        
        elif isinstance(other, Tensor):
            if self.shape != other.shape:
                raise ValueError("Tensor shapes must match for division")
            result = Tensor()
            result.set_tensor(self.tensor.tensor_div_tensor(other.tensor))

            result.requires_grad = self.requires_grad or other.requires_grad
            if self.requires_grad:
                self.grad_fn = div_backward(self, other)

            return result

        else: 
            raise TypeError(f'Unsupported operand type(s) for /: "{type(self)}" and "{type(other)}"')
        

    def __pow__(self, power):
        result = Tensor()
        result.set_tensor(self.tensor.tensor_pow_scalar(power))

        result.requires_grad = self.requires_grad
        if self.requires_grad:
            self.grad_fn = pow_backward(self, power)

        return result
    

    def __rpow__(self, base):
        result = Tensor()
        result.set_tensor(self.tensor.scalar_pow_tensor(base))

        result.requires_grad = self.requires_grad
        if self.requires_grad:
            self.grad_fn = pow_backward(base, self)

        return result


    def __lt__(self, other):
        if isinstance(other, (int, float)):
            result = Tensor()
            result.set_tensor(self.tensor.lt_scalar(other))
            return result

        elif isinstance(other, Tensor):
            if self.shape != other.shape:
                raise ValueError("Tensor shapes must match for comparison")
            result = Tensor()
            result.set_tensor(self.tensor.lt(other.tensor))
            return result

        else:
            raise TypeError(f'Unsupported operand type(s) for <: "{type(self)}" and "{type(other)}"')
    

    def __gt__(self, other):
        if isinstance(other, (int, float)):
            result = Tensor()
            result.set_tensor(self.tensor.gt_scalar(other))
            return result

        elif isinstance(other, Tensor):
            if self.shape != other.shape:
                raise ValueError("Tensor shapes must match for comparison")
            result = Tensor()
            result.set_tensor(self.tensor.gt(other.tensor))
            return result

        else:
            raise TypeError(f'Unsupported operand type(s) for >: "{type(self)}" and "{type(other)}"')
    

    def __eq__(self, other):
        if isinstance(other, Tensor):
            if self.shape != other.shape:
                raise ValueError("Tensor shapes must match for comparison")
            result = Tensor()
            result.set_tensor(self.tensor.eq(other.tensor))
            return result
        else:
            raise TypeError(f'Unsupported operand type(s) for ==: "{type(self)}" and "{type(other)}"')  
          

    def ones_like(self):
        result = Tensor()
        result.set_tensor(self.tensor.ones_like())
        result.requires_grad = self.requires_grad
        return result
    
    def zeros_like(self):
        result = Tensor()
        result.set_tensor(self.tensor.zeros_like())
        result.requires_grad = self.requires_grad
        return result


    def rand_like(self):
        result = Tensor()
        result.set_tensor(self.tensor.rand_like())
        result.requires_grad = self.requires_grad
        return result
    
   
    def reshape(self, new_shape):
        if new_shape.count(-1) > 1:
            raise ValueError("Only one dimension can be inferred")
        known_dims_product = 1
        for dim in new_shape:
            if dim != -1:
                known_dims_product *= dim
        if -1 in new_shape:
            new_shape[new_shape.index(-1)] = self.tensor.size // known_dims_product
        
        result = Tensor()
        result.set_tensor(self.tensor.reshape(new_shape))

        result.requires_grad = self.requires_grad
        if self.requires_grad:
            self.grad_fn = reshape_backward(self, new_shape)

        return result

   
    def sum(self, axis = None, keepdim = False):
        if axis is not None and axis < 0:
            axis += self.ndim
        
        if axis is None:
            axis = -1 

        if axis > self.tensor.ndim - 1:
            raise ValueError(f"Error: axis {axis} out of range for tensor of dimension {self.tensor.ndim}")
        
        result = Tensor()
        result.set_tensor(self.tensor.sum(axis, keepdim))

        result.requires_grad = self.requires_grad
        if self.requires_grad:
            self.grad_fn = sum_backward(self, axis, keepdim)

        return result


    def max(self, axis=None, keepdim=False):
        if axis is not None and axis < 0:
            axis += self.ndim
    
        if axis is None:
            axis = -1

        if axis > self.tensor.ndim - 1:
            raise ValueError(f"Error: axis {axis} out of range for tensor of dimension {self.tensor.ndim}")
    
        max_values, max_indices = self.tensor.max(axis, keepdim)

        # Wrap the results in Tensor objects
        max_values_tensor = Tensor()
        max_values_tensor.set_tensor(max_values)
        max_values_tensor.requires_grad = self.requires_grad

        max_indices_tensor = Tensor()
        max_indices_tensor.set_tensor(max_indices)
        max_indices_tensor.requires_grad = False  # indices don't require gradients

        if self.requires_grad:
            self.grad_fn = max_backward(self, axis, keepdim)

        return max_values_tensor, max_indices_tensor

    
    def sigmoid(self):
        result = Tensor()
        result.set_tensor(self.tensor.sigmoid())

        result.requires_grad = self.requires_grad
        if self.requires_grad:
            self.grad_fn = sigmoid_backward(self)

        return result
    
    def relu(self):
        result = Tensor()
        result.set_tensor(self.tensor.relu())

        result.requires_grad = self.requires_grad
        if self.requires_grad:
            self.grad_fn = relu_backward(self)

        return result
    
    def transpose(self):
        if self.ndim != 2:
            raise ValueError("Only 2D tensors can be transposed")
        result = Tensor()
        result.set_tensor(self.tensor.transpose())

        result.requires_grad = self.requires_grad
        if self.requires_grad:
            self.grad_fn = transpose_backward(self)

        return result
    
    def backward(self, grad = None):
        if not self.requires_grad:
            return 
        if grad is None:
            if self.shape == [1]:
                grad = Tensor([1])
            else:
                raise ValueError("grad must be provided for non-scalar output")
        stack = [(self, grad)]
        visited = set()
        while stack:
            # print(f"len(stack): {len(stack)}")
            tensor, grad = stack.pop()
            # print(f"tensor shape: {tensor.shape} | grad shape: {grad.shape} | grad_fn: {tensor.grad_fn}")
            if tensor.grad is None:
                tensor.grad = grad
            else:
                tensor.grad += grad
            if tensor.grad_fn is not None:
                # print(f"grad_fn: {tensor.grad_fn}")
                grads = tensor.grad_fn.backward(grad)
                # print(f"grads len: {len(grads)}")
                # print(type(grads[0]))
                # print(type(grads[1]))
                for tensor, grad in zip(tensor.grad_fn.input, grads):
                    # print(f"inner tensor shape: {tensor.shape} | grad shape: ")
                    if isinstance(tensor, Tensor) and isinstance(grad, Tensor) and tensor not in visited:
                        # print(f"inner inner tensor shape: {tensor.shape} | grad shape")
                        stack.append((tensor, grad))
                        # print(f"len(stack): {len(stack)}")
                        tensor, grad = stack[-1]
                        # print(f"tensor shape: {tensor.shape} | grad shape: {grad.shape}")
                        visited.add(tensor)
                        # print(f"len(visited): {len(visited)}")


    def zero_grad(self):
        self.grad = None


    def detach(self):
        self.grad = None
        self.grad_fn = None
    

    def log(self):
        result = Tensor()
        result.set_tensor(self.tensor.log())

        result.requires_grad = self.requires_grad
        if self.requires_grad:
            self.grad_fn = log_backward(self)

        return result
    
   
    def squeeze(self, axis = None):
        if axis is not None:
            if axis < 0:
                axis += self.ndim
            
            if axis >= self.ndim or axis < 0:
                raise ValueError(f"Error: axis {axis} out of range for tensor of dimension {self.ndim}")

            if self.shape[axis] != 1:
                raise ValueError(f"Error: cannot squeeze dimension {axis} which is not 1")
            
            new_shape = self.shape[:axis] + self.shape[axis + 1:]
        
        else:
            new_shape = [dim for dim in self.shape if dim != 1]
        
        return self.reshape(new_shape)
    

    def unsqueeze(self, axis):
        if axis < 0:
            axis += self.ndim + 1
        if axis > self.ndim or axis < 0:
            raise ValueError(f"Error: axis {axis} out of range for tensor of dimension {self.ndim}")
        new_shape = self.shape[:axis] + [1] + self.shape[axis:]
        return self.reshape(new_shape) 
    

    def flatten(self):
        return self.reshape([-1])
    

    def item(self):
        if self.tensor.size != 1:
            raise ValueError("Only scalar tensors can be converted to Python scalars")
        return self.tensor.data[0]


    def numpy(self):
        return np.array(self.tensor.data).reshape(self.shape) 
    

# def stack(tensors, axis = 0):
#     new_tensors = []
#     for tensor in tensors:
#         if isinstance(tensor, torch.Tensor):
#             new_tensors.append(Tensor(tensor.tolist()))
#         else:
#             new_tensors.append(tensor)
#     tensors = new_tensors
            
#     if not all(isinstance(tensor, Tensor) for tensor in tensors):
#         raise ValueError("All elements must be tensors")
#     if not all(tensor.shape == tensors[0].shape for tensor in tensors):
#         raise ValueError("All tensors must have the same shape")
#     if axis < 0:
#         axis += tensors[0].ndim + 1
#     if axis > tensors[0].ndim or axis < 0:
#         raise ValueError(f"Error: axis {axis} out of range for tensor of dimension {tensors[0].ndim}")
#     result = Tensor()
#     result.set_tensor(tensor_cpp.stack([tensor.tensor for tensor in tensors], axis))
#     return result