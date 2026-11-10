from app import app
from playwright.sync_api import Page

def test_auth(page: Page, db_connection, test_web_address):
    db_connection.seed('seeds/users.sql')

    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()

    assert page.url == f'http://{test_web_address}/'

def test_failed_login(page: Page, db_connection, test_web_address):
    db_connection.seed('seeds/users.sql')

    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("Password1")
    page.get_by_role("button", name="Log-in").click()

    assert page.url == f'http://{test_web_address}/login/new'