from lib.booking_repository import *
from lib.booking import *
from datetime import date
from lib.database_connection import DatabaseConnection

"""
When we call BookingRepository#all
We get a list of Booking objects reflecting the seed data.
"""
def test_get_all_records(db_connection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.all()

    assert bookings == [
        Booking(3, 2, date(2027, 3, 1), 'requested', 1),
        Booking(2, 1, date(2027, 1, 1), 'declined', 2),
        Booking(2, 4, date(2027, 1, 2), 'accepted', 3),
        Booking(1, 2, date(2027, 2, 11), 'requested', 4),
        Booking( 2, 2, date(2027, 2, 11), 'requested', 5)
    ]

"""
When we call BookingRepository#find_by_booking
We get a single Booking object reflecting the seed data.
"""
def test_get_single_record(db_connection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)

    booking = repository.find_by_booking(3)
    assert booking == Booking(2, 4, date(2027, 1, 2), 'accepted', 3)

"""
When we call BookingRepository#find_by_space_and_status
We get a list of bookings for the specified space.
"""
def test_get_accepted_bookings_for_space(db_connection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.find_by_space_and_status(2, "accepted")
    assert bookings == [
                        Booking(2, 4, date(2027, 1, 2), 'accepted', 3),
                        ]


"""
When we call BookingRepository#find_by_user_and_status
We get a list of all booking requests for the specified user.
"""
def test_get_owner_bookings_for_space(db_connection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.find_by_user_and_status(2, "requested")
    assert bookings == [
            Booking(2, 2, date(2027, 2, 11), 'requested', 5),
        ]

"""
When we call BookingRepository#create
We get a new record in the database.
"""
def test_create_record(db_connection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)

    repository.create(Booking(3, 3, date(2027, 3, 11), 'requested'))

    result = repository.all()
    assert result == [
        Booking(3, 2, date(2027, 3, 1), 'requested', 1),
        Booking(2, 1, date(2027, 1, 1), 'declined', 2),
        Booking(2, 4, date(2027, 1, 2), 'accepted', 3),
        Booking(1, 2, date(2027, 2, 11), 'requested', 4),
        Booking( 2, 2, date(2027, 2, 11), 'requested', 5),
        Booking(3, 3, date(2027, 3, 11), 'requested', 6)
        
    ]

"""
When we call BookingRepository#delete
We remove a record from the database.
"""
def test_delete_record(db_connection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)
    repository.delete(3)

    result = repository.all()
    assert result == [
        Booking(3, 2, date(2027, 3, 1), 'requested', 1),
        Booking(2, 1, date(2027, 1, 1), 'declined', 2),
        Booking(1, 2, date(2027, 2, 11), 'requested', 4),
        Booking(2, 2, date(2027, 2, 11), 'requested', 5),

    ]

"""
When we call BookingRepository#update
We update the specified booking record's status in the database.
"""
def test_update_record(db_connection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)
    repository.update(1, 'accepted')

    result = repository.all()
    assert result == [
        Booking(3, 2, date(2027, 3, 1), 'accepted', 1),
        Booking(2, 1, date(2027, 1, 1), 'declined', 2),
        Booking(2, 4, date(2027, 1, 2), 'accepted', 3),
        Booking(1, 2, date(2027, 2, 11), 'requested', 4),
        Booking(2, 2, date(2027, 2, 11), 'requested', 5),

    ]
    
"""
When we call BookingRepository#find_by_user
it returns the specified's user bookings
"""

def test_find_by_user_id_returns_their_bookings(db_connection: DatabaseConnection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)
    
    result = repository.find_by_user_id(2)
    
    assert result == [
        Booking(3, 2, date(2027, 3, 1), 'requested', 1),
        Booking(1, 2, date(2027, 2, 11), 'requested', 4),
        Booking(2, 2, date(2027, 2, 11), 'requested', 5)
    ] 


"""
When we call BookingRepository#update_expired_bookings
We update the status of all bookings with date in the past to 'expired'
"""
def test_update_record(db_connection):
    db_connection.seed("seeds/expired_bookings.sql")
    repository = BookingRepository(db_connection)
    repository.update_expired_bookings()

    result = repository.all()
    assert result == [
        Booking(3, 2, date(2025, 3, 1), 'expired', 1),
        Booking(2, 1, date(2024, 1, 1), 'expired', 2),
        Booking(2, 4, date(2026, 1, 2), 'expired', 3),
        Booking(1, 2, date(2027, 2, 11), 'requested', 4),
        Booking(2, 2, date(2027, 2, 11), 'requested', 5),

    ]
