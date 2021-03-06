"""Test exponential, log, and powers of quaternions"""
from __future__ import division, print_function, absolute_import

import unittest
import os

import numpy as np

import rowan

one = np.array([1, 0, 0, 0])
zero = np.array([0, 0, 0, 0])


class TestExp(unittest.TestCase):
    """Test exponential function"""

    def test_exp(self):
        """Ensure that quaternion exponential behaves correctly"""
        self.assertTrue(np.all(rowan.exp(zero) == one))
        self.assertTrue(
                np.all(rowan.exp(one) ==
                       np.array([np.exp(1), 0, 0, 0])
                       )
                )
        x = np.array([0, 1, 1, 1])
        self.assertTrue(
                np.allclose(
                    rowan.exp(x),
                    np.array([-0.16055654, 0.5698601, 0.5698601, 0.5698601])
                    )
                )

        self.assertTrue(
                np.allclose(
                    rowan.exp(np.stack((x, one))),
                    np.stack((
                        np.array(
                            [-0.16055654, 0.5698601, 0.5698601, 0.5698601]
                            ),
                        np.array([np.exp(1), 0, 0, 0])
                        ))
                    )
                )

        self.assertTrue(
                np.allclose(
                    rowan.exp10(one),
                    rowan.exp(one*np.log(10))
                    )
                )

        base = 2
        self.assertTrue(
                np.allclose(
                    rowan.expb(one, base),
                    rowan.exp(one*np.log(base))
                    )
                )

        np.random.seed(0)
        shapes = [(4,), (1, 4), (3, 4, 4), (12, 7, 3, 4)]
        answers = np.load(os.path.join(
            os.path.dirname(__file__),
            'files/test_exp.npz'))
        for shape in shapes:
            x = np.random.random_sample(shape)
            self.assertTrue(
                    np.allclose(
                        rowan.exp(x), answers[str(shape)]
                        ),
                    msg="Failed for shape {}".format(shape))

    def test_log(self):
        """Ensure that quaternion logarithm behaves correctly"""
        self.assertTrue(np.all(rowan.log(one) == zero))
        self.assertTrue(
                np.all(
                    rowan.log(zero) ==
                    np.array([-np.inf, 0, 0, 0])
                    )
                )
        self.assertTrue(
                np.all(
                    rowan.log(np.stack((one, zero))) ==
                    np.stack((zero, np.array([-np.inf, 0, 0, 0])))
                    )
                )
        x = np.array([0, 1, 1, 1])
        self.assertTrue(
                np.allclose(
                    rowan.log(np.stack((x, zero))),
                    np.stack((
                        np.array(
                            [0.54930614, 0.90689968, 0.90689968, 0.90689968]
                            ),
                        np.array([-np.inf, 0, 0, 0])))
                    )
                )

        np.random.seed(0)
        shapes = [(4,), (1, 4), (3, 4, 4), (12, 7, 3, 4)]
        answers = np.load(os.path.join(
            os.path.dirname(__file__),
            'files/test_log.npz'))
        for shape in shapes:
            x = np.random.random_sample(shape)
            self.assertTrue(
                    np.allclose(
                        rowan.log(x), answers[str(shape)]
                        ),
                    msg="Failed for shape {}".format(shape))

    def test_logb(self):
        """Ensure that quaternion logarithm for any base behaves correctly"""
        base_test = 3
        self.assertTrue(np.all(rowan.logb(one, base_test) == zero))
        self.assertTrue(
                np.all(
                    rowan.logb(zero, base_test) ==
                    np.array([-np.inf, 0, 0, 0])
                    )
                )

        np.random.seed(0)
        shapes = [(4,), (1, 4), (3, 4, 4), (12, 7, 3, 4)]
        answers = np.load(os.path.join(
            os.path.dirname(__file__),
            'files/test_log.npz'))
        for shape in shapes:
            x = np.random.random_sample(shape)
            self.assertTrue(
                    np.allclose(
                        rowan.logb(x, base_test),
                        answers[str(shape)]/np.log(base_test)
                        ),
                    msg="Failed for shape {}".format(shape))

    def test_log10(self):
        """Ensure that quaternion base 10 logarithm behaves correctly"""
        self.assertTrue(np.all(rowan.log10(one) == zero))
        self.assertTrue(
                np.all(
                    rowan.log10(zero) ==
                    np.array([-np.inf, 0, 0, 0])
                    )
                )

        np.random.seed(0)
        shapes = [(4,), (1, 4), (3, 4, 4), (12, 7, 3, 4)]
        answers = np.load(os.path.join(
            os.path.dirname(__file__),
            'files/test_log.npz'))
        for shape in shapes:
            x = np.random.random_sample(shape)
            self.assertTrue(
                    np.allclose(
                        rowan.log10(x),
                        answers[str(shape)]/np.log(10)
                        ),
                    msg="Failed for shape {}".format(shape))

    def test_power(self):
        """Ensure that quaternion power behaves correctly"""
        self.assertTrue(np.all(rowan.power(one, 0) == one))
        self.assertTrue(np.all(rowan.power(one, 1) == one))
        self.assertTrue(np.all(rowan.power(one, 10) == one))
        self.assertTrue(np.all(rowan.power(zero, 0) == one))
        self.assertTrue(np.all(rowan.power(zero, 1) == zero))
        self.assertTrue(np.all(rowan.power(zero, 10) == zero))

        np.random.seed(0)
        shapes = [(4,), (1, 4), (3, 4, 4), (12, 7, 3, 4)]
        max_power = 8
        for shape in shapes:
            x = np.random.random_sample(shape)
            cur_ans = x
            for i in range(1, max_power+1):
                self.assertTrue(
                        np.allclose(
                            rowan.power(x, i),
                            cur_ans
                            ),
                        msg="Failed for shape {}".format(shape))
                cur_ans = rowan.multiply(cur_ans, x)
