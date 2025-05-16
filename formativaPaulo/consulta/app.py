from flask import Flask, request, jsonify
import json
import os
import requests
import time

app = Flask(__name__)

# Nome do serviço de pacientes no docker-compose
PACIENTE_SERVICE_URL = 'http://paciente:5001/pacientes'

def buscar_paciente(paciente_id, tentativas=5, intervalo=2):
    """
    Tenta buscar os dados do paciente algumas vezes antes de desistir
    """
    for _ in range(tentativas):
        try:
            resp = requests.get(f'{PACIENTE_SERVICE_URL}/{paciente_id}', timeout=3)
            if resp.status_code == 200:
                return resp.json()
            else:
                return None
        except requests.exceptions.RequestException:
            time.sleep(intervalo)
    return None

@app.route('/consultas', methods=['POST'])
def agendar_consulta():
    dados = request.get_json()
    paciente_id = dados.get('paciente_id')
    data = dados.get('data')

    if not paciente_id or not data:
        return jsonify({'erro': 'Campos "paciente_id" e "data" são obrigatórios.'}), 400

    paciente = buscar_paciente(paciente_id)
    if not paciente:
        return jsonify({'erro': 'Paciente não encontrado ou serviço indisponível'}), 503

    if os.path.exists('consultas.json'):
        with open('consultas.json', 'r') as arquivo:
            consultas = json.load(arquivo)
    else:
        consultas = []

    nova_consulta = {
        'id': len(consultas) + 1,
        'paciente_id': paciente_id,
        'data': data
    }

    consultas.append(nova_consulta)

    with open('consultas.json', 'w') as arquivo:
        json.dump(consultas, arquivo, indent=4)

    return jsonify({'mensagem': 'Consulta agendada com sucesso', 'consulta': nova_consulta}), 201

@app.route('/consultas', methods=['GET'])
def listar_consultas():
    if os.path.exists('consultas.json'):
        with open('consultas.json', 'r') as arquivo:
            consultas = json.load(arquivo)
    else:
        consultas = []

    consultas_com_paciente = []
    for consulta in consultas:
        paciente = buscar_paciente(consulta['paciente_id'])
        if not paciente:
            paciente = {'erro': 'Paciente não encontrado ou serviço indisponível'}

        consulta_completa = {
            'id': consulta['id'],
            'data': consulta['data'],
            'paciente': paciente
        }
        consultas_com_paciente.append(consulta_completa)

    return jsonify(consultas_com_paciente)

if __name__ == '__main__':
    app.run(port=5002)
