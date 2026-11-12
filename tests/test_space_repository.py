from lib.space_repository import SpaceRepository
from lib.space import Space
from datetime import date
"""
When we call SpaceRepository#all
We get a list of Space objects reflecting the seed data.
"""
def test_get_all_records(db_connection): 
    db_connection.seed("seeds/spaces.sql") 
    repository = SpaceRepository(db_connection) 

    spaces = repository.all()

    # Assert on the results
    assert spaces == [
        Space('Mercury', 'For the queen worshipers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/mercury-space.png', 1, 1),
        Space('Venus', 'For the fly trap lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/venus-space.png', 2, 2),
        Space('Earth', 'For the life lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/earth-space.png', 3, 3),
        Space('Mars', 'For the wanna-be earth leavers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/mars-space.png', 4, 4),
        Space('Jupiter', 'For the grand regent lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/jupiter-space.png', 5, 5),
        Space('Saturn', 'For the ring lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/saturn-space.png', 2, 6),
        Space('Uranus', 'For the lovers', date(2026, 12, 25), date(2027, 4, 25), 220.13, 'static/uranus-space.png', 3, 7)
    ]

"""
When we call SpaceRepository#find
We get a single Space object reflecting the seed data.
"""
def test_get_single_record(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repository = SpaceRepository(db_connection)

    space = repository.find(3)
    assert space == Space('Earth', 'For the life lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/earth-space.png', 3, 3)




"""
When we call SpaceRepository#create
We get a new record in the database.
"""
def test_create_record(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repository = SpaceRepository(db_connection)

    repository.create(Space('Neptune', 'For the water lovers', '2026-04-25', '2027-04-25', 220.13, 'static/neptune-space.png', 3, None))

    result = repository.all()
    assert result == [
        Space('Mercury', 'For the queen worshipers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/mercury-space.png', 1, 1),
        Space('Venus', 'For the fly trap lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/venus-space.png', 2, 2),
        Space('Earth', 'For the life lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/earth-space.png', 3, 3),
        Space('Mars', 'For the wanna-be earth leavers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/mars-space.png', 4, 4),
        Space('Jupiter', 'For the grand regent lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/jupiter-space.png', 5, 5),
        Space('Saturn', 'For the ring lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/saturn-space.png', 2, 6),
        Space('Uranus', 'For the lovers', date(2026, 12, 25), date(2027, 4, 25), 220.13, 'static/uranus-space.png', 3, 7),
        Space('Neptune', 'For the water lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/neptune-space.png', 3, 8)

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
        Space('Mercury', 'For the queen worshipers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/mercury-space.png', 1, 1),
        Space('Venus', 'For the fly trap lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/venus-space.png', 2, 2),
        Space('Mars', 'For the wanna-be earth leavers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/mars-space.png', 4, 4),
        Space('Jupiter', 'For the grand regent lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/jupiter-space.png', 5, 5),
        Space('Saturn', 'For the ring lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/saturn-space.png', 2, 6),
        Space('Uranus', 'For the lovers', date(2026, 12, 25), date(2027, 4, 25), 220.13, 'static/uranus-space.png', 3, 7),

    ]

"""
When we call SpaceRepository#find_by_owner_id
We find all records with the owner id specified.
"""

def test_find_by_owner(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repository = SpaceRepository(db_connection)
    user_spaces = repository.find_by_owner_id(2)

    assert user_spaces == [
        Space('Venus', 'For the fly trap lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/venus-space.png', 2, 2),
        Space('Saturn', 'For the ring lovers', date(2026, 4, 25), date(2027, 4, 25), 220.13, 'static/saturn-space.png', 2, 6)
    ]