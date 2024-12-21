from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import (
    PrivateFormat, PublicFormat, Encoding, NoEncryption, load_pem_private_key, load_pem_public_key
)

import base64

def generate_rsa_key_pair():
    """
    RSA anahtar çifti üretir.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption()
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem.decode('utf-8'), public_pem.decode('utf-8')
   

def rsa_sign(data, private_key_pem):
    """
    Signs the data using RSA private key.
    """
    private_key = load_pem_private_key(private_key_pem.encode('utf-8'), password=None)
    signature = private_key.sign(
        data.encode('utf-8'),
        PKCS1v15(),
        SHA256()
    )
    return base64.b64encode(signature).decode('utf-8')

def rsa_verify(data, signature, public_key_pem):
    """
    Verifies the RSA signature.
    """
    public_key = load_pem_public_key(public_key_pem.encode('utf-8'))
    signature = base64.b64decode(signature.encode('utf-8'))
    try:
        public_key.verify(
            signature,
            data.encode('utf-8'),
            PKCS1v15(),
            SHA256()
        )
        return True
    except Exception as e:
        print(f"Verification failed: {e}")
        return False
