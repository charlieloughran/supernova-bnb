from playwright.sync_api import Page, expect

"""
this test checks that when the user clicks, logout from a page, they are redirected to home page and the session is removed
"""

def test_logout(page: Page, db_connection, test_web_address):
    db_connection.seed('seeds/users.sql')

    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()
    
    page.goto(f"http://{test_web_address}/my_spaces")
    page.locator('a[href="/logout"]').click()
        
    welcome_msg = page.locator('h1')
    expect(welcome_msg).to_have_text('Welcome Guest')