# tests/test_bookings_routes.py

from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection
from lib.booking_repository import BookingRepository

# Bob (bob@example.com) is user 2 in seeds/users.sql
USER_ID = 2

def test_bookings_list_shown(page: Page, db_connection: DatabaseConnection, test_web_address, login):
    db_connection.seed('seeds/users.sql')
    db_connection.seed('seeds/spaces.sql')
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
    db_connection.seed('seeds/spaces.sql')
    db_connection.seed('seeds/bookings.sql')
    
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
    db_connection.seed('seeds/spaces.sql')
    db_connection.seed('seeds/bookings.sql')
        
    login("bob@example.com", "password2")

    response = page.goto(f"http://{test_web_address}/bookings/999")

    assert response.status == 404
    
def test_bookings_redirects_to_login_when_logged_out(page: Page, test_web_address):
    page.goto(f"http://{test_web_address}/bookings")
    
    assert page.url == f"http://{test_web_address}/login/new"
    
def test_booking_detail_redirects_to_login_when_logged_out(page: Page, test_web_address):
    page.goto(f"http://{test_web_address}/bookings/1")

    assert page.url == f"http://{test_web_address}/login/new"
    
def test_bookings_cards_display_card_details(page: Page, login, db_connection: DatabaseConnection, test_web_address):
    db_connection.seed('seeds/users.sql')
    db_connection.seed('seeds/spaces.sql')
    db_connection.seed('seeds/bookings.sql')
    
    login('bob@example.com', 'password2')
    
    page.goto(f"http://{test_web_address}/bookings")
    
    expect(page.locator(".booking-card")).to_have_count(3)

    expect(page.locator(".booking-space-name")).to_have_text(["Earth", "Mercury", "Venus"])
    expect(page.locator(".booking-price-per-night")).to_contain_text(["220.13", "220.13", "220.13"])
    expect(page.locator(".booking-date")).to_have_text(["2027-03-01", "2027-02-11", "2027-02-11"])
    expect(page.locator(".booking-status")).to_have_text(["requested", "requested", "requested"])
    
    cards = page.locator(".booking-card")

    expect(cards.nth(0).get_by_role("link")).to_have_attribute("href", "/spaces/3")
    expect(cards.nth(1).get_by_role("link")).to_have_attribute("href", "/spaces/1")
    expect(cards.nth(2).get_by_role("link")).to_have_attribute("href", "/spaces/2")
    
def test_bookings_shows_message_when_user_has_no_bookings(page: Page, login, db_connection: DatabaseConnection, test_web_address):
    db_connection.seed('seeds/users.sql')
    db_connection.seed('seeds/spaces.sql')
    db_connection.seed('seeds/bookings.sql')
    db_connection.execute("DELETE FROM bookings WHERE booked_by = %s", [2])

    login("bob@example.com", "password2") #this is booked_by = 2 per above
    
    page.goto(f"http://{test_web_address}/bookings")
    
    expect(page.locator(".booking-card")).to_have_count(0)
    expect(page.locator(".no-bookings-message")).to_have_text("You have no bookings yet.")
    
def test_bookings_grouped_by_status(page: Page, login, db_connection: DatabaseConnection, test_web_address):
    db_connection.seed('seeds/users.sql')
    db_connection.seed('seeds/spaces.sql')
    db_connection.seed('seeds/bookings.sql')
    
    login("bob@example.com", "password2")
    db_connection.execute("INSERT INTO bookings (space_id, booked_by, date, status) VALUES (%s, %s, %s, %s)", [4, 2, '2027-04-10', 'accepted'])
    db_connection.execute("INSERT INTO bookings (space_id, booked_by, date, status) VALUES (%s, %s, %s, %s)", [6, 2, '2027-01-01', 'declined'])
    
    page.goto(f"http://{test_web_address}/bookings")
    
    expect(page.locator(".booking-status-grouping")).to_have_count(3)
    expect(page.locator(".booking-status-grouping-title")).to_have_text(["Requested", "Accepted", "Declined"])
    
    requested = page.locator(".booking-status-grouping").nth(0)
    accepted = page.locator(".booking-status-grouping").nth(1)
    declined = page.locator(".booking-status-grouping").nth(2)
    
    expect(requested.locator(".booking-space-name")).to_have_text(["Earth", "Mercury", "Venus"])
    expect(accepted.locator(".booking-space-name")).to_have_text(["Mars"])
    expect(declined.locator(".booking-space-name")).to_have_text(["Saturn"])

def test_bookings_hides_empty_status_sections(page: Page, login, db_connection: DatabaseConnection, test_web_address):
    
    db_connection.seed("seeds/users.sql")
    db_connection.seed("seeds/spaces.sql")
    db_connection.seed("seeds/bookings.sql")

    login("bob@example.com", "password2")

    page.goto(f"http://{test_web_address}/bookings")

    expect(page.locator(".booking-status-grouping")).to_have_count(1)
    expect(page.locator(".booking-status-grouping-title")).to_have_text(["Requested"])
    
def test_bookings_shows_expired_bookings(page: Page, login, db_connection: DatabaseConnection, test_web_address):
    db_connection.seed("seeds/users.sql")
    db_connection.seed("seeds/spaces.sql")
    db_connection.seed("seeds/expired_bookings.sql")

    login("bob@example.com", "password2")

    page.goto(f"http://{test_web_address}/bookings")

    expect(page.locator(".booking-status-grouping-title")).to_have_text(["Requested", "Expired"])
    expired = page.locator(".booking-status-grouping").nth(1)
    expect(expired.locator(".booking-space-name")).to_have_text(["Earth"])
    