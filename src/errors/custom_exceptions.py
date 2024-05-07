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


class ValidateSellerSubsciprtionError(Exception):
    def __init__(self, message="Validate seller subscription Error") -> None:
        self.message = message
        super().__init__(self.message)


class MultipleSellerSubscriptionDetected(Exception):
    def __init__(
        self, message="Multiple Seller Subsciption for the given email"
    ) -> None:
        self.message = message
        super().__init__(self.message)


class SellerSubscriptionNotActive(Exception):
    def __init__(self, message="Seller subscription is not active") -> None:
        self.message = message
        super().__init__(self.message)


class ReduceLimitOnSubscriptionCancelledError(Exception):
    def __init__(self, message="ReduceLimitOnSubscriptionCancelledError") -> None:
        self.message = message
        super().__init__(self.message)


class BuyerMustUpdateAddressBeforeOrderError(Exception):
    def __init__(
        self, message="Buyer did not set delivery address before checkout"
    ) -> None:
        self.message = message
        super().__init__(self.message)


class NotAllowedToUploadThisImage(Exception):
    def __init__(self, message="NotAllowedToUploadThisImage") -> None:
        self.message = message
        super().__init__(self.message)


class MaximumFeaturedLimit(Exception):
    def __init__(self, message="MaximumFeaturedLimit") -> None:
        self.message = message
        super().__init__(self.message)


class Generic400Error(Exception):
    def __init__(self, message="Generic400") -> None:
        self.message = message
        super().__init__(self.message)


class DishDoesNotHaveEnoughToSell(Exception):
    def __init__(self, message="DishDoesNotHaveEnoughToSell") -> None:
        self.message = message
        super().__init__(self.message)


class SellerApplicationHasNotApproved(Exception):
    def __init__(self, message="SellerApplicationHasNotApproved") -> None:
        self.message = message
        super().__init__(self.message)
