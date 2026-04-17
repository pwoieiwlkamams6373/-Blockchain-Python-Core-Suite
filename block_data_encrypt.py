from cryptography.fernet import Fernet
import json
import hashlib
from typing import Dict, Any

class BlockEncryptor:
    def __init__(self, secret_key: str = None):
        if secret_key:
            key = hashlib.sha256(secret_key.encode()).digest()
            self.key = Fernet(base64.urlsafe_b64encode(key))
        else:
            self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)

    def export_key(self) -> str:
        return self.key.decode()

    def encrypt_block(self, block_data: Dict[str, Any]) -> str:
        data_str = json.dumps(block_data).encode()
        encrypted = self.cipher.encrypt(data_str)
        return encrypted.decode()

    def decrypt_block(self, encrypted_data: str) -> Dict[str, Any]:
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return json.loads(decrypted)
        except:
            return {}

    def hash_encrypted_data(self, encrypted_data: str) -> str:
        return hashlib.sha256(encrypted_data.encode()).hexdigest()

import base64
