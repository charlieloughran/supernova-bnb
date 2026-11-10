from app import app 
from lib.database_connection import DatabaseConnection
from playwright.sync_api import Page, expect

"""
get_space_details returns status 200
"""
def test_get_space_details_returns_correctly():
    client = app.test_client()
    response = client.get("/spaces/1")

    assert response.status_code == 200

"""
space.html shows the correct space listing
"""
def test_space_page_has_correct_listing_details(page: Page, db_connection, test_web_address):
    db_connection.seed("seeds/spaces.sql")

    page.goto(f"http://{test_web_address}/spaces/2")

    assert page.locator('.space_details h2').all_text_contents() == ["Venus"]
    assert page.locator('.space_details h3').all_text_contents()  == ["For the fly trap lovers"]

"""
date selector displays error when already booked date is selected
"""

"""
booking form correctly submits booking to db
"""

