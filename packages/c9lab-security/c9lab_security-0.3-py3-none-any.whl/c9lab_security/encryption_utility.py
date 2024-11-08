import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class EncryptionUtility:
    _key = None
    block_size = AES.block_size

    @classmethod
    def set_key(cls, key):
        cls._key = key

    @classmethod
    def encrypt(cls, data):
        if not cls._key:
            raise ValueError("Encryption key not set.")
        cipher = AES.new(cls._key, AES.MODE_CBC)
        iv = cipher.iv
        encrypted_data = cipher.encrypt(pad(data.encode(), cls.block_size))
        return base64.b64encode(iv + encrypted_data).decode()

    @classmethod
    def decrypt(cls, token):
        if not cls._key:
            raise ValueError("Encryption key not set.")
        data = base64.b64decode(token)
        iv = data[:cls.block_size]
        cipher = AES.new(cls._key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(data[cls.block_size:]), cls.block_size)
        return json.loads(decrypted_data.decode())
