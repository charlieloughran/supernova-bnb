from playwright.sync_api import Page
from werkzeug.security import check_password_hash

from lib.user_repository import UserRepository

def test_signup(page: Page, db_connection):
    db_connection.seed("seeds/users.sql")

    page.goto('http://localhost:5001/register/new')
    page.get_by_placeholder("Name").fill("John Smith")
    page.get_by_placeholder("Email").fill("john@example.com")
    page.get_by_placeholder("Password").fill("password3")
    page.get_by_role("button", name="Sign-up").click()

    assert page.url == 'http://localhost:5001/login/new'

    user = UserRepository(db_connection).find_by_email("john@example.com")
    assert user is not None
    assert user.name == "John Smith"
    assert check_password_hash(user.password_hash, "password3")