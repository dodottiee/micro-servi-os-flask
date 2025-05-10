from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
pedidos = []

@app.route('/pedido', methods=['POST'])
def novo_pedido():
    dados = request.json
    id_produto = dados.get('id_produto')

    resposta = requests.get('http://localhost:5001/produtos')
    lista_produtos = resposta.json()

    produto = next((p for p in lista_produtos if p['id'] == id_produto), None)
    
    # se o produto não for encontrado, retorna erro 404
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    
    #cria um novo pedido com o nome e preço do produto
    pedido = {
        "produto": produto['nome'],
        "valor": produto['preco']
    }
    pedidos.append(pedido) # adiciona o pedido a lista
    
    # retorna o pedido criado com status HTTP 201 (criado)
    return jsonify(pedido), 201

#define uma rota GET para listar todos os pedidos
@app.route('/pedidos')
def listar_pedidos():
    return jsonify(pedidos)

#inicia o servidor Flask escutando na porta 5002
if __name__ == '__main__':
    app.run(port=5002)
    




