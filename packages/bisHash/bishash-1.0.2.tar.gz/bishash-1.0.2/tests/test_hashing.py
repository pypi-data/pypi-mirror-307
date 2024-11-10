import unittest
from hashing import HashingAlgorithm

class TestHashingAlgorithm(unittest.TestCase):
    def setUp(self):
        self.hasher = HashingAlgorithm()

    def test_hash(self):
        data = "my_data"
        hashed_data = self.hasher.hash(data)
        self.assertEqual(hashed_data, "hashed_my_data")

    def test_verify(self):
        data = "my_data"
        hashed_data = self.hasher.hash(data)
        self.assertTrue(self.hasher.verify(data, hashed_data))
        self.assertFalse(self.hasher.verify("wrong_data", hashed_data))

if __name__ == '__main__':
    unittest.main()
