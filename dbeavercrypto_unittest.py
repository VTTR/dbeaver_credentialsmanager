import unittest

from dbeavercrypto import encrypt, decrypt

class TestDBeaverCrypt(unittest.TestCase):
    def test_encrypt(self):
        self.assertEqual('OwEKLE4jpQ==', encrypt('Hello'))

    def test_decrypt(self):
        self.assertEqual('Hello', decrypt('OwEKLE4jpQ=='))

if __name__ == '__main__':
    unittest.main()