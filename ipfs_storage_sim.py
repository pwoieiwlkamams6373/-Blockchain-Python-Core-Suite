import hashlib
import json
from typing import Dict, Any

class IPFSSimulator:
    def __init__(self):
        self.storage: Dict[str, Dict[str, Any]] = {}

    def calculate_cid(self, data: Any) -> str:
        data_str = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(data_str).hexdigest()

    def upload_data(self, data: Any) -> str:
        cid = self.calculate_cid(data)
        self.storage[cid] = {
            "data": data,
            "size": len(json.dumps(data).encode()),
            "timestamp": self._get_timestamp()
        }
        return cid

    def get_data(self, cid: str) -> Any:
        return self.storage.get(cid, {}).get("data", None)

    def delete_data(self, cid: str) -> bool:
        if cid in self.storage:
            del self.storage[cid]
            return True
        return False

    def get_storage_info(self) -> Dict[str, int]:
        total_size = sum([item["size"] for item in self.storage.values()])
        return {
            "total_files": len(self.storage),
            "total_storage_bytes": total_size
        }

    def _get_timestamp(self) -> float:
        from time import time
        return time()
