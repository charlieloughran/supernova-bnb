import os
from lib.user import User
from lib.user_repository import UserRepository
from flask import Flask, request, render_template, redirect, session
from lib.database_connection import *
from lib.space_repository import *
from lib.booking_repository import *
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


# Create a new Flask app
app = Flask(__name__)
app.secret_key = 'some_really_secret_key'

# == Your Routes Here ==
def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('login/new')
        return f(*args, **kwargs)
    return decorated_func

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

@app.route('/register/new', methods=['GET'])
def get_signup_form():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def create_user():
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    user_details = request.form

    if user_repository.find_by_email(user_details["email"]) is not None:
        return render_template(
            'signup.html', 
            error="An account with that email already exists.",
            name=user_details["name"],
            email=user_details["email"]
        )
    
    user_repository.create(
        user = User(name=user_details["name"], 
                    email=user_details["email"], 
                    password_hash=generate_password_hash(user_details["password"], "scrypt:32768:8:1"))
    )
    
    return redirect('/login/new', code=302)

@app.route('/login/new', methods=['GET'])
def get_login_form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def create_session():
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    email = request.form["email"]
    password = request.form["password"]

    user = user_repository.find_by_email(email)
    if user is not None and check_password_hash(user.password_hash, password):
        session["user_id"] = user.id
        session["name"] = user.name
        session["email"] = user.email
        return redirect('/')
    else:
        return render_template(
            'login.html', 
            error="Incorrect email or password.",
            email=email
        )

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

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    test_mode = os.environ.get('APP_ENV') == 'test'
    app.run(
        debug=not test_mode,
        use_reloader=not test_mode,
        port=int(os.environ.get('PORT', 5001)),
    )
