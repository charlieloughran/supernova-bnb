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

    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()

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

    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("bob@example.com")
    page.get_by_placeholder("Password").fill("password2")
    page.get_by_role("button", name="Log-in").click()


    user_bookings = BookingRepository(db_connection).find_by_user_and_status(2, "requested")
    user_booking_ids = [str(booking.id) for booking in user_bookings]

    page.goto(f"http://{test_web_address}/my_spaces/requests")

    booking_ids = page.locator('.booking-id').all_inner_texts()

    assert user_booking_ids == booking_ids


"""
Owner accepts request
"""
def test_owner_accepts_request(page, test_web_address):
    db_connection = DatabaseConnection(test_mode=True)
    db_connection.connect()
    db_connection.seed('seeds/spaces.sql')
    db_connection.seed('seeds/bookings.sql')

    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("bob@example.com")
    page.get_by_placeholder("Password").fill("password2")
    page.get_by_role("button", name="Log-in").click()

    page.goto(f"http://{test_web_address}/my_spaces/requests")

    booking_ids = page.locator('.booking-id').all_inner_texts()

    page.get_by_role("button", name="Accept").click()

    booking_repo = BookingRepository(db_connection)


    assert booking_repo.find_by_booking(5).status == "accepted"



"""
Owner denies request (route)
"""

def test_owner_denies_request(page, test_web_address):
        db_connection = DatabaseConnection(test_mode=True)
        db_connection.connect()
        db_connection.seed('seeds/spaces.sql')
        db_connection.seed('seeds/bookings.sql')

        page.goto(f"http://{test_web_address}/login/new")
        page.get_by_placeholder("Email").fill("bob@example.com")
        page.get_by_placeholder("Password").fill("password2")
        page.get_by_role("button", name="Log-in").click()

        page.goto(f"http://{test_web_address}/my_spaces/requests")

        page.get_by_role("button", name="Deny").click()

        booking_repo = BookingRepository(db_connection)


        assert booking_repo.find_by_booking(5).status == "declined"


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




