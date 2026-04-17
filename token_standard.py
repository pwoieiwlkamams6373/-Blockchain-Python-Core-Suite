from dataclasses import dataclass
from typing import Dict

@dataclass
class BlockchainToken:
    name: str
    symbol: str
    total_supply: float
    decimals: int
    balances: Dict[str, float]

    def __init__(self, name: str, symbol: str, total_supply: float, decimals: int = 18):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.decimals = decimals
        self.balances = {}
        self.balances["owner"] = total_supply

    def transfer(self, sender: str, recipient: str, amount: float) -> bool:
        if self.balances.get(sender, 0) < amount or amount <= 0:
            return False
        self.balances[sender] -= amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount
        return True

    def balance_of(self, address: str) -> float:
        return self.balances.get(address, 0)

    def mint(self, to_address: str, amount: float) -> None:
        if amount <= 0:
            return
        self.total_supply += amount
        self.balances[to_address] = self.balances.get(to_address, 0) + amount

    def burn(self, from_address: str, amount: float) -> bool:
        if self.balances.get(from_address, 0) < amount or amount <= 0:
            return False
        self.balances[from_address] -= amount
        self.total_supply -= amount
        return True
