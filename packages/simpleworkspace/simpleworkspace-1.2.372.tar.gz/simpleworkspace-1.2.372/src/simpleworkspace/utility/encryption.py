from base64 import b64decode as _b64decode, b64encode as _b64encode
from cryptography.hazmat.primitives import hashes as _hashes, padding as _padding
from cryptography.hazmat.primitives.ciphers import Cipher as _Cipher, algorithms as _algorithms, modes as _modes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from io import BufferedIOBase
import os
from simpleworkspace.types.byte import ByteEnum

class _CrossCryptV1:
    __SALT_LENGTH = 8
    __IV_LENGTH = 16
    __KEY_LENGTH = 32

    def __init__(self) -> None:
        import warnings
        warnings.warn("CrossCryptV1 is deprected, please use v2", DeprecationWarning)

    def _DeriveKey(self, password:str, salt:bytes):
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

        kdf = PBKDF2HMAC(
            algorithm=_hashes.SHA256(),
            length=self.__KEY_LENGTH + self.__IV_LENGTH,
            salt=salt,
            iterations=10000
        ).derive(password.encode())
        key = kdf[:self.__KEY_LENGTH]
        iv = kdf[self.__KEY_LENGTH:]
        return key, iv
    
    def EncryptFile(self, inputPath:str, password:str, outputPath:str=None):
        from simpleworkspace.io import file

        if(outputPath is None):
            outputPath = f'{inputPath}.oscc'

        file.Create(
            outputPath,
            self.EncryptBytes(
                file.Read(inputPath, type=bytes),
                password
            )
        )
        return outputPath
    
    def DecryptFile(self, inputPath:str, password:str, outputPath:str=None):
        from simpleworkspace.io import file

        if(outputPath is None):
            outputPath = inputPath.removesuffix('.oscc')

        file.Create(
            outputPath,
            self.DecryptBytes(
                file.Read(inputPath, type=bytes),
                password
            )
        )
        return outputPath

        
    def EncryptString(self, plainText:str, password:str):
        cipherBytes = self.EncryptBytes(plainText.encode(), password)
        return _b64encode(cipherBytes).decode()
    
    def DecryptString(self, cipherText:str, password:str):
        plainBytes = self.DecryptBytes(_b64decode(cipherText), password)
        return plainBytes.decode()

    def EncryptBytes(self, plainBytes:bytes, password:str):
        import os

        salt = os.urandom(self.__SALT_LENGTH)
        key, iv = self._DeriveKey(password, salt)
        cipher = _Cipher(_algorithms.AES(key), _modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = _padding.PKCS7(_algorithms.AES.block_size).padder()
        padded_data = padder.update(plainBytes) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return b'Salted__' + salt + encrypted_data

    def DecryptBytes(self, cipherBytes:bytes, password:str):
        salt = cipherBytes[8:16] #skip first 8 of header "__Salted"
        key, iv = self._DeriveKey(password, salt)

        encrypted_data = cipherBytes[16:] #skip first 8 "__Salted" and next 8 which is the salt itself
        cipher = _Cipher(_algorithms.AES(key), _modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = _padding.PKCS7(_algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data

class CrossCryptV2:
    # Format: schema[32] + CipherNonce[16] + Cipher...
    #   -schema is reserved space

    DEF_AES_KEY_LENGTH = 32
    DEF_PASSWORD_HASH_ITER = 100000

    class Headers:
        class _Schema:
            '''reserved usage for future'''
            DEF_LENGTH = 32
            def ParseBytes(self, schema:bytes):
                return
            def ToBytes(self):
                return bytes([0]*self.DEF_LENGTH)

        DEF_NONCE_LENGTH = 16
        DEF_LENGTH = _Schema.DEF_LENGTH + DEF_NONCE_LENGTH
                
        def __init__(self):
            self.schema = self._Schema()
            self.nonce:bytes = None

        def ParseBytes(self, headers:bytes):
            self.schema.ParseBytes(headers[:self._Schema.DEF_LENGTH])
            self.nonce = headers[self._Schema.DEF_LENGTH:self.DEF_LENGTH]

        def ToBytes(self):
            if(self.nonce is None):
                raise Exception("Headers cannot be constructed, missing nonce...")
            return self.schema.ToBytes() + self.nonce

    def __init__(self, password:str) -> None:
        self._password = password
    
    def GetEncryptor(self):
        nonce = os.urandom(self.Headers.DEF_NONCE_LENGTH)
        cipher = Cipher(algorithms.AES(self._GetDerivedKey()), modes.CTR(nonce), backend=default_backend())
        encryptor = cipher.encryptor()

        headers = self.Headers()
        headers.nonce = nonce
        return headers, encryptor
        
    def GetDecryptor(self, headers:Headers):
        cipher = Cipher(algorithms.AES(self._GetDerivedKey()), modes.CTR(headers.nonce), backend=default_backend())
        encryptor = cipher.decryptor()
        return encryptor

    def EncryptString(self, plainText:str):
        cipherBytes = self.EncryptBytes(plainText.encode())
        return _b64encode(cipherBytes).decode()
    
    def DecryptString(self, cipherText:str):
        plainBytes = self.DecryptBytes(_b64decode(cipherText))
        return plainBytes.decode()

    def EncryptBytes(self, plainBytes:bytes):
        headers, encryptor = self.GetEncryptor()
        return headers.ToBytes() + encryptor.update(plainBytes) + encryptor.finalize()
    
    def DecryptBytes(self, cipherBytes:bytes):
        headers = self.Headers()
        headers.ParseBytes(cipherBytes[:self.Headers.DEF_LENGTH])
        cipherBytes = cipherBytes[self.Headers.DEF_LENGTH:]
        decryptor = self.GetDecryptor(headers)

        return decryptor.update(cipherBytes) + decryptor.finalize()
    
    def EncryptStream(self, inputStream:BufferedIOBase, outputStream:BufferedIOBase):
        readSize = 1 * ByteEnum.MegaByte.value
        headers, encryptor = self.GetEncryptor()
        outputStream.write(headers.ToBytes())
        while(True):
            data = inputStream.read(readSize)
            if not data:
                break
            outputStream.write(encryptor.update(data))
        
        outputStream.write(encryptor.finalize())
        outputStream.flush()

    def DecryptStream(self, inputStream:BufferedIOBase, outputStream:BufferedIOBase):
        readSize = 1 * ByteEnum.MegaByte.value

        headers = self.Headers()
        headers.ParseBytes(inputStream.read(self.Headers.DEF_LENGTH))
        decryptor = self.GetDecryptor(headers)

        while(True):
            data = inputStream.read(readSize)
            if not data:
                break
            outputStream.write(decryptor.update(data))
        
        outputStream.write(decryptor.finalize())
        outputStream.flush()
        
    _cache_GetDerivedKey = None
    def _GetDerivedKey(self):
        if self._cache_GetDerivedKey is not None:
            return self._cache_GetDerivedKey
        # Using PBKDF2HMAC with SHA-256 to derive a 256-bit key (32 bytes)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.DEF_AES_KEY_LENGTH,  # 32 bytes = 256 bits
            salt=bytes([0] * 16), #16 null bytes, salting password is not practical for encryption usage
            iterations=self.DEF_PASSWORD_HASH_ITER,
            backend=default_backend()
        )
        key = kdf.derive(self._password.encode())
        self._cache_GetDerivedKey = key
        return key
    
