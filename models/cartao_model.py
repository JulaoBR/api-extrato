from .base_model import BaseModel

class CartaoModel(BaseModel):
    def consultrar(self, id_cartao, id_usuario):
        query = """
                    SELECT *
                    FROM cartao
                    WHERE idcartao = %s AND idusuario = %s
                """
        try:
            self.cursor.execute(query, (id_cartao, id_usuario))
            return self.cursor.fetchone()
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar cartao: {e}")