from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/produtos', methods=['POST'])
def cadastrar_produto():
    dados = request.get_json()
    nome = dados.get('nome')
    preco = dados.get('preco')

    if not nome or preco is None:
        return jsonify({'erro': 'Campos "nome" e "preco" são obrigatórios.'}), 400

    # Lê os produtos existentes
    if os.path.exists('produtos.json'):
        with open('produtos.json', 'r') as arquivo:
            produtos = json.load(arquivo)
    else:
        produtos = []

    novo_id = max([p['id'] for p in produtos], default=0) + 1

    novo_produto = {
        'id': novo_id,
        'nome': nome,
        'preco': preco
    }

    produtos.append(novo_produto)

    with open('produtos.json', 'w') as arquivo:
        json.dump(produtos, arquivo, indent=4)

    return jsonify({'mensagem': 'Produto cadastrado com sucesso', 'produto': novo_produto}), 201

if __name__ == '__main__':
    app.run(port=5004)
