# routes.py
from flask import Blueprint, request, jsonify

# Criando um Blueprint para as rotas
routes = Blueprint('routes', __name__)

@routes.route('/',methods=['GET'])
def home():
    return jsonify({"message": "Bem-vindo à API Flask! tetse"})

@routes.route('/processar-extrato')
def processar_arquivo():
    dados = request.get_json()  # Pega os dados enviados no corpo da solicitação
    if not dados:
        return jsonify({"error": "Nenhum dado enviado!"}), 400

    # Processa os dados recebidos
    resposta = {
        "message": "Dados recebidos com sucesso!",
        "dados_recebidos": dados
    }
    return jsonify(resposta)