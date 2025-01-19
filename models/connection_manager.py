from .connection import get_connection

class ConnectionManager:
    _connection = None
    _cursor = None
    _active_transactions = 0

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._connection = get_connection()
            cls._cursor = cls._connection.cursor()
        cls._active_transactions += 1
        return cls._connection, cls._cursor

    @classmethod
    def release_connection(cls, commit=True):
        cls._active_transactions -= 1
        if cls._active_transactions <= 0:
            if commit:
                cls._connection.commit()
            else:
                cls._connection.rollback()
            cls._cursor.close()
            cls._connection.close()
            cls._connection = None
            cls._cursor = None