from flask import jsonify
import pandas as pd
from io import StringIO
from types import SimpleNamespace
from datetime import datetime, timedelta, timezone

from models.despesa_model import DespesaModel
from models.despesa_parcela_model import DespesaParcelaModel
from models.cartao_model import CartaoModel
from models.categoria_model import CategoriaModel
from models.importacao_documento_model import ImporteDocumentoModel

from utils.string_utils import remover_acentos, converter_para_minusculas
from utils.number_utils import sanitizar_valor

def processar_arquivo_extrato_cartao(dataframe):
    # Remover acentos nos nomes das colunas
    dataframe.columns = [remover_acentos(coluna) for coluna in dataframe.columns]

    data_csv = dataframe.to_dict(orient='records')

    # Converte o dicionario para uma lista de objeto
    dados_objetos = [SimpleNamespace(**registro) for registro in data_csv]

    return dados_objetos

def calcular_vencimento(form_data):
    cartao = form_data.get('idcartao', 0)
    usuario = form_data.get('idusuario', 0)
    mes = form_data.get('mes', 0)
    ano = form_data.get('ano', 0)

    with CartaoModel() as model_cartao:
        dados_cartao = model_cartao.consultrar(cartao, usuario)
        dia = dados_cartao['diaVencimento']
        if dia < 10:
            dia = str(dia).zfill(2)
    return f"{ano}-{mes}-{dia}"

def associar_categoria(categorias, descricao_extrato, categoria_extrato):
    # 0 Para categorias nao encontradas
    id_categoria = 0

    # Compara a descricao do extrato com os campos extra de comparacao da categoria
    for item in categorias:
        if not item.descricao_extra:
            continue

        descricao_extra_normalizada = converter_para_minusculas(item.descricao_extra)
        descricao_extra_normalizada = descricao_extra_normalizada.split()
        # Verifica se alguma palavra do extrato está na descrição_extra
        if any(palavra in descricao_extrato for palavra in descricao_extra_normalizada):
            id_categoria = item.idcategoria
            break

    # Compara a categoria do extrato com a categoria + campos extras de comparacao da categoria
    if id_categoria == 0:
        for item in categorias:
            if not item.descricao_extra:
                continue

            descricao_extra_normalizada = converter_para_minusculas(remover_acentos(f"{item.descricao} {item.descricao_extra}"))
            descricao_extra_normalizada = descricao_extra_normalizada.split()
            if any(palavra in categoria_extrato for palavra in descricao_extra_normalizada):
                id_categoria = item.idcategoria
                break

    return id_categoria

def importar_extrato_cartao(dataframe, file, form_data):
    cartao = form_data.get('idcartao', 0)
    usuario = form_data.get('idusuario', 0)
    mes = form_data.get('mes', 0)
    ano = form_data.get('ano', 0)

    # Processa o arquivo
    dados_objetos = processar_arquivo_extrato_cartao(dataframe)

    # Definir o fuso horário UTC-3
    fuso_horario = timezone(timedelta(hours=-3))
    data_hora_atual = datetime.now(fuso_horario)

    # Monta data de vencimento com base no mes e ano recebido
    vencimento = calcular_vencimento(form_data)

    # Carregar as categorias do banco de dados
    with CategoriaModel() as model_categoria:
        _categorias = model_categoria.consultrar(usuario)
        categorias = [SimpleNamespace(**item) for item in _categorias]

    try:
        # Inicia a transação
        with DespesaModel() as model_despesa, DespesaParcelaModel() as model_parcela, ImporteDocumentoModel() as model_importe:
            idimportacao = salvar_arquivo_csv(file, usuario, cartao, data_hora_atual, model_importe)

            for registro in dados_objetos:
                tipo = converter_para_minusculas(remover_acentos(registro.Tipo.strip()))
                valor = sanitizar_valor(registro.Valor)

                descricao = converter_para_minusculas(remover_acentos(registro.Lancamento.strip()))
                categoria = converter_para_minusculas(remover_acentos(registro.Categoria.strip()))

                if tipo == 'compra a vista' and valor >= 0:
                    iddespesa = model_despesa.inserir({
                        "idusuario": usuario,
                        "idcartao": cartao, 
                        "idcategoria": associar_categoria(categorias, descricao, categoria),
                        "idimportacao": idimportacao,
                        "valor": valor,
                        "descricao": descricao,
                        "observacao": remover_acentos(f"{descricao} - {registro.Tipo.strip()}"),
                        "dataDespesa": pd.to_datetime(registro.Data, format="%d/%m/%Y").strftime("%Y-%m-%d"),
                        "dataHoraCadastro": data_hora_atual.strftime("%Y-%m-%d %H:%M:%S"),
                        "dataHoraAlteracao": data_hora_atual.strftime("%Y-%m-%d %H:%M:%S")
                    })

                    model_parcela.inserir({
                        "iddespesa": iddespesa,
                        "numero": '1/1',
                        "valorParcela": valor,
                        "desconto": 0.00,
                        "acrescimo": 0.00,
                        "dataVencimento": vencimento,
                        "competencia": f"{ano}-{mes}",
                        "status": 0,
                        "evento": 'F'
                    })
                
    except Exception as e:
        return {"error": f"Erro ao processar CSV: {str(e)}"}

    return {'success': True}

def salvar_arquivo_csv(file, usuario, cartao, data_hora_atual, conexao):
    try:
        # Capturar os dados do arquivo
        nome_arquivo = file.filename
        tipo_arquivo = file.content_type
        tamanho_arquivo = len(file.read())

        # Resetar o cursor do arquivo para poder ler de novo
        file.stream.seek(0)
        conteudo = file.read()  # Lê o arquivo como bytes

        idimportacao = conexao.inserir({
            "idusuario": usuario,
            "idcartao": cartao,
            "idconta": 0,
            "nome_arquivo": nome_arquivo,
            "tipo_arquivo": tipo_arquivo,
            "tamanho_arquivo": tamanho_arquivo,
            "arquivo": conteudo,
            "dataHoraCadastro": data_hora_atual.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        return idimportacao
    
    except Exception as e:
        return {"error": f"Erro ao inserir documento: {str(e)}"}