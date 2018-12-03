from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import unittest

import numpy as np

from art.data_generators import KerasDataGenerator, PyTorchDataGenerator, MXDataGenerator


logger = logging.getLogger('testLogger')


class TestKerasDataGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import keras

        class DummySequence(keras.utils.Sequence):
            def __init__(self):
                self._size = 5
                self._x = np.random.rand(self._size, 28, 28, 1)
                self._y = np.random.randint(0, high=10, size=(self._size, 10))

            def __len__(self):
                return self._size

            def __getitem__(self, idx):
                return self._x[idx], self._y[idx]

        sequence = DummySequence()
        cls.data_gen = KerasDataGenerator(sequence, size=5, batch_size=1)

    def test_gen_interface(self):
        gen = self._dummy_gen()
        data_gen = KerasDataGenerator(gen, size=None, batch_size=5)

        x, y = data_gen.get_batch()

        # Check return types
        self.assertTrue(isinstance(x, np.ndarray))
        self.assertTrue(isinstance(y, np.ndarray))

        # Check shapes
        self.assertTrue(x.shape == (5, 28, 28, 1))
        self.assertTrue(y.shape == (5, 10))

    def test_gen_keras_specific(self):
        gen = self._dummy_gen()
        data_gen = KerasDataGenerator(gen, size=None, batch_size=5)

        iter_ = iter(data_gen.generator)
        x, y = next(iter_)

        # Check return types
        self.assertTrue(isinstance(x, np.ndarray))
        self.assertTrue(isinstance(y, np.ndarray))

        # Check shapes
        self.assertTrue(x.shape == (5, 28, 28, 1))
        self.assertTrue(y.shape == (5, 10))

    def test_sequence_keras_specific(self):
        iter_ = iter(self.data_gen.generator)
        x, y = next(iter_)

        # Check return types
        self.assertTrue(isinstance(x, np.ndarray))
        self.assertTrue(isinstance(y, np.ndarray))

        # Check shapes
        self.assertTrue(x.shape == (28, 28, 1))
        self.assertTrue(y.shape == (10,))

    def test_sequence_interface(self):
        x, y = self.data_gen.get_batch()

        # Check return types
        self.assertTrue(isinstance(x, np.ndarray))
        self.assertTrue(isinstance(y, np.ndarray))

        # Check shapes
        self.assertTrue(x.shape == (28, 28, 1))
        self.assertTrue(y.shape == (10,))

    # def test_imagedatagen_keras_specific(self):
    #     from keras.preprocessing.image import ImageDataGenerator
    #
    #     pass
    #
    # def test_imagedatagen_interface(self):

    @staticmethod
    def _dummy_gen(size=5):
        yield np.random.rand(size, 28, 28, 1), np.random.randint(low=0, high=10, size=(size, 10))


class TestPyTorchGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import torch
        from torch.utils.data import DataLoader

        class DummyDataset(torch.utils.data.Dataset):
            def __init__(self):
                self._size = 10
                self._x = np.random.rand(self._size, 1, 5, 5)
                self._y = np.random.randint(0, high=10, size=self._size)

            def __len__(self):
                return self._size

            def __getitem__(self, idx):
                return self._x[idx], self._y[idx]

        dataset = DummyDataset()
        data_loader = DataLoader(dataset=dataset, batch_size=5, shuffle=True)
        cls.data_gen = PyTorchDataGenerator(data_loader, size=10, batch_size=5)

    def test_gen_interface(self):
        x, y = self.data_gen.get_batch()

        # Check return types
        self.assertTrue(isinstance(x, np.ndarray))
        self.assertTrue(isinstance(y, np.ndarray))

        # Check shapes
        self.assertTrue(x.shape == (5, 1, 5, 5))
        self.assertTrue(y.shape == (5,))

    def test_pytorch_specific(self):
        import torch

        iter_ = iter(self.data_gen.data_loader)
        x, y = next(iter_)

        # Check return types
        self.assertTrue(isinstance(x, torch.Tensor))
        self.assertTrue(isinstance(y, torch.Tensor))

        # Check shapes
        self.assertTrue(x.shape == (5, 1, 5, 5))
        self.assertTrue(y.shape == (5,))


class TestMXGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import mxnet as mx

        x = mx.random.uniform(shape=(10, 1, 5, 5))
        y = mx.random.uniform(shape=10)
        dataset = mx.gluon.data.dataset.ArrayDataset(x, y)

        data_loader = mx.gluon.data.DataLoader(dataset, batch_size=5, shuffle=True)
        cls.data_gen = MXDataGenerator(data_loader, size=10, batch_size=5)

    def test_gen_interface(self):
        x, y = self.data_gen.get_batch()

        # Check return types
        self.assertTrue(isinstance(x, np.ndarray))
        self.assertTrue(isinstance(y, np.ndarray))

        # Check shapes
        self.assertTrue(x.shape == (5, 1, 5, 5))
        self.assertTrue(y.shape == (5,))

    def test_mxnet_specific(self):
        import mxnet as mx

        iter_ = iter(self.data_gen.data_loader)
        x, y = next(iter_)

        # Check return types
        self.assertTrue(isinstance(x, mx.ndarray.NDArray))
        self.assertTrue(isinstance(y, mx.ndarray.NDArray))

        # Check shapes
        self.assertTrue(x.shape == (5, 1, 5, 5))
        self.assertTrue(y.shape == (5,))
