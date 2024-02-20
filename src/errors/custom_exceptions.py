class ServerException(Exception):
    def __init__(self, message="Server error occurred", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidTokenException(Exception):
    def __init__(self, message="Invalid token"):
        self.message = message
        super().__init__(self.message)
