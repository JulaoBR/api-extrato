from .connection import get_connection

class DespesaParcelaModel:
    @staticmethod
    def inserir(dicionario):
        query = """
                    INSERT INTO despesaparcela (
                        iddespesa,
                        numero,
                        valorParcela,
                        desconto,
                        acrescimo,
                        dataVencimento,
                        dataPagamento,
                        competencia,
                        status,
                        evento
                    ) VALUES (
                        %(iddespesa)s,
                        %(numero)s,
                        %(valorParcela)s,
                        %(desconto)s,
                        %(acrescimo)s,
                        %(dataVencimento)s,
                        %(dataPagamento)s,
                        %(competencia)s,
                        %(status)s,
                        %(evento)s
                    )
                """
        try:
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, dicionario)
                    connection.commit()
                    return cursor.lastrowid  # Retorna o ID do novo usuário
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir usuário: {e}")

    @staticmethod
    def consultrar(user_id):
        query = "SELECT * FROM despesaparcela WHERE id = %s"
        try:
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    return cursor.fetchone()  # Retorna um único registro
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar usuário: {e}")