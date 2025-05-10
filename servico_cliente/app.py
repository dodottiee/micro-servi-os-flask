from flask import Flask, request, jsonify

app = Flask(__name__)

# "Banco de dados" em memória
clientes_db = []
proximo_id = 1

# Endpoint para cadastro de cliente
@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    global proximo_id

    dados = request.get_json()
    nome = dados.get('nome')

    # Validação básica
    if not nome:
        return jsonify({'erro': 'O campo "nome" é obrigatório.'}), 400

    novo_cliente = {
        'id': proximo_id,
        'nome': nome
    }

    clientes_db.append(novo_cliente)
    proximo_id += 1

    return jsonify({'mensagem': 'Cliente cadastrado com sucesso', 'cliente': novo_cliente}), 201

# (Opcional) Endpoint para listar clientes cadastrados
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    return jsonify(clientes_db)

if __name__ == '__main__':
    app.run(port=5003)
