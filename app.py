import os
from flask import Flask, request, render_template
from lib.database_connection import *
from lib.space_repository import *
from lib.booking_repository import *

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

# GET route gets details of the space for the space details page
@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_space_details(space_id):
    connection = DatabaseConnection()
    connection.connect()

    # find space details
    space_repository = SpaceRepository(connection)
    space = space_repository.find(space_id)

    # find accepted bookings for space
    booking_repository = BookingRepository(connection)
    bookings = booking_repository.find_by_space_and_status(space_id, 'accepted')
    booked_dates = [booking.date.strftime('%Y-%m-%d') for booking in bookings]

    return render_template('space.html', space=space, booked_dates=booked_dates)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
