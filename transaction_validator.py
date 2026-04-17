import hashlib
import json
from typing import Dict, Any

class TransactionValidator:
    @staticmethod
    def validate_transaction_structure(transaction: Dict[str, Any]) -> bool:
        required_fields = ["sender", "recipient", "amount", "timestamp", "signature"]
        for field in required_fields:
            if field not in transaction:
                return False
        if not isinstance(transaction["amount"], (int, float)) or transaction["amount"] <= 0:
            return False
        return True

    @staticmethod
    def validate_transaction_hash(transaction: Dict[str, Any]) -> bool:
        tx_copy = transaction.copy()
        tx_signature = tx_copy.pop("signature", None)
        tx_string = json.dumps(tx_copy, sort_keys=True).encode()
        calculated_hash = hashlib.sha256(tx_string).hexdigest()
        return calculated_hash == transaction.get("tx_hash", "")

    @staticmethod
    def validate_balance(balance: float, amount: float) -> bool:
        return balance >= amount

    @staticmethod
    def full_transaction_check(transaction: Dict[str, Any], sender_balance: float) -> bool:
        if not TransactionValidator.validate_transaction_structure(transaction):
            return False
        if not TransactionValidator.validate_transaction_hash(transaction):
            return False
        if not TransactionValidator.validate_balance(sender_balance, transaction["amount"]):
            return False
        return True
