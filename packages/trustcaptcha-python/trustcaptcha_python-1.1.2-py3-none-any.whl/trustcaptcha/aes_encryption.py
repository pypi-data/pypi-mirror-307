import base64

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad


class AesEncryption:
    STANDARD_BLOCK_SIZE = 16

    @staticmethod
    def to_aes_secret_key(key_string):
        return base64.b64decode(key_string)

    @staticmethod
    def decrypt_to_string(key, encrypted_text):
        decoded = base64.b64decode(encrypted_text)
        return AesEncryption.decrypt(key, decoded)

    @staticmethod
    def decrypt(key, encrypted_data):
        iv = encrypted_data[:AesEncryption.STANDARD_BLOCK_SIZE]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data[AesEncryption.STANDARD_BLOCK_SIZE:])
        return unpad(decrypted, AES.block_size).decode('utf-8')

