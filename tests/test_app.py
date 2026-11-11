from playwright.sync_api import Page, expect
from lib.space_repository import *

# Tests for your routes go here

"""
We can render the index page
"""
def test_get_index(db_connection,page, test_web_address):
    db_connection.seed("seeds/spaces.sql") 
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/")
    
    # We look at the h1 tag
    h_tag = page.locator("h1")
    

    # We assert that it has the text "This is the homepage."
    expect(h_tag).to_contain_text("Welcome")

"""
We can read all the spaces from the db and display them on the index page
"""

def test_index_gets_spaces(db_connection, page, test_web_address):
    db_connection.seed("seeds/spaces.sql") 
    repository = SpaceRepository(db_connection) 
    page.goto(f"http://{test_web_address}/")
    
    space_card_headers = page.locator('.space_card_header > h3')
    
    space_repo = SpaceRepository(db_connection)
    spaces = space_repo.all()
    space_names = [space.name for space in spaces]
    
    expect(space_card_headers).to_contain_text(space_names)
