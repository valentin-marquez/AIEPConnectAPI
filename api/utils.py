from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import time
import os

class SimpleCrypto:
    ALGORITHM = algorithms.AES
    CHARSET = 'utf-8'
    HEX = '0123456789ABCDEF'
    NUM_ALGORITHM = 'SHA1PRNG'

    @staticmethod
    def encrypt(str, str2):
        key = SimpleCrypto._get_raw_key(str.encode(SimpleCrypto.CHARSET))
        cipher = Cipher(SimpleCrypto.ALGORITHM(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(SimpleCrypto.ALGORITHM.block_size).padder()
        padded_data = padder.update(str2.encode(SimpleCrypto.CHARSET)) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return SimpleCrypto._to_hex(ciphertext)

    @staticmethod
    def decrypt(str, str2):
        key = SimpleCrypto._get_raw_key(str.encode(SimpleCrypto.CHARSET))
        cipher = Cipher(SimpleCrypto.ALGORITHM(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext_padded = decryptor.update(bytes.fromhex(str2)) + decryptor.finalize()
        unpadder = padding.PKCS7(SimpleCrypto.ALGORITHM.block_size).unpadder()
        plaintext = unpadder.update(plaintext_padded) + unpadder.finalize()
        return plaintext.decode(SimpleCrypto.CHARSET)

    @staticmethod
    def _get_raw_key(bArr):
        backend = default_backend()
        salt = bArr
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )
        return kdf.derive(bArr)

    @staticmethod
    def _to_byte(str):
        return bytes.fromhex(str)

    @staticmethod
    def _to_hex(bArr):
        return bArr.hex()

    @staticmethod
    def _append_hex(stringBuffer, b):
        stringBuffer.append(SimpleCrypto.HEX[(b >> 4) & 15])
        stringBuffer.append(SimpleCrypto.HEX[b & 15])


class AESEncryption:
    ALGORITHM = algorithms.AES
    ALGORITHM_DIGEST = hashes.SHA1()
    CHARSET = 'utf-8'
    HEX = '0123456789ABCDEF'
    TRANSFORMATION = algorithms.AES.block_size

    @staticmethod
    def encrypt(str, str2):
        try:
            key = str2.encode(AESEncryption.CHARSET)
            cipher = Cipher(AESEncryption.ALGORITHM(key), modes.CBC(b'\x00' * 16), backend=default_backend())
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(AESEncryption.TRANSFORMATION).padder()
            padded_data = padder.update(str.encode(AESEncryption.CHARSET)) + padder.finalize()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            return SimpleCrypto._to_hex(ciphertext)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def decrypt(str, str2):
        try:
            key = str2.encode(AESEncryption.CHARSET)
            cipher = Cipher(AESEncryption.ALGORITHM(key), modes.CBC(b'\x00' * 16), backend=default_backend())
            decryptor = cipher.decryptor()
            plaintext_padded = decryptor.update(bytes.fromhex(str)) + decryptor.finalize()
            unpadder = padding.PKCS7(AESEncryption.TRANSFORMATION).unpadder()
            plaintext = unpadder.update(plaintext_padded) + unpadder.finalize()
            return plaintext.decode(AESEncryption.CHARSET)
        except Exception as e:
            print(e)
            raise RuntimeError(e)

    @staticmethod
    def encrypt_with_passphrase(str, str2):
        try:
            digest = hashes.Hash(AESEncryption.ALGORITHM_DIGEST, backend=default_backend())
            digest.update(str2.encode(AESEncryption.CHARSET))
            key = digest.finalize()[:16]
            cipher = Cipher(AESEncryption.ALGORITHM(key), modes.CBC(b'\x00' * 16), backend=default_backend())
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(AESEncryption.TRANSFORMATION).padder()
            padded_data = padder.update(str.encode(AESEncryption.CHARSET)) + padder.finalize()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            return SimpleCrypto._to_hex(ciphertext)
        except Exception as e:
            raise RuntimeError("wrong key")

    @staticmethod
    def to_hex(bArr):
        return bArr.hex()

    @staticmethod
    def _append_hex(stringBuffer, b):
        stringBuffer.append(AESEncryption.HEX[(b >> 4) & 15])
        stringBuffer.append(AESEncryption.HEX[b & 15])

    @staticmethod
    def decrypt_with_passphrase(str, str2):
        try:
            digest = hashes.Hash(AESEncryption.ALGORITHM_DIGEST, backend=default_backend())
            digest.update(str2.encode(AESEncryption.CHARSET))
            key = digest.finalize()[:16]
            cipher = Cipher(AESEncryption.ALGORITHM(key), modes.CBC(b'\x00' * 16), backend=default_backend())
            decryptor = cipher.decryptor()
            plaintext_padded = decryptor.update(bytes.fromhex(str)) + decryptor.finalize()
            unpadder = padding.PKCS7(AESEncryption.TRANSFORMATION).unpadder()
            plaintext = unpadder.update(plaintext_padded) + unpadder.finalize()
            return plaintext.decode(AESEncryption.CHARSET)
        except Exception as e:
            raise RuntimeError("wrong key")

    @staticmethod
    def to_byte(str):
        return bytes.fromhex(str)


class ZubronHelper:
    """
    Attributes:
        
    

    Returns:
        _type_: _description_
    """
    NSE = "*NSE*"
    NSS = "*NSS*"
    TSE = "*TSE*"
    TSS = "*TSS*"
    UNE = "*UNE*"
    UNS = "*UNS*"


    @staticmethod
    def get_encrypted_token(username:str = ""):
        stringBuffer = []
        valueOf = str(int(time.time() * 1000))
        stringBuffer.append(ZubronHelper.UNS)
        stringBuffer.append(username)
        stringBuffer.append(ZubronHelper.UNE)
        stringBuffer.append(ZubronHelper.NSS)
        stringBuffer.append("Moofwd")
        stringBuffer.append(ZubronHelper.NSE)
        stringBuffer.append(ZubronHelper.TSS)
        stringBuffer.append(valueOf)
        stringBuffer.append(ZubronHelper.TSE)
        return AESEncryption.encrypt(''.join(stringBuffer), os.getenv('TOKEN_SECRET_KEY'))




