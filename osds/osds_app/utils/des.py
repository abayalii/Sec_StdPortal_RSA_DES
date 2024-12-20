from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64


# Ensure the key is always 8 bytes long (DES requires an 8-byte key)
def ensure_key_length(key: str) -> str:
    return key.ljust(8, '\0')[:8]  # Pad to 8 bytes if too short, truncate if too long


def encrypt_des(key: str, plaintext: str) -> str:
    key = ensure_key_length(key)
    key_bytes = key.encode()
    cipher = DES.new(key_bytes, DES.MODE_ECB)
    padded_text = pad(plaintext.encode(), DES.block_size)  # Apply padding to plaintext
    encrypted_text = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted_text).decode()


def decrypt_des(key: str, encrypted_text: str) -> str:
    key = ensure_key_length(key)
    key_bytes = key.encode()
    cipher = DES.new(key_bytes, DES.MODE_ECB)
    decoded_encrypted_text = base64.b64decode(encrypted_text)
    decrypted_text = unpad(cipher.decrypt(decoded_encrypted_text), DES.block_size)  # Remove padding
    return decrypted_text.decode()
