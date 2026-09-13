import os
from cryptography.fernet import Fernet


class EncryptionManager:
    def __init__(self, key_file: str = "secret.key"):
        self.key_file = key_file
        self.cipher_suite = self._initialize_encryption()

    def _initialize_encryption(self) -> Fernet:
        """Инициализация шифрования"""
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
        else:
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()

        return Fernet(key)

    def encrypt(self, data: str) -> str:
        """Шифрование данных"""
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Дешифрование данных"""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()