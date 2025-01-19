from .base_model import BaseModel

class CategoriaModel(BaseModel):
    def consultrar(self, id_usuario):
        query = """
                    SELECT 
                        categoria.idcategoria,
                        categoria.descricao,
                        categoria.descricao_extra
                    FROM categoria
                    WHERE idusuario = %s
                    ORDER BY descricao
                """
        try:
            self.cursor.execute(query, (id_usuario))
            return self.cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar categoria: {e}")