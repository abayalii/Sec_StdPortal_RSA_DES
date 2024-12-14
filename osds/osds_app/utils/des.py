from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

def des_encrypt(data, des_key):
    """
    Veriyi DES algoritması ile şifreler.
    """
    des_key = base64.b64decode(des_key.encode('utf-8'))
    iv = os.urandom(8)  # DES blok boyutu
    cipher = Cipher(algorithms.DES(des_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    # PKCS7 Padding
    padding_length = 8 - (len(data) % 8)
    data += chr(padding_length) * padding_length
    encrypted_data = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_data).decode('utf-8')

def des_decrypt(encrypted_data, des_key):
    """
    Şifrelenmiş veriyi DES algoritması ile çözer.
    """
    encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
    des_key = base64.b64decode(des_key.encode('utf-8'))
    iv, encrypted_data = encrypted_data[:8], encrypted_data[8:]
    cipher = Cipher(algorithms.DES(des_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # PKCS7 Padding'i Kaldır
    padding_length = decrypted_data[-1]
    return decrypted_data[:-padding_length].decode('utf-8')
