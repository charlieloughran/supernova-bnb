from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection
from lib.space_repository import SpaceRepository
from lib.booking_repository import BookingRepository

from app import app
# As an Owner, I want to see a list of all my booking requests so that I can accept / deny the request

# As an Owner, I want to see a list of all my upcoming bookings

"""
Owner can go to a page of their requests
"""

def test_get_space_details_returns_correctly(page: Page, test_web_address):
    db_connection = DatabaseConnection(test_mode=True)
    db_connection.connect()
    db_connection.seed('seeds/spaces.sql')
    db_connection.seed('seeds/bookings.sql')

    response = page.request.get(f"http://{test_web_address}/my_spaces/requests")

    assert response.status == 200


"""
Owner can see a list of all their booking requests

"""
def test_list_of_all_booking_requests(page: Page, test_web_address):
    db_connection = DatabaseConnection(test_mode=True)
    db_connection.connect()
    db_connection.seed('seeds/spaces.sql')
    db_connection.seed('seeds/bookings.sql')

    #User signed in 
    user_id = 2

    user_bookings = BookingRepository(db_connection).find_by_user_and_status(user_id, "requested")
    user_booking_ids = [str(booking.id) for booking in user_bookings]

    page.goto(f"http://{test_web_address}/my_spaces/requests")

    page_title = page.locator('h2')

    expect(page_title).to_have_text('My Spaces - Bookings')

    booking_ids = page.locator('.booking-id').all_inner_texts()

    assert user_booking_ids == booking_ids


"""
Owner accepts request (route)
"""
def test_owner_accepts_request(page, test_web_address):
    pass

"""
Owner denies request (route)
"""

def test_owner_denies_request(page, test_web_address):
    pass

"""
Owner accepts request (DB)
"""

def test_database_result_when_owner_accepts_request(page, test_web_address):
    pass

"""
Owner denies request (DB)

"""

def test_database_result_when_owner_denies_request(page, test_web_address):
    pass

"""
Owner receives mutliple requests within same dates

"""

def test_owner_receives_mutliple_requests_within_same_date(page, test_web_address):
    pass


"""
Date of booking has passed today's date

"""

def test_date_of_booking_is_before_today(page, test_web_address):
    pass




