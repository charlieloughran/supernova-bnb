from app import app
from playwright.sync_api import Page

def test_auth(page: Page, db_connection):
    db_connection.seed('seeds/users.sql')

    page.goto("http://localhost:5001/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()

    assert page.url == 'http://localhost:5001/'

def test_failed_login(page: Page, db_connection):
    db_connection.seed('seeds/users.sql')

    page.goto("http://localhost:5001/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("Password1")
    page.get_by_role("button", name="Log-in").click()

    assert page.url == 'http://localhost:5001/login/new'