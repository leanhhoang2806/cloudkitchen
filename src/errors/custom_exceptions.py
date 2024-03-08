class ServerException(Exception):
    def __init__(self, message="Server error occurred", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidTokenException(Exception):
    def __init__(self, message="Invalid token") -> None:
        self.message = message
        super().__init__(self.message)


class UniqueViolationException(Exception):
    def __init__(self, message="Unique constraint violation") -> None:
        self.message = message
        super().__init__(self.message)


class MediaUploadLimitException(Exception):
    def __init__(self, message="Maximum Media Upload allowed") -> None:
        self.message = message
        super().__init__(self.message)


class BothSearchTermEmpty(Exception):
    def __init__(
        self, message="Both Zipcode and name in the search term are empty"
    ) -> None:
        self.message = message
        super().__init__(self.message)


class GenericTryError(Exception):
    def __init__(self, message="Generic error on Try") -> None:
        self.message = message
        super().__init__(self.message)
