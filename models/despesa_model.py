from .base_model import BaseModel

class DespesaModel(BaseModel):
    def inserir(self, dicionario):
        query = """
                    INSERT INTO despesa (
                        idusuario,
                        idcategoria,
                        idcartao,
                        idimportacao,
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
                        %(idimportacao)s,
                        %(valor)s,
                        %(descricao)s,
                        %(observacao)s,
                        %(dataDespesa)s,
                        %(dataHoraCadastro)s,
                        %(dataHoraAlteracao)s
                    )
                """
        try:
            self.cursor.execute(query, dicionario)
            return self.cursor.lastrowid  # Retorna o ID do novo usuário
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir usuário: {e}")

    def consultrar(self, user_id):
        query = "SELECT * FROM despesa WHERE id = %s"
        try:
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()  # Retorna um único registro
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar usuário: {e}")