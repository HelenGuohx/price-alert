

class Error(Exception):
    """base class for exceptions"""
    def __init__(self, message):
        self.message = message


class RequestFailureError(Error):
    pass


class HTMLElementNotMatched(Error):
    pass


class UserNotFoundError(Error):
    pass


class InvalidEmailError(Error):
    pass


class UserAlreadyExistError(Error):
    pass


class PasswordError(Error):
    pass


class PasswordNotMatchError(PasswordError):
    pass
