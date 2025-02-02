from .base_model import BaseModel

class DespesaParcelaModel(BaseModel):
    def inserir(self, dicionario):
        query = """
                    INSERT INTO despesaparcela (
                        iddespesa,
                        numero,
                        valorParcela,
                        desconto,
                        acrescimo,
                        dataVencimento,
                        competencia,
                        status,
                        evento,
                        origem_importacao
                    ) VALUES (
                        %(iddespesa)s,
                        %(numero)s,
                        %(valorParcela)s,
                        %(desconto)s,
                        %(acrescimo)s,
                        %(dataVencimento)s,
                        %(competencia)s,
                        %(status)s,
                        %(evento)s,
                        %(origem_importacao)s
                    )
                """
        try:
            self.cursor.execute(query, dicionario)
            return self.cursor.lastrowid  # Retorna o ID do novo usuário
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir usuário: {e}")

    def consultrar(self, user_id):
        query = "SELECT * FROM despesaparcela WHERE id = %s"
        try:
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()  # Retorna um único registro
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar usuário: {e}")