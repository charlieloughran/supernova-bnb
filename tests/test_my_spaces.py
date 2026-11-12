from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection
from lib.space_repository import SpaceRepository

"""
Render a list of all spaces
"""

def test_my_spaces_list_shown(page: Page, test_web_address, login):
    db_connection = DatabaseConnection(test_mode=True)
    db_connection.connect()
    db_connection.seed('seeds/spaces.sql')

    login("bob@example.com", "password2")

    repository = SpaceRepository(db_connection) 
    user_spaces = repository.find_by_owner_id(2)
    space_names = [space.name for space in user_spaces]

    page.goto(f"http://{test_web_address}/my_spaces")


    

    spaces = page.locator('h3')


    assert space_names == spaces.all_inner_texts()


"""
Render a form to fill in space details

"""
# def test_show_form_to_add_space(page: Page, test_web_address):
#     assert page.url == f"http://{test_web_address}/my_spaces/add"





"""
Fill a form for space details and save to DB
"""

def test_add_space_to_list(page: Page, test_web_address, login):
    db_connection = DatabaseConnection(test_mode=True)
    db_connection.connect()
    db_connection.seed('seeds/spaces.sql')

    repository = SpaceRepository(db_connection)
    
    login("bob@example.com", "password2")

    page.goto(f"http://{test_web_address}/my_spaces/add")

    page.get_by_label("Name").fill('Neptune')
    page.get_by_label("Description").fill('For the water lovers')
    page.get_by_label("Available From").fill('2026-04-25')
    page.get_by_label("Available To").fill('2027-04-25')
    page.get_by_label("Price (per night)").fill('220')
    page.get_by_label("Upload Image of Space").set_input_files("static/neptune.jpg")
    page.get_by_role("button", name="Submit").click()


    spaces = page.locator('h3').all_inner_texts()

    user_spaces = repository.find_by_owner_id(2)
    space_names = [user_space.name for user_space in user_spaces]
    assert space_names == spaces