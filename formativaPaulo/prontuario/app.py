from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/prontuarios', methods=['POST'])
def adicionar_registro():
    dados = request.get_json()
    paciente_id = dados.get('paciente_id')
    descricao = dados.get('descricao')

    if not paciente_id or not descricao:
        return jsonify({'erro': 'Campos "paciente_id" e "descricao" são obrigatórios.'}), 400

    if os.path.exists('prontuarios.json'):
        with open('prontuarios.json', 'r') as arquivo:
            registros = json.load(arquivo)
    else:
        registros = []

    novo_registro = {
        'id': len(registros) + 1,
        'paciente_id': paciente_id,
        'descricao': descricao
    }

    registros.append(novo_registro)

    with open('prontuarios.json', 'w') as arquivo:
        json.dump(registros, arquivo, indent=4)

    return jsonify({'mensagem': 'Registro adicionado', 'registro': novo_registro}), 201

@app.route('/prontuarios/<int:paciente_id>', methods=['GET'])
def obter_registros(paciente_id):
    if os.path.exists('prontuarios.json'):
        with open('prontuarios.json', 'r') as arquivo:
            registros = json.load(arquivo)
    else:
        registros = []

    registros_paciente = [r for r in registros if r['paciente_id'] == paciente_id]
    return jsonify(registros_paciente)

if __name__ == '__main__':
    app.run(port=5003)
