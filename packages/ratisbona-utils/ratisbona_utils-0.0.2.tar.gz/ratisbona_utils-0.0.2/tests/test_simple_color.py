import unittest

from ratisbona_utils.colors.simple_color import f_inv, f


class MyTestCase(unittest.TestCase):

    def test_finv_must_be_inv_of_f(self):
        t=0.0
        while t<100.0:
            fval = f(t)
            finvval = f_inv(fval)
            print(t, fval, finvval)
            self.assertAlmostEqual( t, finvval)
            t += 0.01


if __name__ == '__main__':
    unittest.main()
