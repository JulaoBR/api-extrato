from .connection import get_connection

class ConnectionManager:
    _connection = None
    _cursor = None
    _active_transactions = 0

    @classmethod
    def get_connection(cls):
        """Obtém a conexão e o cursor, iniciando uma nova transação se necessário."""
        if cls._connection is None:
            cls._connection = get_connection()
            cls._cursor = cls._connection.cursor()
        cls._active_transactions += 1
        return cls._connection, cls._cursor

    @classmethod
    def release_connection(cls, commit=True):
        """Libera a conexão, aplicando commit ou rollback conforme necessário."""
        if cls._active_transactions <= 0:
            raise RuntimeError("Tentativa de liberar conexão sem transação ativa.")

        cls._active_transactions -= 1
        if cls._active_transactions == 0:
            try:
                if commit:
                    cls._connection.commit()
                else:
                    cls._connection.rollback()
            finally:
                cls._cursor.close()
                cls._connection.close()
                cls._connection = None
                cls._cursor = None

    @classmethod
    def close_all(cls):
        """Fecha a conexão e cursor imediatamente, se ainda estiverem abertos."""
        if cls._cursor:
            cls._cursor.close()
        if cls._connection:
            cls._connection.close()
        cls._connection = None
        cls._cursor = None
        cls._active_transactions = 0

    @classmethod
    def transaction(cls):
        """Protocolo de contexto para gerenciar conexões automaticamente."""
        class TransactionContext:
            def __enter__(self_):
                return cls.get_connection()

            def __exit__(self_, exc_type, exc_value, traceback):
                cls.release_connection(commit=exc_type is None)

        return TransactionContext()