from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection
from lib.space_repository import SpaceRepository

"""
Render a list of all spaces
"""

def test_my_spaces_list_shown(page: Page, test_web_address):
    db_connection = DatabaseConnection(test_mode=True)
    db_connection.connect()
    db_connection.seed('seeds/spaces.sql')

    repository = SpaceRepository(db_connection) 
    user_spaces = repository.find_by_owner_id(2)
    space_names = [space.name for space in user_spaces]

    page.goto(f"http://{test_web_address}/my_spaces")


    

    spaces = page.locator('.space-name')


    assert space_names == spaces.all_inner_texts()




