from django.test import TestCase
from .utils.des import encrypt_des, decrypt_des, validate_des_key

# Create your tests here.

class DESTest(TestCase):
    def setUp(self):
        self.test_key = "12345678"  # 8 byte key
        self.plaintext = "admin"

    def test_encryption_decryption(self):
        # Encrypt
        encrypted = encrypt_des(self.test_key.encode(), self.plaintext)
        
        # Decrypt
        decrypted = decrypt_des(self.test_key.encode(), encrypted)
        
        # Assert
        self.assertEqual(self.plaintext, decrypted)

    def test_key_validation(self):
        # Test invalid key length
        invalid_key = "123"
        with self.assertRaises(ValueError):
            validate_des_key(invalid_key)

        # Test valid key length
        valid_key = "12345678"
        key_bytes = validate_des_key(valid_key)
        self.assertEqual(len(key_bytes), 8)

