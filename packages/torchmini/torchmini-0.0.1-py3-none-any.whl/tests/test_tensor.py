import unittest
import torchmini
from torchmini.tensor import Tensor

class TestTensor(unittest.TestCase):
    
    def setUp(self):
        pass


    def test_element_access(self):
        a = Tensor([1, 2, 3, 4, 5])
        self.assertEqual(a[2], 3)

        b = Tensor([[1, 2], [3, 4]])
        self.assertEqual(b[1, 0], 3)
    

    def test_add(self):
        a = Tensor([[1, 2], [3, 4]]) 
        b = Tensor([[1, 2], [3, 4]])
        c = a + b
        self.assertEqual(c, Tensor([[2, 4], [6, 8]]))
    

    def test_sub(self):
        a = Tensor([[1, 11], [3, 4]])
        b = Tensor([[1, 2], [5, 4]])
        c = a - b
        self.assertEqual(c, Tensor([[0, 9], [-2, 0]]))
    

    def test_mul(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor([[1, 2], [3, 4]])
        c = a * b
        self.assertEqual(c, Tensor([[1, 4], [9, 16]]))

        d = a * 2
        self.assertEqual(d, Tensor([[2, 4], [6, 8]]))


    def test_matmul(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor([[1, 2], [3, 4]])
        c = a @ b
        self.assertEqual(c, Tensor([[7, 10], [15, 22]]))
    
    
    def test_div(self):
        a = Tensor([[1, 2], [3, 4]])
        b = a/2 
        self.assertEqual(b, Tensor([[0.5, 1], [1.5, 2]]))


    def test_pow(self):
        a = Tensor([[1, 2], [3, 4]])
        b = a**2
        self.assertEqual(b, Tensor([[1, 4], [9, 16]]))


    def test_lt(self):
        a = Tensor([[1, 2], [8, 4]])
        b = Tensor([[1, 2], [3, 6]])
        c = a < b
        self.assertEqual(c, Tensor([[False, False], [False, True]]))
    

    def test_gt(self):
        a = Tensor([[1, 2], [8, 4]])
        b = Tensor([[1, 2], [3, 6]])
        c = a > b
        self.assertEqual(c, Tensor([[False, False], [True, False]]))
    

    def test_eq(self):
        a = Tensor([[1, 2], [8, 4]])
        b = Tensor([[1, 2], [3, 6]])
        c = a == b
        self.assertEqual(c, Tensor([[True, True], [False, False]]))
    

    def test_ones_like(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor.ones_like(a)
        self.assertEqual(b, Tensor([[1, 1], [1, 1]]))

    
    def test_zeros_like(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor.zeros_like(a)
        self.assertEqual(b, Tensor([[0, 0], [0, 0]]))
    

    def test_rand_like(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor.rand_like(a)
        self.assertEqual(b.shape, a.shape)
    

    def test_reshape(self):
        a = Tensor([[1, 2], [3, 4]])
        b = a.reshape((1, 4))
        self.assertEqual(b, Tensor([[1, 2, 3, 4]]))
    

    def test_sum(self):
        a = Tensor([[1, 2], [3, 4]])
        b = a.sum()
        self.assertEqual(b, Tensor(10))

        c = a.sum(axis = 0)
        self.assertEqual(c, Tensor([4, 6]))

        d = a.sum(axis = 1)
        self.assertEqual(d, Tensor([3, 7]))

        e = a.sum(axis = 1, keepdim = True)
        self.assertEqual(e, Tensor([[3], [7]]))


    def test_max(self):
        a = Tensor([[2, 1], [3, 4]])
        values, indices = a.max()
        self.assertEqual(values, Tensor(4))
        self.assertEqual(indices, Tensor(3))

        values, indices = a.max(axis = 0)
        self.assertEqual(values, Tensor([3, 4]))
        self.assertEqual(indices, Tensor([1, 1]))

        values, indices = a.max(axis = 1)
        self.assertEqual(values, Tensor([2, 4]))
        self.assertEqual(indices, Tensor([0, 1]))

    def test_sigmoid(self):
        pass
    

    def test_relu(self):
        a = Tensor([[1, -2], [-3, 4]])
        b = a.relu()
        self.assertEqual(b, Tensor([[1, 0], [0, 4]]))
    

    def test_transpose(self):
        a = Tensor([[1, 2], [3, 4]])
        b = a.transpose()
        self.assertEqual(b, Tensor([[1, 3], [2, 4]]))


    def test_backward(self):
        pass

    
    def test_squeeze(self):
        a = Tensor([[[1, 2], [3, 4]]])
        b = a.squeeze()
        self.assertEqual(b, Tensor([[1, 2], [3, 4]]))
    

    def test_unsqueeze(self):
        a = Tensor([[1, 2], [3, 4]])
        b = a.unsqueeze(0)
        self.assertEqual(b, Tensor([[[1, 2], [3, 4]]]))

        c = b.squeeze(0)
        self.assertEqual(c, a)
    

    def test_flatten(self):
        a = Tensor([[1, 2], [3, 4]])
        b = a.flatten()
        self.assertEqual(b, Tensor([1, 2, 3, 4]))
    

    def test_item(self):
        a = Tensor([1])
        b = a.item()
        self.assertEqual(b, 1)
    

    def test_numpy(self):
        a = Tensor([1, 2, 3, 4])
        b = a.numpy()
        self.assertEqual(b.tolist(), [1, 2, 3, 4])
    

    def test_stack(self):
        a = Tensor([1, 2, 3])
        b = Tensor([4, 5, 6])
        c = torchmini.stack([a, b], axis=0)
        self.assertEqual(c, Tensor([[1, 2, 3], [4, 5, 6]]))
   
if __name__ == "__main__":
    unittest.main()