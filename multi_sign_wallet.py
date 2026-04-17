from typing import List, Dict
import hashlib

class MultiSigWallet:
    def __init__(self, owners: List[str], required_signatures: int):
        self.owners = owners
        self.required = required_signatures
        self.transactions: Dict[str, Dict] = {}

    def create_transaction(self, tx_id: str, to_address: str, amount: float, creator: str) -> bool:
        if creator not in self.owners:
            return False
        self.transactions[tx_id] = {
            "to": to_address,
            "amount": amount,
            "signatures": [],
            "executed": False
        }
        return True

    def sign_transaction(self, tx_id: str, signer: str) -> bool:
        if tx_id not in self.transactions or signer not in self.owners:
            return False
        tx = self.transactions[tx_id]
        if signer in tx["signatures"] or tx["executed"]:
            return False
        tx["signatures"].append(signer)
        return True

    def execute_transaction(self, tx_id: str) -> bool:
        if tx_id not in self.transactions:
            return False
        tx = self.transactions[tx_id]
        if len(tx["signatures"]) >= self.required and not tx["executed"]:
            tx["executed"] = True
            return True
        return False

    def get_transaction_status(self, tx_id: str) -> Dict:
        return self.transactions.get(tx_id, {})
