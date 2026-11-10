# tests/test_user_repository.py

from werkzeug.security import check_password_hash, generate_password_hash

from lib.user import User
from lib.user_repository import UserRepository
from lib.database_connection import DatabaseConnection


def test_get_all_users(db_connection: DatabaseConnection):
    db_connection.seed("seeds/users.sql")
    repository = UserRepository(db_connection)

    users = repository.all()

    assert [(u.id, u.name, u.email) for u in users] == [
        (1, "Alice Smith", "alice@example.com"),
        (2, "Bob Jones", "bob@example.com"),
    ]


def test_seeded_password_hashes_are_real_hashes(db_connection: DatabaseConnection):
    db_connection.seed("seeds/users.sql")
    repository = UserRepository(db_connection)

    users = repository.all()

    assert check_password_hash(users[0].password_hash, "password1")
    assert check_password_hash(users[1].password_hash, "password2")


def test_find_user_by_id(db_connection: DatabaseConnection):
    db_connection.seed("seeds/users.sql")
    repository = UserRepository(db_connection)

    user = repository.find(1)

    assert (user.id, user.name, user.email) == (1, "Alice Smith", "alice@example.com")


def test_find_user_by_id_returns_none_when_missing(db_connection: DatabaseConnection):
    db_connection.seed("seeds/users.sql")
    repository = UserRepository(db_connection)

    assert repository.find(999) is None


def test_find_user_by_email(db_connection: DatabaseConnection):
    db_connection.seed("seeds/users.sql")
    repository = UserRepository(db_connection)

    user = repository.find_by_email("bob@example.com")

    assert (user.id, user.name, user.email) == (2, "Bob Jones", "bob@example.com")


def test_find_user_by_email_returns_none_when_missing(
    db_connection: DatabaseConnection,
):
    db_connection.seed("seeds/users.sql")
    repository = UserRepository(db_connection)

    assert repository.find_by_email("nobody@example.com") is None


def test_create_user(db_connection: DatabaseConnection):
    db_connection.seed("seeds/users.sql")
    repository = UserRepository(db_connection)
    new_user = User(
        "Carol Lee", "carol@example.com", generate_password_hash("password3")
    )

    repository.create(new_user)

    saved = repository.find_by_email("carol@example.com")
    assert (saved.id, saved.name, saved.email) == (3, "Carol Lee", "carol@example.com")
    assert check_password_hash(saved.password_hash, "password3")
    assert len(repository.all()) == 3
