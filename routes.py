# routes.py
from flask import Blueprint, request, jsonify

from controllers.despesa_controller import importar_extrato_cartao

from utils.csv_validation_utils import validar_csv_import_cartao

# Criando um Blueprint para as rotas
routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bem-vindo à API Flask!"})

@routes.route('/processar-extrato-cartao', methods=['POST'])
def importar_extrato():
    if 'file' not in request.files:
        return jsonify({'error': "Nenhum arquivo enviado."}), 400

    file = request.files['file']

    resultado_validacao = validar_csv_import_cartao(file)
    if not resultado_validacao.is_valid():
        return jsonify({'error': resultado_validacao.get_error()}), 400

    resultado_importacao = importar_extrato_cartao(
        resultado_validacao.dataframe, file, request.args
    )
    if not resultado_importacao.get("success", False):
        return jsonify({'error': resultado_importacao.get("error", "Erro ao importar dados.")}), 500

    return jsonify({
        'success': f"Arquivo {file.filename} recebido e processado com sucesso!",
    }), 200