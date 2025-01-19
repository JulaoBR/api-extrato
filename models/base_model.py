from .connection import get_connection

class BaseModel:
    def __init__(self, connection=None, cursor=None):
        self._external_connection = connection is not None
        self.connection = connection or get_connection()
        self.cursor = cursor or self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._external_connection:  # Apenas gerencia transação se for interna
            if exc_type:
                self.connection.rollback()
            else:
                self.connection.commit()
            self.cursor.close()
            self.connection.close()