from .base_model import BaseModel

class ImporteDocumentoModel(BaseModel):
    def inserir(self, dicionario):
        query = """
                    INSERT INTO impotacao_documento (
                        idusuario,
                        idcartao,
                        idconta,
                        nome_arquivo,
                        tipo_arquivo,
                        tamanho_arquivo,
                        arquivo,
                        dataHoraCadastro
                    ) VALUES (
                        %(idusuario)s,
                        %(idcartao)s,
                        %(idconta)s,
                        %(nome_arquivo)s,
                        %(tipo_arquivo)s,
                        %(tamanho_arquivo)s,
                        %(arquivo)s,
                        %(dataHoraCadastro)s
                    )
                """
        try:
            self.cursor.execute(query, dicionario)
            return self.cursor.lastrowid
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir documento de importacao: {e}")