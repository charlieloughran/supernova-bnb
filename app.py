import os
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection
from lib.space_repository import SpaceRepository
from lib.booking_repository import BookingRepository

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
    
# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
