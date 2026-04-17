import socket
import threading
import json
from typing import Set, List

class P2PNetwork:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.peers: Set[tuple] = set()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_server(self) -> None:
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"P2P节点启动: {self.host}:{self.port}")
        while True:
            client_sock, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_peer, args=(client_sock, addr)).start()

    def handle_peer(self, client_sock: socket.socket, addr: tuple) -> None:
        self.peers.add(addr)
        try:
            while True:
                data = client_sock.recv(4096)
                if not data:
                    break
                self.broadcast_message(data, addr)
        finally:
            self.peers.remove(addr)
            client_sock.close()

    def connect_to_peer(self, peer_host: str, peer_port: int) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer_host, peer_port))
            self.peers.add((peer_host, peer_port))
            threading.Thread(target=self.listen_peer_messages, args=(sock,)).start()
        except Exception as e:
            print(f"连接节点失败: {e}")

    def broadcast_message(self, message: bytes, exclude_addr: tuple) -> None:
        for peer in self.peers:
            if peer != exclude_addr:
                try:
                    peer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    peer_sock.connect(peer)
                    peer_sock.send(message)
                    peer_sock.close()
                except:
                    continue

    def listen_peer_messages(self, sock: socket.socket) -> None:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            print(f"收到节点消息: {json.loads(data.decode())}")
