import unittest
import multidim_galerkin_pod.ten_sor_utils as tsu
import numpy as np


class TensorFoldUnfold(unittest.TestCase):
    def setUp(self):
        self.X = np.random.randn(10, 11, 12, 6, 5, 4, 3, 2)
        self.fdo = 2  # dimension to be flattened
        self.fdt = 5  # dimension to be flattened

    def test_fold_unfold_tensor_single(self):
        '''
        check if we can fold some dimensions and unfold it again
        '''

        fX, fXdims = tsu.flatten_mode(self.X, self.fdo,
                                      tdims=self.X.shape)
        fXf, _ = tsu.unflatten_mode(fX, self.fdo, ftdims=fXdims)
        # should be exact as it is the same values
        self.assertTrue(np.abs(self.X-fXf).sum() == 0)

    def test_fold_unfold_tensor_double(self):
        '''
        check if we can fold some dimensions and unfold it again
        '''

        fX, fXdims = tsu.flatten_mode(self.X, self.fdt,
                                      tdims=self.X.shape)
        ffX, ffXdims = tsu.flatten_mode(fX, self.fdo, tdims=fXdims)
        ffXf, ffXfdims = tsu.unflatten_mode(ffX, self.fdo, ftdims=ffXdims)
        ffXff, _ = tsu.unflatten_mode(ffXf, self.fdt, ftdims=ffXfdims)
        # should be exact as it is the same values
        self.assertTrue(np.abs(self.X-ffXff).sum() == 0.)

    def test_fold_unfold_tensor_mto(self):
        '''
        check if we can fold some dimensions and unfold it again
        '''

        fX, fXdims = tsu.flatten_mode(self.X, self.fdo,
                                      tdims=self.X.shape, howmany=4)
        fXf, _ = tsu.unflatten_mode(fX, self.fdo, ftdims=fXdims)
        # self.assertTrue(np.allclose(self.X, fXf, atol=1e-13))

        # should be exact as it is the same values
        self.assertTrue(np.abs((self.X-fXf)).sum() == 0.)


class TensorTranspose(unittest.TestCase):
    '''transposing tensors by cycling through the dimensions
    '''

    def setUp(self):
        self.X = np.random.randn(10, 11, 12, 6, 5, 4, 3, 2)

    def test_repeated_transposes(self):
        tX = tsu.tnsrtrnsps(self.X, 1)
        ttX = tsu.tnsrtrnsps(tX, 1)
        t2X = tsu.tnsrtrnsps(self.X, times=2)
        self.assertTrue(np.abs((ttX-t2X)).sum() == 0.)

    def test_tomode_transposes(self):
        ttX = tsu.tnsrtrnsps(self.X, tomode=4)
        t2X = tsu.tnsrtrnsps(self.X, times=3)
        self.assertTrue(np.abs((ttX-t2X)).sum() == 0.)

    def test_inverse_transposes(self):
        ttX = tsu.tnsrtrnsps(self.X, tomode=-3)
        ttXtt = tsu.tnsrtrnsps(ttX, tomode=3)
        self.assertTrue(np.abs((ttXtt-self.X)).sum() == 0.)

    def test_inverse_transposes_two(self):
        ttX = tsu.tnsrtrnsps(self.X, tomode=-4)
        ttXtt = tsu.tnsrtrnsps(ttX, times=3)
        self.assertTrue(np.abs((ttXtt-self.X)).sum() == 0.)

    def test_inverse_transposes_three(self):
        ttX = tsu.tnsrtrnsps(self.X, times=2)
        ttXtt = tsu.tnsrtrnsps(ttX, times=-2)
        self.assertTrue(np.abs((ttXtt-self.X)).sum() == 0.)


if __name__ == '__main__':
    unittest.main()
