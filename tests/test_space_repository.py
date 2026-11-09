from lib.space_repository import SpaceRepository
from lib.space import Space

"""
When we call SpaceRepository#all
We get a list of Space objects reflecting the seed data.
"""
def test_get_all_records(db_connection): # See conftest.py to learn what `db_connection` is.
    db_connection.seed("seeds/spaces.sql") # Seed our database with some test data
    repository = SpaceRepository(db_connection) # Create a new SpaceRepository

    spaces = repository.all() # Get all spaces

    # Assert on the results
    assert spaces == [

    ]

"""
When we call SpaceRepository#find
We get a single Space object reflecting the seed data.
"""
def test_get_single_record(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repository = SpaceRepository(db_connection)

    space = repository.find(3)
    assert space == Space()




"""
When we call SpaceRepository#create
We get a new record in the database.
"""
def test_create_record(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repository = SpaceRepository(db_connection)

    repository.create(Space())

    result = repository.all()
    assert result == [


    ]

"""
When we call SpaceRepository#delete
We remove a record from the database.
"""
def test_delete_record(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repository = SpaceRepository(db_connection)
    repository.delete(3)

    spaces = repository.all()
    assert spaces == [

    ]