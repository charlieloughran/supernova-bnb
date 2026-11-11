from playwright.sync_api import Page, expect

def test_auth(page: Page, db_connection, test_web_address):
    db_connection.seed('seeds/users.sql')

    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()

    assert page.url == f'http://{test_web_address}/'

def test_login_incorrect_password(page: Page, test_web_address):
    page.goto(f'http://{test_web_address}/login/new')
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password123")
    page.get_by_role("button", name="Log-in").click()

    assert page.url == f'http://{test_web_address}/login'
    expect(page.get_by_role("alert")).to_contain_text(
        "Incorrect email or password."
    )

def test_login_incorrect_email(page: Page, test_web_address):
    page.goto(f'http://{test_web_address}/login/new')
    page.get_by_placeholder("Email").fill("alic@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()

    assert page.url == f'http://{test_web_address}/login'
    expect(page.get_by_role("alert")).to_contain_text(
        "Incorrect email or password."
    )