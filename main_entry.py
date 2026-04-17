from blockchain_core import BlockchainCore
from crypto_wallet import CryptoWallet
from block_miner import BlockMiner
from chain_verifier import ChainVerifier
from p2p_network import P2PNetwork

def main():
    print("=== 区块链项目主程序启动 ===")
    
    # 初始化核心组件
    blockchain = BlockchainCore()
    wallet = CryptoWallet()
    wallet.generate_key_pair()
    miner = BlockMiner(blockchain)
    verifier = ChainVerifier(blockchain)
    
    # 创建测试钱包
    user_wallet = CryptoWallet()
    user_wallet.generate_key_pair()
    
    # 发起交易
    blockchain.add_transaction(
        sender=wallet.address,
        recipient=user_wallet.address,
        amount=5.0
    )
    
    # 挖矿打包
    new_block = miner.mine_pending_transactions(wallet.address)
    print(f"新区块已挖出: {new_block['index']}")
    
    # 验证链完整性
    is_valid = verifier.verify_chain_integrity()
    print(f"区块链状态: {'有效' if is_valid else '异常'}")
    
    # 启动P2P节点
    p2p = P2PNetwork("127.0.0.1", 6000)
    print("P2P网络节点已就绪")
    print("=== 主程序初始化完成 ===")

if __name__ == "__main__":
    main()
