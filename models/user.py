from dataclasses import dataclass, field
from typing import Dict, List
import uuid
from models import Model
from common.errors import UserNotFoundError, InvalidEmailError, UserAlreadyExistError, PasswordNotMatchError, PasswordError
from common.utils import Utils

@dataclass
class User(Model):
    collection: str = field(init=False, default="users")
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
        }

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by("email", email)
        except TypeError as e:
            print(e)
            raise UserNotFoundError("This email is not found")

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise InvalidEmailError("Wrong format of the email")

        Utils.check_password(password)

        try:
            cls.find_by_email(email)
            raise UserAlreadyExistError("This email has been registered")
        except UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_mongo()

        return True

    @classmethod
    def is_login_valid(cls, email, password) -> bool:
        if not Utils.email_is_valid(email):
            raise InvalidEmailError("Wrong format of the email")

        user = cls.find_by_email(email)
        if not Utils.verify_hash_password(password, user.password):
            raise PasswordNotMatchError("Password is wrong ")

        return True
