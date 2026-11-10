from lib.booking import *

"""
Booking constructs with an id, space_id, booked_by, date, status
"""
def test_booking_constructs():
    booking = Booking(3, 2, "2027-01-01", 'requested', 3)
    assert booking.id == 3
    assert booking.space_id == 3
    assert booking.booked_by == 2
    assert booking.date == "2027-01-01"
    assert booking.status == 'requested'

"""
We can format bookings to strings nicely
"""
def test_bookings_format_nicely():
    booking = Booking(3, 2, "2027-01-01", 'requested', 1)
    assert str(booking) == "Booking(3, 2, 2027-01-01, requested, 1)"

"""
We can compare two identical bookings
And have them be equal
"""
def test_bookings_are_equal():
    booking1 = Booking(3, 2, "2027-01-01", 'requested', 1)
    booking2 = Booking(3, 2, "2027-01-01", 'requested', 1)
    assert booking1 == booking2