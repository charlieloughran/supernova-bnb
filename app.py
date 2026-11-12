import os

from lib.user import User
from lib.user_repository import UserRepository
from flask import Flask, request, render_template, redirect, session, abort, flash
from lib.database_connection import *
from lib.space_repository import *
from lib.space import Space
from lib.booking_repository import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import date


# Create a new Flask app
app = Flask(__name__)
app.secret_key = 'some_really_secret_key'

# == Your Routes Here ==
def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login/new')
        return f(*args, **kwargs)
    return decorated_func

def update_expired_bookings(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        db_connection = get_flask_database_connection(app)
        booking_repository = BookingRepository(db_connection)
        booking_repository.update_expired_bookings()
        return f(*args, **kwargs)
    return decorated_func

def user_owns_space(space: Space):
    return space.owner_id == session.get("user_id")

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
@update_expired_bookings
def get_space_details(space_id):
    db_connection = get_flask_database_connection(app)

    # find space details
    space_repository = SpaceRepository(db_connection)
    space = space_repository.find(space_id)

    # find accepted bookings for space
    booking_repository = BookingRepository(db_connection)
    bookings = booking_repository.find_by_space_and_status(space_id, 'accepted')
    booked_dates = [booking.date.strftime('%Y-%m-%d') for booking in bookings]

    return render_template('space.html', space=space, booked_dates=booked_dates, today=date.today(), is_owner=user_owns_space(space))

@app.route('/spaces/<int:space_id>', methods=['POST'])
@login_required
def request_booking(space_id):
    db_connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(db_connection)
    space_repository = SpaceRepository(db_connection)
    
    # find space availability dates
    space_details = space_repository.find(space_id)
    
    if user_owns_space(space_details):
        # raise error if the user owns the space
        flash("You cannot book your own space.", 'error')
        return redirect(f'/spaces/{space_id}')

    # get date from form and user_id from session data
    if request.form['booking_date'] == '':
        # raise error if no date inputted
        flash('Please select a date.', 'error')
        return redirect(f'/spaces/{space_id}')
            
    booking_date = datetime.strptime(
        request.form['booking_date'], '%Y-%m-%d'
        ).date()
    booked_by = session["user_id"]

    # find already accepted bookings
    accepted_bookings = booking_repository.find_by_space_and_status(space_id, 'accepted')

    accepted_bookings_same_date = [booking for booking in accepted_bookings if booking.date == booking_date]

    min_date = max(date.today(), space_details.availability_start_date)
    max_date = space_details.availability_end_date
    
    if accepted_bookings_same_date != []:
        # raise error if date is already booked
        flash('Sorry, this date is already booked. Please select another date.', 'error')
        return redirect(f'/spaces/{space_id}')

    elif booking_date < min_date:
        # raise error if booking date is in the past
        flash('The date selected is in the past. Please select a date available on the calendar.', 'error')
        return redirect(f'/spaces/{space_id}')

    elif booking_date > max_date:
        # raise error if space isn't available to book on date
        flash('Sorry, the space is unavailable on this date. Please select a date available on the calendar', 'error')
        return redirect(f'/spaces/{space_id}')

    else:
        # create the booking
        booking = Booking(space_id, booked_by, booking_date, 'requested')
        booking_repository.create(booking)

        # success message
        flash("Your booking request has been submitted!", "success")
        return redirect(f'/spaces/{space_id}')

@app.route('/my_spaces', methods=['GET'])
@login_required
def get_my_spaces():
    print("ROUTE HIT")
    db_connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(db_connection)

    #Gets Username/User ID from session
    all_spaces = space_repo.find_by_owner_id(session["user_id"]) #Passes Username/ User ID as parameter

    # Lists all user spaces on my-spaces template
    return render_template('my-spaces.html', spaces=all_spaces)

@app.route("/bookings", methods=["GET"])
@login_required
@update_expired_bookings
def get_bookings():
    db_connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(db_connection)
    space_repo = SpaceRepository(db_connection)

    spaces = space_repo.all()
    spaces_by_id = {space.id: space for space in spaces}

    user_bookings = booking_repo.find_by_user_id(session["user_id"])

    bookings_by_status = {
        "requested": [],
        "accepted": [],
        "declined": [],
        "expired": [],
    }
    for booking in user_bookings:
        bookings_by_status[booking.status].append(booking)

    return render_template("bookings.html", bookings=user_bookings, spaces_by_id=spaces_by_id,bookings_by_status=bookings_by_status)

@app.route('/bookings/<int:id>')
@login_required
@update_expired_bookings
def get_booking(id):
    db_connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(db_connection)
    booking = booking_repo.find_by_booking(id)
    if booking is None:
        abort(404)
    return render_template('booking.html', booking=booking)
    
@app.route('/my_spaces/add', methods=['GET'])
@login_required
def show_add_a_space_form():
    return render_template('add-space.html')

@app.route('/my_spaces/new', methods=['POST'])
@login_required
def add_a_space():
    db_connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(db_connection)
    space_details = request.form

    image_file = request.files.get('image-url')
    image_path = None

    if image_file and image_file.filename != '':
        filename = secure_filename(image_file.filename)

        upload_folder = os.path.join('static')
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        image_file.save(file_path)

        image_path = f"/static/{filename}"


    space = Space(space_details["space-name"], space_details["space-description"], datetime.strptime(space_details['availability-start-date'], '%Y-%m-%d').date(), datetime.strptime(space_details['availability-end-date'], '%Y-%m-%d').date(), space_details["price-per-night"], image_path, session['user_id'], None)

    space_repo.create(space)

    return redirect('/my_spaces')


@app.route('/my_spaces/requests', methods=['GET'])
@login_required
@update_expired_bookings
def see_list_of_requests():
    db_connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(db_connection)

    user_bookings = booking_repo.find_by_user_and_status(session["user_id"], "requested")

    return render_template('requests.html' , bookings=user_bookings)


@app.route('/my_spaces/requests/<int:id>/accept', methods=['POST'])
@login_required
def accept_requests(id):
    db_connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(db_connection)
    booking_repo.update(id, "accepted")

    return redirect('/my_spaces/requests')

@app.route('/logout', methods=['get'])
@login_required
def logout():
    session.clear()
    return redirect('/')

@app.route('/my_spaces/requests/<int:id>/deny', methods=['POST'])
@login_required
def deny_requests(id):
    db_connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(db_connection)
    booking_repo.update(id, "declined")

    return redirect('/my_spaces/requests')

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
