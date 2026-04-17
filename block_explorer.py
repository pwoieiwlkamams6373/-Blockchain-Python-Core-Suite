from typing import List, Dict, Any, Optional

class BlockExplorer:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def get_block_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        if 0 <= index < len(self.blockchain.chain):
            return self.blockchain.chain[index]
        return None

    def get_block_by_hash(self, block_hash: str) -> Optional[Dict[str, Any]]:
        for block in self.blockchain.chain:
            if self.blockchain.hash_block(block) == block_hash:
                return block
        return None

    def search_transaction(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        for block in self.blockchain.chain:
            for tx in block["transactions"]:
                if tx.get("tx_hash") == tx_hash:
                    return tx
        return None

    def get_address_transactions(self, address: str) -> List[Dict[str, Any]]:
        tx_list = []
        for block in self.blockchain.chain:
            for tx in block["transactions"]:
                if tx["sender"] == address or tx["recipient"] == address:
                    tx_list.append(tx)
        return tx_list

    def get_address_balance(self, address: str) -> float:
        balance = 0.0
        for block in self.blockchain.chain:
            for tx in block["transactions"]:
                if tx["recipient"] == address:
                    balance += tx["amount"]
                if tx["sender"] == address:
                    balance -= tx["amount"]
        return balance
