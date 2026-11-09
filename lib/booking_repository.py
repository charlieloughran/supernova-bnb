from lib.booking import Booking

class BookingRepository:

    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from bookings')
        bookings = []
        for row in rows:
            item = Booking(row["id"], row["space_id"], row["booked_by"], row["date"], row["status"])
            bookings.append(item)
        return bookings

    def find(self, booking_id):
        rows = self._connection.execute(
            'SELECT * from bookings WHERE id = %s', [booking_id])
        row = rows[0]
        return Booking(row["id"], row["space_id"], row["booked_by"], row["date"], row["status"])

    def create(self, booking):
        self._connection.execute('INSERT INTO bookings (space_id, booked_by, date, status) VALUES (%s, %s, %s, %s)', [
                                booking.space_id, booking.booked_by, booking.date, booking.status])
        return None

    def delete(self, booking_id):
        self._connection.execute(
            'DELETE FROM bookings WHERE id = %s', [booking_id])
        return None
