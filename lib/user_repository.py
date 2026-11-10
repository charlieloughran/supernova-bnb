# user_repository.py

from lib.user import User
from lib.database_connection import DatabaseConnection


class UserRepository:
    def __init__(self, connection: DatabaseConnection):
        self._connection = connection

    def create(self, user: User) -> None:
        self._connection.execute(
            "insert into users (first_name, surname, email, password) VALUES (%s, %s, %s, %s)",
            [user.first_name, user.surname, user.email, user.password],
        )

    def find_by_email(self, email: str) -> User | None:
        rows = self._connection.execute(
            "select * from users where email = %s", [email]
        )  # a list of dictionaries
        if not rows:
            return None
        row = rows[0]
        return User(
            row["first_name"], row["surname"], row["email"], row["password"], row["id"]
        )

    def all(self) -> list[User]:
        rows = self._connection.execute("select * from users order by id")
        return [
            User(
                row["first_name"],
                row["surname"],
                row["email"],
                row["password"],
                row["id"],
            )
            for row in rows
        ]

    def find(self, id: int) -> User | None:
        rows = self._connection.execute("select * from users where id = %s", [id])
        if not rows:
            return None
        row = rows[0]
        return User(
            row["first_name"], row["surname"], row["email"], row["password"], row["id"]
        )
