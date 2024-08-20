class DatabaseSessionManagerError(Exception):
    def __init__(self, *args: object) -> None:
        self.message = 'DatabaseSessionManager is not initialized'
        super().__init__(*args)

