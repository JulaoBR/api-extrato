from flask import jsonify
import pandas as pd
from io import StringIO
from types import SimpleNamespace
from datetime import datetime, timedelta, timezone

from models.despesa_model import DespesaModel
from models.despesa_model import DespesaModel
from models.despesa_parcela_model import DespesaParcelaModel

from utils.string_utils import remover_acentos
from utils.number_utils import sanitizar_valor

def processar_arquivo_extrato_cartao(_request):
    file = _request.files['file']  # O arquivo enviado

    # Lê o arquivo como texto
    file_data = file.stream.read().decode('utf-8')

    # Converte para um DataFrame usando pandas
    csv_data = pd.read_csv(StringIO(file_data))

    # Remover acentos nos nomes das colunas
    csv_data.columns = [remover_acentos(coluna) for coluna in csv_data.columns]

    data_csv = csv_data.to_dict(orient='records')

    # Converte o dicionario para uma lista de objeto
    dados_objetos = [SimpleNamespace(**registro) for registro in data_csv]

    return dados_objetos
    

def importar_extrato_cartao(_request):
    # Verifica se um arquivo foi enviado
    if 'file' not in _request.files:
        return {'error': 'Arquivo não encontrado'}

    cartao = _request.args.get('idcartao', 0)
    usuario = _request.args.get('idusuario', 0)
    dados_objetos = processar_arquivo_extrato_cartao(_request)

    # Definir o fuso horário UTC-3
    fuso_horario = timezone(timedelta(hours=-3))
    data_hora_atual = datetime.now(fuso_horario)

    novos_dados = []
    for registro in dados_objetos:
        iddespesa = DespesaModel.inserir({
            "idusuario": usuario,
            "idcartao": cartao, 
            "idcategoria": 52,
            "valor": sanitizar_valor(registro.Valor),
            "descricao": remover_acentos(registro.Lancamento.strip()),
            "observacao": remover_acentos(f"{registro.Lancamento.strip()} - {registro.Tipo.strip()}"),
            "dataDespesa": pd.to_datetime(registro.Data, format="%d/%m/%Y").strftime("%Y-%m-%d"),
            "dataHoraCadastro": data_hora_atual.strftime("%Y-%m-%d %H:%M:%S"),
            "dataHoraAlteracao": data_hora_atual.strftime("%Y-%m-%d %H:%M:%S")
        })

        DespesaParcelaModel.inserir({
            "iddespesa": iddespesa,
            "numero": '1/1',
            "valorParcela": sanitizar_valor(registro.Valor),
            "desconto": 0.00,
            "acrescimo": 0.00,
            "dataVencimento": pd.to_datetime(registro.Data, format="%d/%m/%Y").strftime("%Y-%m-%d"),
            "dataPagamento": pd.to_datetime(registro.Data, format="%d/%m/%Y").strftime("%Y-%m-%d"),
            "competencia": '',
            "status": 0,
            "evento": 'F'
        })
    
        # Adicionar o novo dicionário na lista
        novos_dados.append(iddespesa)

    return novos_dados