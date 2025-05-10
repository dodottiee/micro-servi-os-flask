from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    if not os.path.exists('produtos.json'):
        with open('produtos.json', 'w') as f:
            json.dump([], f)

    with open('produtos.json', 'r') as arquivo:
        produtos = json.load(arquivo)

    return jsonify(produtos)


if __name__ == '__main__':
    app.run(port=5001)
