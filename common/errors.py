

class Error(Exception):
    """base class for exceptions"""
    def __init__(self, message):
        self.message = message


class RequestFailureError(Error):
    pass


class UserNotFoundError(Error):
    pass


class InvalidEmailError(Error):
    pass


class UserAlreadyExistError(Error):
    pass


class PasswordNotMatchError(Error):
    pass