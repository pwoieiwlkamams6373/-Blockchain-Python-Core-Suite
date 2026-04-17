from typing import List, Dict, Any
import hashlib
import time

class Layer2Rollup:
    def __init__(self, l1_chain):
        self.l1_chain = l1_chain
        self.batch_transactions: List[Dict] = []
        self.batches: List[Dict] = []
        self.batch_size = 10

    def add_l2_transaction(self, tx: Dict[str, Any]) -> bool:
        if not all(k in tx for k in ["sender", "recipient", "amount"]):
            return False
        tx["tx_hash"] = hashlib.sha256(f"{tx}{time.time()}".encode()).hexdigest()
        self.batch_transactions.append(tx)
        if len(self.batch_transactions) >= self.batch_size:
            self.create_batch()
        return True

    def create_batch(self) -> str:
        batch_id = hashlib.sha256(str(time.time()).encode()).hexdigest()
        batch = {
            "batch_id": batch_id,
            "transactions": self.batch_transactions.copy(),
            "timestamp": time.time(),
            "l1_block": None
        }
        self.batches.append(batch)
        self.batch_transactions = []
        return batch_id

    def commit_to_l1(self, batch_id: str) -> bool:
        for batch in self.batches:
            if batch["batch_id"] == batch_id:
                batch["l1_block"] = len(self.l1_chain.chain) + 1
                return True
        return False

    def get_batch(self, batch_id: str) -> Dict[str, Any]:
        for batch in self.batches:
            if batch["batch_id"] == batch_id:
                return batch
        return {}

    def get_pending_batch_count(self) -> int:
        return len(self.batch_transactions)
