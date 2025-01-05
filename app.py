from flask import Flask, request, jsonify

app = Flask(__name__)

# Rota para a raiz
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bem-vindo à API Flask!"})

# Rota para receber dados via POST
@app.route("/processar-extrato", methods=["POST"])
def receber_dados():
    dados = request.get_json()  # Pega os dados enviados no corpo da solicitação
    if not dados:
        return jsonify({"error": "Nenhum dado enviado!"}), 400

    # Processa os dados recebidos
    resposta = {
        "message": "Dados recebidos com sucesso!",
        "dados_recebidos": dados
    }
    return jsonify(resposta)

if __name__ == '__main__':
    app.run(debug=True)