import hashlib
import random
from typing import Dict, bool

class ZKProof:
    def __init__(self, secret: str):
        self.secret = secret
        self.secret_hash = self._hash(secret)

    def _hash(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def generate_proof(self) -> Dict[str, str]:
        rand_val = str(random.randint(100000, 999999))
        commitment = self._hash(self.secret + rand_val)
        return {
            "commitment": commitment,
            "random": rand_val,
            "public_hash": self.secret_hash
        }

    def verify_proof(self, proof: Dict[str, str]) -> bool:
        computed = self._hash(self.secret + proof["random"])
        return computed == proof["commitment"] and proof["public_hash"] == self.secret_hash

    def verify_anonymous_ownership(self, proof: Dict[str, str]) -> bool:
        try:
            return self.verify_proof(proof)
        except:
            return False
