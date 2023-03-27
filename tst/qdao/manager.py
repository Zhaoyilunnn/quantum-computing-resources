import numpy as np

from qiskit.compiler import transpile

from qdao.manager import SvManager
from qdao.test import QdaoBaseTest


class TestSvDao(QdaoBaseTest):

    _sv_dao = SvManager()

    def test_load_sv_continuous(self):
        vec0 = np.random.rand(4) + 1j * np.random.rand(4)
        vec1 = np.random.rand(4) + 1j * np.random.rand(4)
        vec2 = np.random.rand(4) + 1j * np.random.rand(4)
        vec3 = np.random.rand(4) + 1j * np.random.rand(4)
        print(vec0)
        print(vec1)
        print(vec2)
        print(vec3)
        np.save("sv0.npy", vec0)
        np.save("sv1.npy", vec1)
        np.save("sv2.npy", vec2)
        np.save("sv3.npy", vec3)

        self._sv_dao.load_sv([0,1,2])
        print(self._sv_dao._chunk)
        np.testing.assert_array_equal(self._sv_dao._chunk[0:4], vec0)
        np.testing.assert_array_equal(self._sv_dao._chunk[4:8], vec1)
        np.testing.assert_array_equal(self._sv_dao._chunk[8:12], vec2)
        np.testing.assert_array_equal(self._sv_dao._chunk[12:16], vec3)

    def test_load_sv_interleave(self):
        vec0 = np.random.rand(4) + 1j * np.random.rand(4)
        vec1 = np.random.rand(4) + 1j * np.random.rand(4)
        vec2 = np.random.rand(4) + 1j * np.random.rand(4)
        vec3 = np.random.rand(4) + 1j * np.random.rand(4)
        print(vec0)
        print(vec1)
        print(vec2)
        print(vec3)
        np.save("sv0.npy", vec0)
        np.save("sv1.npy", vec1)
        np.save("sv2.npy", vec2)
        np.save("sv3.npy", vec3)

        self._sv_dao.load_sv([0,1,3])
        print(self._sv_dao._chunk)
        np.testing.assert_array_equal(self._sv_dao._chunk[0:4], vec0)
        np.testing.assert_array_equal(self._sv_dao._chunk[4:8], vec2)
        np.testing.assert_array_equal(self._sv_dao._chunk[8:12], vec1)
        np.testing.assert_array_equal(self._sv_dao._chunk[12:16], vec3)

    def test_save_sv_continuous(self):
        vec = np.random.rand(16) + 1j * np.random.rand(16)
        self._sv_dao._chunk = vec
        self._sv_dao.store_sv([0,1,2])
        vec0 = np.load("sv0.npy")
        vec1 = np.load("sv1.npy")
        vec2 = np.load("sv2.npy")
        vec3 = np.load("sv3.npy")
        np.testing.assert_array_equal(self._sv_dao._chunk[0:4], vec0)
        np.testing.assert_array_equal(self._sv_dao._chunk[4:8], vec1)
        np.testing.assert_array_equal(self._sv_dao._chunk[8:12], vec2)
        np.testing.assert_array_equal(self._sv_dao._chunk[12:16], vec3)

    def test_save_sv_interleave(self):
        vec = np.random.rand(16) + 1j * np.random.rand(16)
        self._sv_dao._chunk = vec
        self._sv_dao.store_sv([0,1,3])
        vec0 = np.load("sv0.npy")
        vec1 = np.load("sv1.npy")
        vec2 = np.load("sv2.npy")
        vec3 = np.load("sv3.npy")
        np.testing.assert_array_equal(self._sv_dao._chunk[0:4], vec0)
        np.testing.assert_array_equal(self._sv_dao._chunk[8:12], vec1)
        np.testing.assert_array_equal(self._sv_dao._chunk[4:8], vec2)
        np.testing.assert_array_equal(self._sv_dao._chunk[12:16], vec3)