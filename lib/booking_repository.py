from lib.booking import Booking

class BookingRepository:

    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from bookings order by id')
        bookings = []
        for row in rows:
            item = Booking(row["space_id"], row["booked_by"], row["date"], row["status"], row["id"])
            bookings.append(item)
        return bookings

    def find_by_booking(self, booking_id):
        rows = self._connection.execute(
            'SELECT * from bookings WHERE id = %s', [booking_id])
        row = rows[0]
        return Booking(row["space_id"], row["booked_by"], row["date"], row["status"], row["id"])

    def find_by_space_and_status(self, space_id, booking_status):
        rows = self._connection.execute(
            'SELECT * from bookings WHERE space_id = %s and status = %s', [space_id, booking_status])
        bookings = []
        for row in rows:
            item = Booking(row["space_id"], row["booked_by"], row["date"], row["status"], row["id"])
            bookings.append(item)
        return bookings

    def create(self, booking):
        self._connection.execute('INSERT INTO bookings (space_id, booked_by, date, status) VALUES (%s, %s, %s, %s)', [
                                booking.space_id, booking.booked_by, booking.date, booking.status])
        return None

    def delete(self, booking_id):
        self._connection.execute(
            'DELETE FROM bookings WHERE id = %s', [booking_id])
        return None

    def update(self, booking_id, new_status):
        self._connection.execute(
            'UPDATE bookings SET status = %s WHERE id = %s', [new_status, booking_id]
        )
        return None