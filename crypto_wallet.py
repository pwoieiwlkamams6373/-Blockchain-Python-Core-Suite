import hashlib
import ecdsa
import binascii
from dataclasses import dataclass

@dataclass
class CryptoWallet:
    private_key: str = None
    public_key: str = None
    address: str = None

    def generate_key_pair(self) -> None:
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.private_key = binascii.hexlify(sk.to_string()).decode()
        vk = sk.get_verifying_key()
        self.public_key = binascii.hexlify(vk.to_string()).decode()
        self.generate_wallet_address()

    def generate_wallet_address(self) -> None:
        pub_key_bytes = binascii.unhexlify(self.public_key)
        sha256_hash = hashlib.sha256(pub_key_bytes).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        self.address = binascii.hexlify(ripemd160_hash).decode()

    def sign_transaction(self, transaction_data: str) -> str:
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(self.private_key), curve=ecdsa.SECP256k1)
        signature = sk.sign(transaction_data.encode())
        return binascii.hexlify(signature).decode()

    def verify_signature(self, public_key: str, transaction_data: str, signature: str) -> bool:
        vk = ecdsa.VerifyingKey.from_string(binascii.unhexlify(public_key), curve=ecdsa.SECP256k1)
        try:
            return vk.verify(binascii.unhexlify(signature), transaction_data.encode())
        except:
            return False
