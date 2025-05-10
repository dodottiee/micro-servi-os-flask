# importa o modulo Flask e a função jsonify,
# que converte listas/dicionarios em JSON

from flask import Flask, jsonify

#cria uma instancia da aplicação Flask
app = Flask(__name__)

# lista de produtos simulando um pequeno banco de dados
produtos = [
    {"id": 1, "nome": "notebook", "preco": 3500},
    {"id": 2, "nome": "mouse", "preco": 50},
    {"id": 3, "nome": "teclado", "preco": 100}
]

#define a rota /produtos com o metodo GET para retornar os produtos
@app.route('/produtos')
def listar_produtos():
    return jsonify(produtos) #conveerte a lista para JSON e retorna

#inicia o servidor Flask escutando na porta 5001
if __name__ == '__main__':
    app.run(port=5001)