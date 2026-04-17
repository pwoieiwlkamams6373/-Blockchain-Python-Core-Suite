from time import time
from typing import Dict, Any

class BlockMiner:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.miner_reward = 1.0

    def mine_pending_transactions(self, miner_address: str) -> Dict[str, Any]:
        if not self.blockchain.pending_transactions:
            raise Exception("无待处理交易，无需挖矿")
        
        last_block = self.blockchain.last_block
        last_proof = last_block["proof"]
        proof = self.blockchain.proof_of_work(last_proof)

        self.blockchain.add_transaction(
            sender="0",
            recipient=miner_address,
            amount=self.miner_reward
        )

        new_block = {
            "index": len(self.blockchain.chain) + 1,
            "timestamp": time(),
            "transactions": self.blockchain.pending_transactions,
            "proof": proof,
            "previous_hash": self.blockchain.hash_block(last_block)
        }

        self.blockchain.chain.append(new_block)
        self.blockchain.pending_transactions = []
        return new_block

    def set_miner_reward(self, reward: float) -> None:
        if reward > 0:
            self.miner_reward = reward
