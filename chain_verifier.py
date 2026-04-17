from typing import List, Dict, Any

class ChainVerifier:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def verify_chain_integrity(self) -> bool:
        chain = self.blockchain.chain
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i-1]

            if current_block["previous_hash"] != self.blockchain.hash_block(previous_block):
                return False
            
            if not self.blockchain.valid_proof(previous_block["proof"], current_block["proof"]):
                return False
        return True

    def find_chain_fork(self) -> List[int]:
        fork_indices = []
        chain = self.blockchain.chain
        for i in range(1, len(chain)):
            prev_hash = chain[i]["previous_hash"]
            real_prev_hash = self.blockchain.hash_block(chain[i-1])
            if prev_hash != real_prev_hash:
                fork_indices.append(i)
        return fork_indices

    def export_chain_health_report(self) -> Dict[str, Any]:
        return {
            "chain_length": len(self.blockchain.chain),
            "is_valid": self.verify_chain_integrity(),
            "fork_positions": self.find_chain_fork()
        }
