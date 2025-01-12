from datetime import datetime, timedelta, timezone

def converter_para_data(data_str, formato="%d/%m/%Y"):
    return datetime.strptime(data_str, formato)

def formatar_data(data, formato="%d/%m/%Y"):
    return data.strftime(formato)

def obter_data_hora_atual(formato="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(formato)

def adicionar_dias(data, dias):
    return data + timedelta(days=dias)

def subtrair_dias(data, dias):
    return data - timedelta(days=dias)

def diferenca_entre_datas(data1, data2):
    return (data2 - data1).days

def eh_data_futura(data):
    return data > datetime.now()

def primeiro_dia_do_mes(data):
    return data.replace(day=1)

def calcular_idade(data_nascimento):
    hoje = datetime.today()
    idade = hoje.year - data_nascimento.year
    if hoje.month < data_nascimento.month or (hoje.month == data_nascimento.month and hoje.day < data_nascimento.day):
        idade -= 1
    return idade

def eh_ano_bissexto(ano):
    return (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0)