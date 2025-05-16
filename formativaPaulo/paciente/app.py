from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Rota para cadastrar um paciente
@app.route('/pacientes', methods=['POST'])
def cadastrar_paciente():
    dados = request.get_json()
    nome = dados.get('nome')
    idade = dados.get('idade')

    if not nome or idade is None:
        return jsonify({'erro': 'Campos "nome" e "idade" são obrigatórios.'}), 400

    if os.path.exists('pacientes.json'):
        with open('pacientes.json', 'r') as arquivo:
            pacientes = json.load(arquivo)
    else:
        pacientes = []

    novo_id = max([p['id'] for p in pacientes], default=0) + 1
    novo_paciente = {'id': novo_id, 'nome': nome, 'idade': idade}
    pacientes.append(novo_paciente)

    with open('pacientes.json', 'w') as arquivo:
        json.dump(pacientes, arquivo, indent=4)

    return jsonify({'mensagem': 'Paciente cadastrado com sucesso', 'paciente': novo_paciente}), 201

# Rota para listar todos os pacientes
@app.route('/pacientes', methods=['GET'])
def listar_pacientes():
    if os.path.exists('pacientes.json'):
        with open('pacientes.json', 'r') as arquivo:
            pacientes = json.load(arquivo)
    else:
        pacientes = []
    return jsonify(pacientes)

# Rota para obter um paciente por ID
@app.route('/pacientes/<int:id>', methods=['GET'])
def obter_paciente(id):
    if os.path.exists('pacientes.json'):
        with open('pacientes.json', 'r') as arquivo:
            pacientes = json.load(arquivo)
    else:
        pacientes = []

    paciente = next((p for p in pacientes if p['id'] == id), None)
    if paciente:
        return jsonify(paciente)
    else:
        return jsonify({'erro': 'Paciente não encontrado'}), 404

if __name__ == '__main__':
    app.run(port=5001)
