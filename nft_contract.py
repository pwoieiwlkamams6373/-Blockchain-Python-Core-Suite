from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class NFTItem:
    token_id: str
    owner: str
    metadata_uri: str
    created_at: float

class NFTContract:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.nfts: Dict[str, NFTItem] = {}
        self.balances: Dict[str, int] = {}

    def mint_nft(self, token_id: str, owner: str, metadata_uri: str) -> bool:
        if token_id in self.nfts:
            return False
        self.nfts[token_id] = NFTItem(
            token_id=token_id,
            owner=owner,
            metadata_uri=metadata_uri,
            created_at=self._get_time()
        )
        self.balances[owner] = self.balances.get(owner, 0) + 1
        return True

    def transfer_nft(self, token_id: str, from_addr: str, to_addr: str) -> bool:
        if token_id not in self.nfts or self.nfts[token_id].owner != from_addr:
            return False
        self.nfts[token_id].owner = to_addr
        self.balances[from_addr] -= 1
        self.balances[to_addr] = self.balances.get(to_addr, 0) + 1
        return True

    def get_owner(self, token_id: str) -> Optional[str]:
        return self.nfts[token_id].owner if token_id in self.nfts else None

    def get_nft_metadata(self, token_id: str) -> Optional[str]:
        return self.nfts[token_id].metadata_uri if token_id in self.nfts else None

    def balance_of(self, owner: str) -> int:
        return self.balances.get(owner, 0)

    def _get_time(self) -> float:
        import time
        return time.time()
