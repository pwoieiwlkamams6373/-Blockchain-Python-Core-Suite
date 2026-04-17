from typing import List, Dict, Any

class ConsensusAlgorithm:
    def __init__(self, blockchain, nodes: List[str]):
        self.blockchain = blockchain
        self.nodes = nodes

    def proof_of_stake(self, validators: List[str], stakes: Dict[str, float]) -> str:
        total_stake = sum(stakes.values())
        if total_stake == 0:
            return validators[0] if validators else None
        
        import random
        rand = random.uniform(0, total_stake)
        current = 0
        for validator, stake in stakes.items():
            current += stake
            if current >= rand:
                return validator
        return validators[0]

    def resolve_conflicts(self) -> bool:
        new_chain = None
        max_length = len(self.blockchain.chain)

        for node in self.nodes:
            response = self._get_node_chain(node)
            if response:
                length = response["length"]
                chain = response["chain"]
                if length > max_length and self._verify_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.blockchain.chain = new_chain
            return True
        return False

    def _get_node_chain(self, node: str) -> Dict[str, Any]:
        import requests
        try:
            response = requests.get(f"http://{node}/chain")
            if response.status_code == 200:
                return response.json()
        except:
            return None

    def _verify_chain(self, chain: List[Dict[str, Any]]) -> bool:
        for i in range(1, len(chain)):
            if chain[i]["previous_hash"] != self._hash(chain[i-1]):
                return False
        return True

    def _hash(self, block: Dict[str, Any]) -> str:
        import hashlib, json
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
