from .connection import get_connection

class DespesaModel:
    @staticmethod
    def inserir(dicionario):
        query = """
                    INSERT INTO despesa (
                        idusuario,
                        idcategoria,
                        idcartao, 
                        valor,
                        descricao,
                        observacao,
                        dataDespesa,
                        dataHoraCadastro,
                        dataHoraAlteracao
                    ) VALUES (
                        %(idusuario)s,
                        %(idcategoria)s,
                        %(idcartao)s,
                        %(valor)s,
                        %(descricao)s,
                        %(observacao)s,
                        %(dataDespesa)s,
                        %(dataHoraCadastro)s,
                        %(dataHoraAlteracao)s
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
        query = "SELECT * FROM despesa WHERE id = %s"
        try:
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    return cursor.fetchone()  # Retorna um único registro
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar usuário: {e}")