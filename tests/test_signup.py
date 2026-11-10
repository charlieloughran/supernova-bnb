from playwright.sync_api import Page, expect
from werkzeug.security import check_password_hash

from lib.user_repository import UserRepository

def test_signup(page: Page, db_connection, test_web_address):
    db_connection.seed("seeds/users.sql")

    page.goto(f'http://{test_web_address}/register/new')
    page.get_by_placeholder("Name").fill("John Smith")
    page.get_by_placeholder("Email").fill("john@example.com")
    page.get_by_placeholder("Password").fill("password3")
    page.get_by_role("button", name="Sign-up").click()

    assert page.url == f'http://{test_web_address}/login/new'

    user = UserRepository(db_connection).find_by_email("john@example.com")
    assert user is not None
    assert user.name == "John Smith"
    assert check_password_hash(user.password_hash, "password3")

def test_signup_preexisting_email(page: Page, db_connection, test_web_address):
    db_connection.seed("seeds/users.sql")

    page.goto(f'http://{test_web_address}/register/new')
    page.get_by_placeholder("Name").fill("Alice")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password123")
    page.get_by_role("button", name="Sign-up").click()

    expect(page.get_by_role("alert")).to_contain_text(
        "An account with that email already exists."
    )
