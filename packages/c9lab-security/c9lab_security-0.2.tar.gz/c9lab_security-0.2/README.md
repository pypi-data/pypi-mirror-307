# c9lab-security

This package provides middleware for encrypting and decrypting requests and responses in Django Rest Framework.

## Installation

```bash
pip install c9lab-security



MIDDLEWARE = [
    ...,
    'c9lab_security.middleware.DecryptRequestMiddleware',
    'c9lab_security.middleware.EncryptResponseMiddleware',
]

# Set the encryption key
from c9lab_security.encryption_utility import EncryptionUtility
EncryptionUtility.set_key(b'your-16-byte-key')  # Use a 16, 24, or 32 byte key




Ensure your requests and responses use the application/json content type and include the encrypted data under the statistics field.