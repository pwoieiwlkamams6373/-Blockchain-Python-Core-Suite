from typing import Dict, Any, List
import hashlib
import time

class CrossChainBridge:
    def __init__(self, supported_chains: List[str]):
        self.supported_chains = supported_chains
        self.locked_assets: Dict[str, Dict] = {}
        self.wrapped_assets: Dict[str, Dict] = {}
        self.bridge_transactions: List[Dict] = []

    def lock_asset(self, source_chain: str, address: str, asset: str, amount: float) -> str:
        if source_chain not in self.supported_chains:
            return ""
        tx_id = hashlib.sha256(f"{address}{asset}{amount}{time.time()}".encode()).hexdigest()
        self.locked_assets[tx_id] = {
            "chain": source_chain,
            "owner": address,
            "asset": asset,
            "amount": amount,
            "timestamp": time.time()
        }
        self.bridge_transactions.append({"tx_id": tx_id, "type": "lock", "status": "completed"})
        return tx_id

    def mint_wrapped_asset(self, target_chain: str, tx_id: str, address: str) -> bool:
        if tx_id not in self.locked_assets or target_chain not in self.supported_chains:
            return False
        lock_data = self.locked_assets[tx_id]
        self.wrapped_assets[tx_id] = {
            "target_chain": target_chain,
            "owner": address,
            "asset": lock_data["asset"],
            "amount": lock_data["amount"]
        }
        return True

    def unlock_asset(self, tx_id: str) -> bool:
        if tx_id in self.locked_assets and tx_id in self.wrapped_assets:
            del self.wrapped_assets[tx_id]
            return True
        return False

    def get_bridge_status(self) -> Dict[str, Any]:
        return {
            "supported_chains": self.supported_chains,
            "locked_count": len(self.locked_assets),
            "wrapped_count": len(self.wrapped_assets)
        }
