import unittest

from demo_app import is_prime, primes_below


class PrimeTests(unittest.TestCase):
    def test_small_numbers(self):
        self.assertEqual(primes_below(20), [2, 3, 5, 7, 11, 13, 17, 19])

    def test_edges(self):
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(2))
        self.assertFalse(is_prime(9))

    def test_a_larger_prime(self):
        self.assertTrue(is_prime(104729))


if __name__ == "__main__":
    unittest.main()
