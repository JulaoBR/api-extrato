import unicodedata
from unidecode import unidecode

def remover_acentos(texto):
    """Remove acentos de uma string."""
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )

def converter_para_maiusculas(texto):
    return texto.upper()

