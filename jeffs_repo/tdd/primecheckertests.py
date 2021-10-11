'''
   primecheckertests.py
   Jeff Ondich, 9 May 2012
   Updated for use in a lab exercise, 4 Nov 2013
'''

import primechecker
import unittest

class PrimeCheckerTester(unittest.TestCase):
    def setUp(self):
        self.prime_checker = primechecker.PrimeChecker(100)
        print("setup")

    def tearDown(self):
        print("tear")
        pass

    def test_zero(self):
        self.assertFalse(self.prime_checker.is_prime(0))
            
        print("tzero")

    def test_two(self):
        self.assertTrue(self.prime_checker.is_prime(2))
        print("two")

    
    def test_one(self):
        self.assertFalse(self.prime_checker.is_prime(1))
        print("one")

    def test_prime(self):
        self.assertTrue(self.prime_checker.is_prime(97))
        print("zprime")

    def test_composite(self):
        self.assertFalse(self.prime_checker.is_prime(96))
        print("vcomposite")

    def test_primes_below(self):
        self.assertEqual(self.prime_checker.get_primes_below(20), [2, 3, 5, 7, 11, 13, 17, 19])
        print("prime below")

    def test_negative(self):
        # self.assertRaises(ValueError,self.prime_checker.is_prime,0)
        with self.assertRaises(ValueError):
             self.prime_checker.is_prime(-50)
if __name__ == '__main__':
    unittest.main()

