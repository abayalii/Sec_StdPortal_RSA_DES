from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64
import os

def validate_des_key(key: str) -> bytes:
    key = key.encode()
    if len(key) != 8:
        raise ValueError("DES key must be exactly 8 bytes long.")
    return key

def encrypt_des(key: bytes, plaintext: str) -> str:
    iv = os.urandom(8)  # Generate random IV
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_text = pad(plaintext.encode(), DES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    # Combine IV and encrypted text
    return base64.b64encode(iv + encrypted_text).decode()

def decrypt_des(key: bytes, encrypted_text: str) -> str:
    encrypted_data = base64.b64decode(encrypted_text)
    iv = encrypted_data[:8]  # Extract IV
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted_text = unpad(
        cipher.decrypt(encrypted_data[8:]), 
        DES.block_size
    )
    return decrypted_text.decode()





