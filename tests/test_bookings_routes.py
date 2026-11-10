# tests/test_bookings_routes.py

from playwright.sync_api import Page
from lib.database_connection import DatabaseConnection
from lib.booking_repository import BookingRepository


# starts with logged in user, and seed

USER_ID = 2

def test_bookings_list_shown(page: Page, db_connection: DatabaseConnection, test_web_address,):
    db_connection.seed('seeds/bookings.sql')
    
    repository = BookingRepository(db_connection)
    user_bookings = repository.find_by_user_id(USER_ID)
    statuses = [booking.status for booking in user_bookings]

    page.goto(f"http://{test_web_address}/bookings")

    shown = page.locator(".booking-status")

    assert statuses == shown.all_inner_texts()
    