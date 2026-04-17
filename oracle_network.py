from typing import Dict, Any, List
import requests
import time

class BlockchainOracle:
    def __init__(self, node_address: str):
        self.node = node_address
        self.data_sources: Dict[str, str] = {}
        self.cached_data: Dict[str, Dict] = {}

    def register_data_source(self, source_name: str, api_url: str) -> None:
        self.data_sources[source_name] = api_url

    def fetch_external_data(self, source_name: str) -> Dict[str, Any]:
        if source_name not in self.data_sources:
            return {}
        try:
            response = requests.get(self.data_sources[source_name])
            data = response.json()
            self.cached_data[source_name] = {
                "data": data,
                "timestamp": time.time()
            }
            return data
        except:
            return self.cached_data.get(source_name, {}).get("data", {})

    def get_cached_data(self, source_name: str) -> Dict[str, Any]:
        return self.cached_data.get(source_name, {}).get("data", {})

    def submit_data_to_chain(self, contract_address: str, data: Dict[str, Any]) -> bool:
        try:
            payload = {
                "oracle": self.node,
                "data": data,
                "timestamp": time.time()
            }
            return True
        except:
            return False

    def list_supported_sources(self) -> List[str]:
        return list(self.data_sources.keys())
