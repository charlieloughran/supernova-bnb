# lib/user.py

class User:
    def __init__(
        self,
        first_name: str,
        surname: str,
        email: str,
        password: str,
        id: int | None = None,
    ) -> None:

        self.first_name = first_name
        self.surname = surname
        self.email = email
        self.password = password
        self.id = id
        # self.dob = dob

    def __repr__(self):
        return f"User({self.first_name}, {self.surname}, {self.email}, {self.id})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.__dict__ == other.__dict__
