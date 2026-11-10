from lib.space import Space

"""
Space constructs with a name, description, start date, end date, price per night, image url and the owner ID
"""
def test_space_constructs():
    space = Space("Test", "For the test lovers", "2026-05-09", "2026-05-09", 220.14, "static/test-space.png", 1, 1)
    assert space.id == 1
    assert space.name == "Test"
    assert space.description == "For the test lovers"
    assert space.availability_start_date == "2026-05-09"
    assert space.availability_end_date == "2026-05-09"
    assert space.price_per_night == 220.14
    assert space.image_url == "static/test-space.png"
    assert space.owner_id == 1
   
"""
Format spaces to strings nicely
"""
def test_spaces_format_nicely():
    space = Space("Test", "For the test lovers", "2026-05-09", "2026-05-09", 220.14, "static/test-space.png", 1, 1)
    assert str(space) == f"Space(Test, For the test lovers, 2026-05-09, 2026-05-09, 220.14, static/test-space.png, 1, 1)"


"""
We can compare two identical spaces
And have them be equal
"""
def test_spaces_are_equal():
    space1 = Space("Test", "For the test lovers", "2026-05-09", "2026-05-09", 220.14, "static/test-space.png", 1, 1)
    space2 = Space("Test", "For the test lovers", "2026-05-09", "2026-05-09", 220.14, "static/test-space.png", 1, 1)
    assert space1 == space2

