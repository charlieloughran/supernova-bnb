import os
from flask import Flask, request, render_template, redirect
from lib.database_connection import get_flask_database_connection
from lib.space_repository import SpaceRepository
from lib.space import Space
from datetime import datetime

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
    print("ROUTE HIT")
    db_connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(db_connection)

    #Gets Username/User ID from session
    all_spaces = space_repo.find_by_owner_id(2) #Passes Username/ User ID as parameter

    # Lists all user spaces on my-spaces template
    return render_template('my-spaces.html', spaces=all_spaces)

@app.route('/my_spaces/add', methods=['GET'])
def show_add_a_space_form():
    return render_template('add-space.html')

@app.route('/my_spaces/new', methods=['POST'])
def add_a_space():
    db_connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(db_connection)
    space_details = request.form


    space = Space(space_details["space-name"], space_details["space-description"], datetime.strptime(space_details['availability-start-date'], '%Y-%m-%d').date(), datetime.strptime(space_details['availability-end-date'], '%Y-%m-%d').date(), space_details["price-per-night"], space_details["image-url"], 2, None)

    space_repo.create(space)

    return redirect('/my_spaces')

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
