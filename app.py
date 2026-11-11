import os
from flask import Flask, request, render_template, abort
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
@app.route('/', methods=['GET'])
def get_index():
    connection = get_flask_database_connection(app)
    connection.connect()
    repo = SpaceRepository(connection)
    spaces = repo.all()
    
    return render_template('index.html',spaces=spaces)

# GET route gets details of the space for the space details page
@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_space_details(space_id):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()

    # find space details
    space_repository = SpaceRepository(connection)
    space = space_repository.find(space_id)

    # find accepted bookings for space
    booking_repository = BookingRepository(connection)
    bookings = booking_repository.find_by_space_and_status(space_id, 'accepted')
    booked_dates = [booking.date.strftime('%Y-%m-%d') for booking in bookings]

    return render_template('space.html', space=space, booked_dates=booked_dates)


@app.route('/my_spaces', methods=['GET'])
def get_my_spaces():
    db_connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(db_connection)

    #Gets Username/User ID from session

    all_spaces = space_repo.find_by_owner_id(2) #Passes Username/ User ID as parameter

    # Lists all user spaces on my-spaces template
    return render_template('my-spaces.html', spaces=all_spaces)

@app.route('/bookings', methods=['GET'])
def get_bookings():
    db_connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(db_connection)
    
    #Gets Username/User ID from session
    # user_bookings = booking_repo.find_by_user_id(session["user_id"])
    
    user_bookings = booking_repo.find_by_user_id(2) 
    
    #Lists all bookings relating to the authenticated user
    return render_template('bookings.html', bookings=user_bookings)

@app.route('/bookings/<int:id>')
def get_booking(id):
    db_connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(db_connection)
    booking = booking_repo.find_by_booking(id)
    if booking is None:
        abort(404)
    return render_template('booking.html', booking=booking)
    
# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
