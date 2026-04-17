import hashlib
from typing import List

class MerkleTree:
    def __init__(self, transactions: List[str]):
        self.transactions = transactions
        self.root = self.build_merkle_root()

    def hash_node(self, node: str) -> str:
        return hashlib.sha256(node.encode()).hexdigest()

    def build_merkle_root(self) -> str:
        if not self.transactions:
            return self.hash_node("")
        
        nodes = [self.hash_node(tx) for tx in self.transactions]
        while len(nodes) > 1:
            temp = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i+1] if i+1 < len(nodes) else left
                combined = self.hash_node(left + right)
                temp.append(combined)
            nodes = temp
        return nodes[0]

    def get_merkle_root(self) -> str:
        return self.root

    def verify_transaction_in_block(self, tx_hash: str, proof: List[str]) -> bool:
        current_hash = tx_hash
        for node in proof:
            current_hash = self.hash_node(current_hash + node)
        return current_hash == self.root
