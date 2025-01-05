# routes.py
from flask import Blueprint, request, jsonify
import pandas as pd
from io import StringIO

# Criando um Blueprint para as rotas
routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bem-vindo à API Flask! tetse"})

# Função para sanitizar valores monetários
def sanitizar_valor(valor):
    if isinstance(valor, str):  # Verifica se é uma string
        valor = valor.replace("R$", "").replace("\u00a0", "").replace(".", "").replace(",", ".").strip()
        return float(valor)
    return valor

@routes.route('/processar-extrato', methods=['POST'])
def processar_arquivo():
     # Verifica se um arquivo foi enviado
    if 'file' not in request.files:
        return jsonify({'error': 'Arquivo não encontrado'}), 400

    file = request.files['file']  # O arquivo enviado

    # Lê o arquivo como texto
    file_data = file.stream.read().decode('utf-8')

    # Converte para um DataFrame usando pandas
    csv_data = pd.read_csv(StringIO(file_data))

     # Sanitiza a coluna "Valor" (ou a coluna que você precisa)
    if 'Valor' in csv_data.columns:
        csv_data['Valor'] = csv_data['Valor'].apply(sanitizar_valor)

    # Exemplo: Retorna as 5 primeiras linhas do CSV em JSON
    data_csv = csv_data.to_dict(orient='records')

    # Exemplo de processamento
    return jsonify({
        'message': 'Arquivo recebido e processado com sucesso!',
        'filename': file.filename,
        'dados': data_csv
    }), 200