import pandas as pd
from io import StringIO

class CSVValidationResult:
    """ Classe para armazenar o resultado da validação do CSV """
    def __init__(self, success, error=None, dataframe=None):
        self.success = success
        self.error = error
        self.dataframe = dataframe  # Pode ser útil para outra função que precisa do CSV

    def is_valid(self):
        """ Retorna True se o CSV for válido, False caso contrário """
        return self.success

    def get_error(self):
        """ Retorna o erro se houver, ou None """
        return self.error

def validar_csv_import_cartao(file):
    try:
        if file.stream.read(1) == b"":  # Lê o primeiro byte para checar se está vazio
            return CSVValidationResult(
                success=False,
                error=f"O arquivo está vazio!"
            )

        file.stream.seek(0)

        # Lê o arquivo como texto
        file_data = file.stream.read().decode('utf-8')

        # Ler o CSV com pandas
        df = pd.read_csv(StringIO(file_data), sep=",", quotechar='"', encoding="utf-8")

        # Definir colunas esperadas
        colunas_esperadas = ["Data", "Lançamento", "Categoria", "Tipo", "Valor"]

        # Validar colunas
        if list(df.columns) != colunas_esperadas:
            return CSVValidationResult(
                success=False,
                error=f"As colunas do arquivo não estão corretas. Esperado: {colunas_esperadas}, Encontrado: {list(df.columns)}"
            )

        # Retorna sucesso com o DataFrame
        return CSVValidationResult(success=True, dataframe=df)

    except pd.errors.ParserError as e:
        return CSVValidationResult(success=False, error=f"Erro ao processar o CSV: {str(e)}")
    except UnicodeDecodeError:
        return CSVValidationResult(success=False, error="Erro de codificação: o arquivo não está em UTF-8.")
    except Exception as e:
        return CSVValidationResult(success=False, error=f"Erro inesperado: {str(e)}")