from flask import jsonify
import pandas as pd
from io import StringIO
from types import SimpleNamespace
from datetime import datetime, timedelta, timezone

from models.despesa_model import DespesaModel
from models.despesa_parcela_model import DespesaParcelaModel
from models.cartao_model import CartaoModel
from models.categoria_model import CategoriaModel

from utils.string_utils import remover_acentos, converter_para_minusculas
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

def calcular_vencimento(cartao, usuario, _request):
    mes = _request.args.get('mes', 0)
    ano = _request.args.get('ano', 0)

    dados_cartao = CartaoModel().consultrar(cartao, usuario)
    dia = dados_cartao['diaVencimento']
    if dia < 10:
        dia = str(dia).zfill(2)

    return f"{ano}-{mes}-{dia}"

def associar_categoria(categorias, string):
    string = converter_para_minusculas(remover_acentos(string.strip()))

    # 0 Para categorias nao encontradas
    id_categoria = 0
    for categoria in categorias:
        string_compara = converter_para_minusculas(remover_acentos(f"{categoria.descricao}/{categoria.descricao_extra}"))
        if string in string_compara:
            id_categoria = categoria.idcategoria
            break

    return id_categoria

def importar_extrato_cartao(_request):
    # Verifica se um arquivo foi enviado
    if 'file' not in _request.files:
        return {'error': 'Arquivo não encontrado'}

    cartao = _request.args.get('idcartao', 0)
    usuario = _request.args.get('idusuario', 0)
    mes = _request.args.get('mes', 0)
    ano = _request.args.get('ano', 0)
    dados_objetos = processar_arquivo_extrato_cartao(_request)

    # Definir o fuso horário UTC-3
    fuso_horario = timezone(timedelta(hours=-3))
    data_hora_atual = datetime.now(fuso_horario)

    # Monta data de vencimento com base no mes e ano recebido
    vencimento = calcular_vencimento(cartao, usuario, _request)

    # Carregar as categorias do banco de dados
    _categorias = CategoriaModel().consultrar(usuario)
    categorias = [SimpleNamespace(**item) for item in _categorias]

    novos_dados = []
    # Inicia a transação
    with DespesaModel() as model_despesa, DespesaParcelaModel() as model_parcela:
        for registro in dados_objetos:
            tipo = converter_para_minusculas(remover_acentos(registro.Tipo.strip()))

            if tipo == 'compra a vista':
                iddespesa = model_despesa.inserir({
                    "idusuario": usuario,
                    "idcartao": cartao, 
                    "idcategoria": associar_categoria(categorias, registro.Categoria),
                    "valor": sanitizar_valor(registro.Valor),
                    "descricao": remover_acentos(registro.Lancamento.strip()),
                    "observacao": remover_acentos(f"{registro.Lancamento.strip()} - {registro.Tipo.strip()}"),
                    "dataDespesa": pd.to_datetime(registro.Data, format="%d/%m/%Y").strftime("%Y-%m-%d"),
                    "dataHoraCadastro": data_hora_atual.strftime("%Y-%m-%d %H:%M:%S"),
                    "dataHoraAlteracao": data_hora_atual.strftime("%Y-%m-%d %H:%M:%S")
                })

                model_parcela.inserir({
                    "iddespesa": iddespesa,
                    "numero": '1/1',
                    "valorParcela": sanitizar_valor(registro.Valor),
                    "desconto": 0.00,
                    "acrescimo": 0.00,
                    "dataVencimento": vencimento,
                    "competencia": f"{ano}-{mes}",
                    "status": 0,
                    "evento": 'F'
                })
            
                novos_dados.append(iddespesa)

    return novos_dados