from flask import Flask, jsonify, request
from blockchain_core import BlockchainCore

app = Flask(__name__)
blockchain = BlockchainCore()

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }), 200

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return jsonify({"error": "参数缺失"}), 400
    index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])
    return jsonify({"message": f"交易将加入区块 {index}"}), 201

@app.route('/mine', methods=['GET'])
def mine():
    from block_miner import BlockMiner
    miner = BlockMiner(blockchain)
    new_block = miner.mine_pending_transactions("miner_node")
    return jsonify(new_block), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    return jsonify({"message": "节点注册成功"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
