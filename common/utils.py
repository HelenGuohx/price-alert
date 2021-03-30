import re
from passlib.hash import pbkdf2_sha512
from common.errors import PasswordError

class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        email_pattern = re.compile(r"^[\w\d-]+@([\w-]+\.)+\w+$")
        return True if email_pattern.search(email) else False

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def verify_hash_password(password: str, hash_password: str) -> bool:
        return pbkdf2_sha512.verify(password, hash_password)

    @staticmethod
    def check_password(password: str) -> bool:
        if len(password) < 6:
            raise PasswordError("Password must have at least 6 characters")

        letter_pattern = re.compile(r'[a-zA-Z]')
        if not re.search(letter_pattern, password):
            raise PasswordError("Password must contain letters a-z or A-Z")

        number_pattern = re.compile(r'\d')
        if not re.search(number_pattern, password):
            raise PasswordError("Password must contain numbers 0-9")

        return True
