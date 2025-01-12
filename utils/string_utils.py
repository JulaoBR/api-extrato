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

def converter_para_minusculas(texto):
    return texto.lower()

def capitalize_primeira_letra(texto):
    return texto.capitalize()

def remover_espacos_extras(texto):
    return " ".join(texto.split())

def esta_vazia(texto):
    return not texto or texto.strip() == ""

def extrair_substring(texto, inicio, fim):
    return texto[inicio:fim]