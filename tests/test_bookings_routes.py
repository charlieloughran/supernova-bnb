# tests/test_bookings_routes.py

from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection
from lib.booking_repository import BookingRepository

# Bob (bob@example.com) is user 2 in seeds/users.sql
USER_ID = 2

def test_bookings_list_shown(page: Page, db_connection: DatabaseConnection, test_web_address, login):
    db_connection.seed('seeds/users.sql')
    db_connection.seed('seeds/bookings.sql')
    
    login("bob@example.com", "password2")
    
    repository = BookingRepository(db_connection)
    user_bookings = repository.find_by_user_id(USER_ID)
    statuses = [booking.status for booking in user_bookings]

    page.goto(f"http://{test_web_address}/bookings")

    shown = page.locator(".booking-status")

    assert statuses == shown.all_inner_texts()
    
def test_booking_detail_shown(
    page: Page, db_connection: DatabaseConnection, test_web_address, login
):
    db_connection.seed('seeds/users.sql')
    db_connection.seed("seeds/bookings.sql")
    
    login("bob@example.com", "password2")

    repository = BookingRepository(db_connection)
    booking = repository.find_by_booking(1)

    page.goto(f"http://{test_web_address}/bookings/1")

    expect(page.locator(".booking-date")).to_have_text(str(booking.date))
    expect(page.locator(".booking-status")).to_have_text(booking.status)
    
def test_booking_detail_returns_404_when_missing(
    page: Page, db_connection: DatabaseConnection, test_web_address, login
):
    db_connection.seed('seeds/users.sql')
    db_connection.seed("seeds/bookings.sql")
        
    login("bob@example.com", "password2")

    response = page.goto(f"http://{test_web_address}/bookings/999")

    assert response.status == 404
    
def test_bookings_redirects_to_login_when_logged_out(page: Page, test_web_address):
    page.goto(f"http://{test_web_address}/bookings")
    
    assert page.url == f"http://{test_web_address}/login/new"
    
def test_booking_detail_redirects_to_login_when_logged_out(page: Page, test_web_address):
    page.goto(f"http://{test_web_address}/bookings/1")

    assert page.url == f"http://{test_web_address}/login/new"