from lib.booking_repository import *
from lib.booking import *
from datetime import date

"""
When we call BookingRepository#all
We get a list of Booking objects reflecting the seed data.
"""
def test_get_all_records(db_connection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.all()

    assert bookings == [
        Booking(1, 3, 2, date(2027, 3, 1), 'requested'),
        Booking(2, 2, 1, date(2027, 1, 1), 'declined'),
        Booking(3, 2, 4, date(2027, 1, 2), 'accepted'),
        Booking(4, 1, 2, date(2027, 2, 11), 'requested')
    ]

"""
When we call BookingRepository#find
We get a single Booking object reflecting the seed data.
"""
def test_get_single_record(db_connection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)

    booking = repository.find(3)
    assert booking == Booking(3, 2, 4, date(2027, 1, 2), 'accepted')

"""
When we call BookingRepository#create
We get a new record in the database.
"""
def test_create_record(db_connection):
    db_connection.seed("seeds/bookings.sql")
    repository = BookingRepository(db_connection)

    repository.create(Booking(None, 3, 3, date(2027, 3, 11), 'requested'))

    result = repository.all()
    assert result == [
        Booking(1, 3, 2, date(2027, 3, 1), 'requested'),
        Booking(2, 2, 1, date(2027, 1, 1), 'declined'),
        Booking(3, 2, 4, date(2027, 1, 2), 'accepted'),
        Booking(4, 1, 2, date(2027, 2, 11), 'requested'),
        Booking(5, 3, 3, date(2027, 3, 11), 'requested')
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
        Booking(1, 3, 2, date(2027, 3, 1), 'requested'),
        Booking(2, 2, 1, date(2027, 1, 1), 'declined'),
        Booking(4, 1, 2, date(2027, 2, 11), 'requested')
    ]
