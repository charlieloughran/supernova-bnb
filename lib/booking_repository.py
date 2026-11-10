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

    def find(self, booking_id: int) -> Booking | None:
        rows = self._connection.execute(
            'SELECT * from bookings WHERE id = %s', [booking_id])
        if not rows:
            return None
        row = rows[0]
        return Booking(row["space_id"], row["booked_by"], row["date"], row["status"], row["id"])

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