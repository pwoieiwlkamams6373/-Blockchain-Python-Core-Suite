from typing import Dict, List
from dataclasses import dataclass

@dataclass
class StakingPool:
    apy: float
    min_stake: float
    lock_period: int
    stakes: Dict[str, float]
    rewards: Dict[str, float]

    def __init__(self, apy: float, min_stake: float, lock_period: int):
        self.apy = apy
        self.min_stake = min_stake
        self.lock_period = lock_period
        self.stakes = {}
        self.rewards = {}
        self.stake_start_time = {}

    def stake_tokens(self, address: str, amount: float, current_time: int) -> bool:
        if amount < self.min_stake:
            return False
        self.stakes[address] = self.stakes.get(address, 0) + amount
        if address not in self.stake_start_time:
            self.stake_start_time[address] = current_time
        return True

    def calculate_rewards(self, address: str, current_time: int) -> float:
        if address not in self.stakes:
            return 0.0
        time_elapsed = current_time - self.stake_start_time[address]
        if time_elapsed < self.lock_period:
            return 0.0
        stake_amount = self.stakes[address]
        reward = stake_amount * self.apy * (time_elapsed / 365)
        return round(reward, 4)

    def claim_rewards(self, address: str, current_time: int) -> float:
        reward = self.calculate_rewards(address, current_time)
        if reward > 0:
            self.rewards[address] = self.rewards.get(address, 0) + reward
            self.stake_start_time[address] = current_time
        return reward

    def unstake(self, address: str, current_time: int) -> float:
        if current_time - self.stake_start_time.get(address, 0) < self.lock_period:
            return 0.0
        amount = self.stakes.pop(address, 0.0)
        self.stake_start_time.pop(address, None)
        return amount
