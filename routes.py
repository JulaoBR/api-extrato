# routes.py
from flask import Blueprint, request, jsonify

from controllers.despesa_controller import importar_extrato_cartao

# Criando um Blueprint para as rotas
routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bem-vindo à API Flask! tetse"})

@routes.route('/processar-extrato-cartao', methods=['POST'])
def importar_extrato():
    _request = request

    file = request.files['file']
    novos_dados = importar_extrato_cartao(_request)

    # Exemplo de processamento
    return jsonify({
        'message': 'Arquivo recebido e processado com sucesso!',
        'filename': file.filename,
        'dados': novos_dados
    }), 200