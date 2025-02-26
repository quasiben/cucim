import unittest

import cupy as cp
from cupy.testing import assert_array_equal
from cupyx.scipy.ndimage import binary_dilation, binary_erosion
from skimage import data

from cucim.skimage import feature
from cucim.skimage.util import img_as_float


class TestCanny(unittest.TestCase):
    def test_00_00_zeros(self):
        """Test that the Canny filter finds no points for a blank field"""
        result = feature.canny(cp.zeros((20, 20)), 4, 0, 0, cp.ones((20, 20),
                               bool))
        self.assertFalse(cp.any(result))

    def test_00_01_zeros_mask(self):
        """Test that the Canny filter finds no points in a masked image"""
        result = (feature.canny(cp.random.uniform(size=(20, 20)), 4, 0, 0,
                                cp.zeros((20, 20), bool)))
        self.assertFalse(cp.any(result))

    def test_01_01_circle(self):
        """Test that the Canny filter finds the outlines of a circle"""
        i, j = cp.mgrid[-200:200, -200:200].astype(float) / 200
        c = cp.abs(cp.sqrt(i * i + j * j) - 0.5) < 0.02
        result = feature.canny(c.astype(float), 4, 0, 0, cp.ones(c.shape, bool))
        #
        # erode and dilate the circle to get rings that should contain the
        # outlines
        #
        # TODO: grlee77: only implemented brute_force=True, so added that to
        #                these tests
        cd = binary_dilation(c, iterations=3, brute_force=True)
        ce = binary_erosion(c, iterations=3, brute_force=True)
        cde = cp.logical_and(cd, cp.logical_not(ce))
        self.assertTrue(cp.all(cde[result]))
        #
        # The circle has a radius of 100. There are two rings here, one
        # for the inside edge and one for the outside. So that's
        # 100 * 2 * 2 * 3 for those places where pi is still 3.
        # The edge contains both pixels if there's a tie, so we
        # bump the count a little.
        point_count = cp.sum(result)
        self.assertTrue(point_count > 1200)
        self.assertTrue(point_count < 1600)

    def test_01_02_circle_with_noise(self):
        """Test that the Canny filter finds the circle outlines
        in a noisy image"""
        cp.random.seed(0)
        i, j = cp.mgrid[-200:200, -200:200].astype(float) / 200
        c = cp.abs(cp.sqrt(i * i + j * j) - 0.5) < 0.02
        cf = c.astype(float) * 0.5 + cp.random.uniform(size=c.shape) * 0.5
        result = feature.canny(cf, 4, 0.1, 0.2, cp.ones(c.shape, bool))
        #
        # erode and dilate the circle to get rings that should contain the
        # outlines
        #
        cd = binary_dilation(c, iterations=4, brute_force=True)
        ce = binary_erosion(c, iterations=4, brute_force=True)
        cde = cp.logical_and(cd, cp.logical_not(ce))
        self.assertTrue(cp.all(cde[result]))
        point_count = cp.sum(result)
        self.assertTrue(point_count > 1200)
        self.assertTrue(point_count < 1600)

    def test_image_shape(self):
        self.assertRaises(ValueError, feature.canny, cp.zeros((20, 20, 20)), 4,
                          0, 0)

    def test_mask_none(self):
        result1 = feature.canny(cp.zeros((20, 20)), 4, 0, 0, cp.ones((20, 20),
                                bool))
        result2 = feature.canny(cp.zeros((20, 20)), 4, 0, 0)
        self.assertTrue(cp.all(result1 == result2))

    @cp.testing.with_requires("skimage>=1.18")
    def test_use_quantiles(self):
        image = img_as_float(cp.asarray(data.camera()[::100, ::100]))

        # Correct output produced manually with quantiles
        # of 0.8 and 0.6 for high and low respectively
        correct_output = cp.asarray(
            [[False, False, False, False, False, False],
             [False,  True,  True,  True, False, False],   # noqa
             [False, False, False,  True, False, False],   # noqa
             [False, False, False,  True, False, False],   # noqa
             [False, False,  True,  True, False, False],   # noqa
             [False, False, False, False, False, False]])

        result = feature.canny(image, low_threshold=0.6, high_threshold=0.8,
                               use_quantiles=True)

        assert_array_equal(result, correct_output)

    def test_invalid_use_quantiles(self):
        image = img_as_float(cp.array(data.camera()[::50, ::50]))

        self.assertRaises(ValueError, feature.canny, image, use_quantiles=True,
                          low_threshold=0.5, high_threshold=3.6)

        self.assertRaises(ValueError, feature.canny, image, use_quantiles=True,
                          low_threshold=-5, high_threshold=0.5)

        self.assertRaises(ValueError, feature.canny, image, use_quantiles=True,
                          low_threshold=99, high_threshold=0.9)

        self.assertRaises(ValueError, feature.canny, image, use_quantiles=True,
                          low_threshold=0.5, high_threshold=-100)

        # Example from issue #4282
        image = data.camera()
        self.assertRaises(ValueError, feature.canny, image, use_quantiles=True,
                          low_threshold=50, high_threshold=150)

    def test_dtype(self):
        """Check that the same output is produced regardless of image dtype."""
        image_uint8 = cp.asarray(data.camera())
        image_float = img_as_float(image_uint8)

        result_uint8 = feature.canny(image_uint8)
        result_float = feature.canny(image_float)

        assert_array_equal(result_uint8, result_float)
