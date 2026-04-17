from typing import Dict, Any, Callable
from dataclasses import dataclass

@dataclass
class SmartContract:
    contract_address: str
    owner_address: str
    state: Dict[str, Any]
    functions: Dict[str, Callable]

    def __init__(self, contract_address: str, owner_address: str):
        self.contract_address = contract_address
        self.owner_address = owner_address
        self.state = {}
        self.functions = {}

    def register_function(self, func_name: str, func: Callable) -> None:
        self.functions[func_name] = func

    def execute_function(self, func_name: str, caller: str, *args, **kwargs) -> Any:
        if func_name not in self.functions:
            raise Exception("函数不存在")
        if caller != self.owner_address and func_name in ["update_state", "delete_state"]:
            raise Exception("无执行权限")
        return self.functions[func_name](self, *args, **kwargs)

    def update_state(self, key: str, value: Any) -> None:
        self.state[key] = value

    def get_state(self, key: str) -> Any:
        return self.state.get(key, None)

    def delete_state(self, key: str) -> None:
        if key in self.state:
            del self.state[key]
