# lib/user.py


class User:
    def __init__(
        self, name: str, email: str, password_hash: str, id: int | None = None
    ) -> None:
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.id = id

    def __repr__(self):
        return f"User({self.name}, {self.email}, {self.id})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.__dict__ == other.__dict__
