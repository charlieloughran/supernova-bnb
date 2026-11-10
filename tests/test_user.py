# tests/test_user.py

from lib.user import User


def test_user_constructs():
    user = User("Alex Smith", "alex@example.com", "hashed_password1")
    assert user.name == "Alex Smith"
    assert user.email == "alex@example.com"
    assert user.password_hash == "hashed_password1"


def test_users_format_nicely():
    user = User("Alex Smith", "alex@example.com", "hashed_password1", 1)
    assert str(user) == "User(Alex Smith, alex@example.com, 1)"


def test_users_are_equal():
    user1 = User("Alex Smith", "alex@example.com", "hashed_password1", 1)
    user2 = User("Alex Smith", "alex@example.com", "hashed_password1", 1)
    assert user1 == user2


def test_id_defaults_to_none():
    user = User("Alex Smith", "alex@example.com", "hashed_password1")
    assert user.id is None


def test_constructs_with_id():
    user = User("Alex Smith", "alex@example.com", "hashed_password1", 5)
    assert user.id == 5


def test_two_different_users_are_not_equal():
    user1 = User("Alex Smith", "alex@example.com", "hashed_password1", 1)
    user2 = User("Sam Jones", "sam@example.com", "hashed_password2", 2)
    assert user1 != user2


def test_users_with_different_emails_are_not_equal():
    user1 = User("Alex Smith", "alex@example.com", "hashed_password1", 1)
    user2 = User("Alex Smith", "other@example.com", "hashed_password1", 1)
    assert user1 != user2


def test_user_is_not_equal_to_a_non_user():
    user = User("Alex Smith", "alex@example.com", "hashed_password1", 1)
    assert user != "alex@example.com"


def test_password_hash_not_in_string():
    user = User("Alex Smith", "alex@example.com", "hashed_password1", 1)
    assert "hashed_password1" not in str(user)
