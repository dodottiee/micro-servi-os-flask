from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/faturar', methods=['POST'])
def calcular_fatura():
    dados = request.get_json()
    paciente_id = dados.get('paciente_id')
    valor_consulta = dados.get('valor_consulta')
    quantidade = dados.get('quantidade')

    if not paciente_id or not valor_consulta or not quantidade:
        return jsonify({'erro': 'Campos "paciente_id", "valor_consulta" e "quantidade" são obrigatórios.'}), 400

    total = valor_consulta * quantidade

    fatura = {
        'paciente_id': paciente_id,
        'quantidade': quantidade,
        'valor_unitario': valor_consulta,
        'total': total
    }

    return jsonify({'mensagem': 'Fatura gerada com sucesso', 'fatura': fatura}), 200

if __name__ == '__main__':
    app.run(port=5004)
