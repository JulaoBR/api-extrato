
def arredondar(numero, casas_decimais=2):
    return round(numero, casas_decimais)

def para_percentual(numero):
    return numero * 100

def formatar_moeda(valor, simbolo="R$", casas_decimais=2):
    return f"{simbolo} {valor:,.{casas_decimais}f}"

def calcular_juros_compostos(valor_inicial, taxa_juros, periodo):
    return valor_inicial * (1 + taxa_juros / 100) ** periodo

def transformar_valor_bra_to_eua(valor_real, decimal=2):
    valor_americano = float(valor_real.replace('.', '').replace(',', '.'))
    return round(valor_americano, decimal)

def transformar_valor_eua_to_bra(valor_americano, decimal=2):
    valor_formatado = f"{valor_americano:,.{decimal}f}"  # Usa ponto para milhares e vírgula para decimais
    return valor_formatado.replace(',', 'X').replace('.', ',').replace('X', '.')

def sanitizar_valor(valor):
    if isinstance(valor, str):  # Verifica se é uma string
        valor = valor.replace("R$", "").replace("\u00a0", "").replace(".", "").replace(",", ".").replace(" ", "").strip()
        return float(valor)
    return valor