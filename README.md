# Blockchain-Python-Core-Suite
一站式区块链开发工具集，基于 Python 构建，包含底层链核心、加密钱包、共识算法、智能合约、Layer2、跨链桥、NFT、DAO 等全场景模块，支持生产级区块链项目快速开发与部署。

## 项目特性
- 完整区块链底层核心与挖矿机制
- 加密钱包、多重签名、零知识证明安全组件
- P2P 网络、节点监控、交易池、区块浏览器
- 智能合约基础框架 + Token/NFT 标准
- DAO 治理、质押挖矿、预言机、Layer2 扩容
- 跨链桥、数据加密、链上数据存储模拟
- 开箱即用、模块化、可直接扩展

## 文件清单与功能说明
1. **blockchain_core.py** - 区块链核心类，实现区块结构、链式结构、交易管理、工作量证明
2. **crypto_wallet.py** - 加密钱包，生成公私钥对、地址、签名与验签功能
3. **p2p_network.py** - P2P 去中心化网络，节点发现、消息广播、连接管理
4. **smart_contract_base.py** - 智能合约基础框架，支持函数注册、权限控制、状态管理
5. **transaction_validator.py** - 交易验证器，校验结构、哈希、余额、签名合法性
6. **block_miner.py** - 区块挖矿工具，打包待处理交易、执行共识、发放矿工奖励
7. **chain_verifier.py** - 链完整性校验，检测分叉、篡改，输出链健康报告
8. **token_standard.py** - 同质化代币标准，支持转账、铸造、销毁、余额查询
9. **ipfs_storage_sim.py** - 去中心化存储模拟器，实现 CID 计算、上传、获取、删除
10. **consensus_algorithm.py** - 共识算法模块，支持 PoS 与最长链冲突解决
11. **block_explorer.py** - 区块浏览器，按高度/哈希查询、地址交易与余额统计
12. **merkle_tree.py** - 默克尔树实现，交易哈希构建、根计算、存在性证明
13. **multi_sign_wallet.py** - 多重签名钱包，支持多管理员签名、交易执行控制
14. **blockchain_api_server.py** - 区块链 REST API 服务，提供链查询、交易、挖矿接口
15. **staking_pool.py** - 质押池，支持代币质押、收益计算、自动复利、锁仓解锁
16. **cross_chain_bridge.py** - 跨链桥，支持资产锁定、跨链铸造、跨链赎回
17. **dao_governance.py** - DAO 治理系统，创建提案、代币投票、提案终审
18. **zero_knowledge_proof.py** - 零知识证明，匿名验证所有权、不泄露原始数据
19. **oracle_network.py** - 预言机网络，对接外部 API、链下数据上链、缓存管理
20. **layer2_scaling.py** - Layer2  Rollup 扩容，批量交易打包、提交到 Layer1
21. **nft_contract.py** - NFT 合约标准，支持铸造、转让、元数据、余额查询
22. **transaction_mempool.py** - 交易内存池，按手续费排序、批量提取、清理
23. **block_data_encrypt.py** - 区块数据加密，AES 加密区块、哈希校验、解密还原
24. **node_monitor.py** - 节点监控，实时采集指标、健康检查、异常告警
25. **main_entry.py** - 项目主入口，集成所有模块，快速启动测试与演示

## 快速启动
```bash
# 安装依赖
pip install flask ecdsa cryptography requests

# 启动主程序
python main_entry.py

# 启动 API 服务
python blockchain_api_server.py
