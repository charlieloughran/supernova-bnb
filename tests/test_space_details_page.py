from app import app 
from lib.database_connection import DatabaseConnection
from playwright.sync_api import Page, expect

"""
get_space_details returns status 200
"""
def test_get_space_details_returns_correctly(page: Page, test_web_address):
    response = page.request.get(f"http://{test_web_address}/spaces/1")

    assert response.status == 200

"""
space.html shows the correct space listing
"""
def test_space_page_has_correct_listing_details(page: Page, db_connection, test_web_address):
    db_connection.seed("seeds/spaces.sql")
    db_connection.seed("seeds/bookings.sql")

    page.goto(f"http://{test_web_address}/spaces/2")

    expect(page.locator('.space_details h2')).to_have_text("Venus")
    expect(page.locator('.space_details h3')).to_have_text("For the fly trap lovers")

"""
date selector displays error when already booked date is selected
"""
def test_date_selector_displays_error_for_booked_dates(page: Page, db_connection, test_web_address):
    db_connection.seed("seeds/spaces.sql")
    db_connection.seed("seeds/bookings.sql")
    db_connection.seed("seeds/users.sql")

    # first log in
    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()

    page.goto(f"http://{test_web_address}/spaces/2")
    page.get_by_label('Select date:').fill('2027-01-02')
    page.get_by_role('button', name='Request booking').click()

    expect(page.locator(".alert-error")).to_be_visible()
    expect(page.locator('.alert-error')).to_have_text('Sorry, this date is already booked. Please select another date.')

"""
date selector displays error when user selects date above the max date available
"""
def test_date_selector_displays_error_for_unavailable_dates(page: Page, db_connection, test_web_address):
    db_connection.seed("seeds/spaces.sql")
    db_connection.seed("seeds/bookings.sql")
    db_connection.seed("seeds/users.sql")

    # first log in
    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()

    page.goto(f"http://{test_web_address}/spaces/2")
    page.get_by_label('Select date:').fill('2030-01-02')
    page.get_by_role('button', name='Request booking').click()

    expect(page.locator(".alert-error")).to_be_visible()
    expect(page.locator('.alert-error')).to_have_text('Sorry, the space is unavailable on this date. Please select a date available on the calendar')

"""
date selector displays error when user selects date in the past
"""
def test_date_selector_displays_error_for_past_dates(page: Page, db_connection, test_web_address):
    db_connection.seed("seeds/spaces.sql")
    db_connection.seed("seeds/bookings.sql")
    db_connection.seed("seeds/users.sql")

    # first log in
    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()

    page.goto(f"http://{test_web_address}/spaces/2")
    page.get_by_label('Select date:').fill('2021-01-02')
    page.get_by_role('button', name='Request booking').click()

    expect(page.locator(".alert-error")).to_be_visible()
    expect(page.locator('.alert-error')).to_have_text('The date selected is in the past. Please select a date available on the calendar.')

"""
date selector displays error when user submits without inputting a date
"""
def test_date_selector_displays_error_when_no_date(page: Page, db_connection, test_web_address):
    db_connection.seed("seeds/spaces.sql")
    db_connection.seed("seeds/bookings.sql")
    db_connection.seed("seeds/users.sql")

    # first log in
    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()

    page.goto(f"http://{test_web_address}/spaces/2")
    page.get_by_role('button', name='Request booking').click()

    expect(page.locator(".alert-error")).to_be_visible()
    expect(page.locator('.alert-error')).to_have_text('Please select a date.')


"""
booking form correctly submits booking to db
"""
def test_date_selector_correctly_submits_booking(page: Page, db_connection, test_web_address):
    db_connection.seed("seeds/spaces.sql")
    db_connection.seed("seeds/bookings.sql")
    db_connection.seed("seeds/users.sql")

    # first log in
    page.goto(f"http://{test_web_address}/login/new")
    page.get_by_placeholder("Email").fill("alice@example.com")
    page.get_by_placeholder("Password").fill("password1")
    page.get_by_role("button", name="Log-in").click()

    # navigate to space page and complete form
    page.goto(f"http://{test_web_address}/spaces/2")
    page.get_by_label('Select date:').fill('2027-01-01')
    expect(page.get_by_label('Select date:')).to_have_value('2027-01-01')
    page.get_by_role('button', name='Request booking').click()

    result = db_connection.execute("SELECT * FROM bookings WHERE date = '2027-01-01' and space_id = 2 and booked_by = 1 and status = 'requested'")
    assert len(result) == 1
    assert result[0]['booked_by'] == 1
    assert result[0]['space_id'] == 2
    assert result[0]['status'] == 'requested'

def test_owner_sees_note_instead_of_booking_form_on_their_own_space(page: Page, db_connection: DatabaseConnection, login, test_web_address):
    db_connection.seed('seeds/users.sql')
    db_connection.seed('seeds/spaces.sql')
    db_connection.seed('seeds/bookings.sql')
    
    login("bob@example.com", "password2")
    
    page.goto(f"http://{test_web_address}/spaces/2")
    
    expect(page.get_by_role("button", name="Request Booking")).to_have_count(0)
    expect(page.locator(".owner-note")).to_have_text("This is your space, so you cannot book it")

def test_owner_cant_book_own_space_by_posting_directly(page: Page, db_connection:DatabaseConnection, login, test_web_address):
    # block spaces/2 from submitting a post request for Bob
    db_connection.seed('seeds/users.sql')
    db_connection.seed('seeds/spaces.sql')
    db_connection.seed('seeds/bookings.sql')
    
    login("bob@example.com", "password2")
    
    page.request.post(f"http://{test_web_address}/spaces/2", form={"booking_date": "2027-03-15"})
    
    result = db_connection.execute("SELECT * FROM bookings WHERE date = '2027-03-15' AND space_id = 2")  #

    assert len(result) == 0
