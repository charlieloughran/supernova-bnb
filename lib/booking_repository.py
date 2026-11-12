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
        if not rows:
            return None
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

    def find_by_user_and_status(self, owner_id, booking_status):
        rows = self._connection.execute(
            'SELECT bookings.id AS id, space_id, booked_by, date, status FROM bookings JOIN spaces ON bookings.space_id = spaces.id WHERE owner_id = %s and status = %s', [owner_id, booking_status])
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
            'UPDATE bookings ' \
            'SET status = %s ' \
            'WHERE id = %s ', [new_status, booking_id]
        )
        return None

    def update_expired_bookings(self):
        self._connection.execute(
            'UPDATE bookings ' \
            'SET status = %s ' \
            'WHERE date < CURRENT_DATE and status != %s ', ['expired', 'expired']
        )
        return None
    
    def find_by_user_id(self, user_id: int) -> list[Booking]:
        rows = self._connection.execute(
            '''
            SELECT * FROM bookings
            WHERE booked_by = %s
            ORDER BY id
            ''', [user_id]
        )
        return [
            Booking(row["space_id"], row["booked_by"], row["date"], row["status"], row["id"])
            for row in rows
        ]