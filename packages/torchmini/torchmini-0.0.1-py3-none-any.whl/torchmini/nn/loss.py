from torchmini.nn.module import Module
from torchmini.tensor import Tensor
from torchmini.nn import functional as F
from torchmini.autograd import *
from abc import ABC

class Loss(Module, ABC):
    "Abstract class for loss functions"

    def __init__(self):
        super().__init__()

    def forward(self, predictions, labels):
        raise NotImplementedError
            
    def __call__(self, *inputs):
        return self.forward(*inputs)
    

class MSELoss(Loss):
    def __init__(self):
        super().__init__()

    def forward(self, predictions, target):
        assert target.shape == predictions.shape, \
            "Labels and predictions shape does not match: {} and {}".format(target.shape, predictions.shape)
        
        cost = ((predictions - target) ** 2).sum() / predictions.numel
        return cost
    

class CrossEntropyLoss(Loss):
    def __init__(self):
        super().__init__()

    def forward(self, input, target):
        # print("CrossEntropyLoss forward")
        # print(f"input shape: {input.shape} | target shape: {target.shape}")

        assert isinstance(input, Tensor), \
            "Cross entropy argument 'input' must be Tensor, not {}".format(type(input))
        
        assert isinstance(target, Tensor), \
            "Cross entropy argument 'target' must be Tensor, not {}".format(type(target))
        if input.ndim > 2:
            input = input.squeeze(-1)

        if input.ndim == 1:
            if target.numel == 1:
                num_classes = input.shape[0]
                target = F.one_hot_encode(target, num_classes)
                
                logits = F.softmax(input, dim=0)
                target = target.reshape(logits.shape)
                cost = -1*(logits.log() * target).sum()
                
            else:
                # target -> class probabilities (one-hot encoded)
                assert target.shape == input.shape, \
                    "Input and target shape does not match: {} and {}".format(input.shape, target.shape)
                logits = F.softmax(input, dim=0)
                target = target.reshape(logits.shape)
                cost = -1*(logits.log() * target).sum()


        elif input.ndim == 2:
            if target.ndim > 1:
                target = target.squeeze(-1)
            # batched 
            if target.ndim == 1:
                # target -> Ground truth class indices:
                num_classes = input.shape[1]

                target = F.one_hot_encode(target, num_classes)
                # print(f"Target shape: {target.shape}")
                
                batch_size = input.shape[0]
                logits = F.softmax(input, dim=1)
                # print(f"Logits shape: {logits.shape}")
                target = target.reshape(logits.shape)
                # print(f"Target shape: {target.shape}")

                # print(f"logits: {logits}")
                # print(f"target: {target}")
                # a = logits.log()
                # print(f"logits.log(): {a}")
                # b = a * target
                # print(f"logits.log() * target: {b}")
                # c = b.sum()
                # print(f"(logits.log() * target).sum(): {c}")
                # d = -1 * c
                # print(f"-1 * (logits.log() * target).sum(): {d}")
                # e = d / batch_size
                # print(f"-1 * (logits.log() * target).sum() / batch_size: {e}")
                cost = -1*(logits.log() * target).sum() / batch_size
                # print(f"Cost: {cost}")

            else:
                # target -> class probabilities (one-hot encoded)
                assert target.shape == input.shape, \
                    "Input and target shape does not match: {} and {}".format(input.shape, target.shape)
                
                batch_size = input.shape[0]
                logits = F.softmax(input, dim=1)
                target = target.reshape(logits.shape)
                cost = -(logits.log() * target).sum() / batch_size

        if input.requires_grad:
            cost.grad_fn = cross_entropy_loss_backward(input, target)

        # print(f"Cost: {cost}")        
        return cost
            


