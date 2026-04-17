from typing import Dict, Any, List
import time
import threading

class NodeMonitor:
    def __init__(self, node_address: str):
        self.node = node_address
        self.metrics = {
            "block_height": 0,
            "peer_count": 0,
            "tx_pending": 0,
            "uptime": 0,
            "last_check": 0
        }
        self.start_time = time.time()
        self.alerts = []

    def update_metrics(self, blockchain, p2p_network) -> None:
        self.metrics["block_height"] = len(blockchain.chain)
        self.metrics["peer_count"] = len(p2p_network.peers)
        self.metrics["tx_pending"] = len(blockchain.pending_transactions)
        self.metrics["uptime"] = time.time() - self.start_time
        self.metrics["last_check"] = time.time()

    def start_background_monitor(self, blockchain, p2p_network):
        def monitor_loop():
            while True:
                self.update_metrics(blockchain, p2p_network)
                self.check_health()
                time.sleep(10)
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()

    def check_health(self) -> bool:
        healthy = True
        if self.metrics["tx_pending"] > 500:
            self.alerts.append({"level": "high", "msg": "交易池拥堵", "time": time.time()})
            healthy = False
        if self.metrics["peer_count"] < 3:
            self.alerts.append({"level": "medium", "msg": "节点连接数过低", "time": time.time()})
            healthy = False
        return healthy

    def get_node_status(self) -> Dict[str, Any]:
        return {
            "node": self.node,
            "metrics": self.metrics,
            "health": self.check_health(),
            "alerts": self.alerts[-5:]
        }
