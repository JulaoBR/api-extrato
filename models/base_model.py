from .connection_manager import ConnectionManager

class BaseModel:
    def __init__(self):
        self.connection, self.cursor = ConnectionManager.get_connection()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        commit = exc_type is None
        ConnectionManager.release_connection(commit)