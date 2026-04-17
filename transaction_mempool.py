from typing import List, Dict, Any
import heapq
import hashlib

class TransactionMempool:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.transactions = []
        self.tx_hashes = set()

    def add_transaction(self, tx: Dict[str, Any], fee: float) -> bool:
        tx_hash = hashlib.sha256(str(tx).encode()).hexdigest()
        if tx_hash in self.tx_hashes or len(self.transactions) >= self.max_size:
            return False
        heapq.heappush(self.transactions, (-fee, tx_hash, tx))
        self.tx_hashes.add(tx_hash)
        return True

    def get_top_transactions(self, count: int) -> List[Dict[str, Any]]:
        result = []
        temp = []
        for _ in range(min(count, len(self.transactions))):
            fee, tx_hash, tx = heapq.heappop(self.transactions)
            result.append(tx)
            temp.append((fee, tx_hash, tx))
        for item in temp:
            heapq.heappush(self.transactions, item)
        return result

    def remove_transactions(self, tx_hashes: List[str]) -> None:
        new_txs = []
        for item in self.transactions:
            if item[1] not in tx_hashes:
                new_txs.append(item)
            else:
                self.tx_hashes.discard(item[1])
        self.transactions = new_txs
        heapq.heapify(self.transactions)

    def get_mempool_size(self) -> int:
        return len(self.transactions)

    def clear_mempool(self) -> None:
        self.transactions = []
        self.tx_hashes.clear()
