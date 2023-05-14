from models.user import User


def authenticate(username: str, password: str) -> User:
    return User.auth(username, password)
