# Design Recipe

## 1. Overview

We would like a web application that allows users to list spaces they have available, and to hire spaces for the night

- Any signed-up user can list a new space.
- Users can list multiple spaces.
- Users should be able to name their space, provide a short description of the space, and a price per night.
- Users should be able to offer a range of dates where their space is available.
- Any signed-up user can request to hire any space for one night, and this should be approved by the user that owns that space.
- Nights for which a space has already been booked should not be available for users to book that space.
- Until a user has confirmed a booking request, that space can still be booked for that night.

---

## 2. Roles

**Space Owner:** Lists the spaces and accepts bookings
**Booking Maker:** Looks for spaces and requests bookings


---

## 3. User Stories


**Space Owner:** 

As a Space Owner, I would like to create an account so that I can list my spaces.
As a Space Owner, I would like to add a new space to spaces list.
As a Space Owner, I would like to be able to add multiple spaces to spaces list.
As a Space Owner, I would like to share the name, description and price per night for my space.
As a Space Owner, I would like to offer a range of dates when my space is available.
As a Space Owner, I would like to approve requests made my Booking Makers.
As a Space Owner, I would like to still receive requests after a booking request has been made.

**Booking Maker:** 
As a Booking Maker, I would like to request to book any space for one night.
As a Booking Maker, I would like to see when a space is available.
As a Booking Maker, I would like to see a list of all spaces
As a Booking Maker, I would like to see if my booking has been accepted or declined.


---


## 4. Technical Architecture & Tech Stack
- **Language:** Python 3.13.8
- **Web Framework:** Flask
- **Database:** PostgreSQL
- **Authentication**:
- **Testing:** `pytest` 


---


## 5. Data Model (PostgreSQL Schema)

### Tables & Attributes


1. `users`
    - `id` (Primary Key, Serial/Integer)
    - `name` (String, Not Null)
    - `email` (String, Unique, Not Null)
    - `password_hash` (String, Not Null)


2. `spaces`
    - `id` (Primary Key, Serial/Integer)
    - `name` (String, Not Null)
    - `description` (String, Not Null)
    - `user_id (owner)` int
    - `availability_start_date` date
    - `availability_end_date` date
    - `price_per_night` float
    - `image_url` url

3. `booking`
    - `id` (Primary Key, Serial/Integer)
    - `space_id` int
    - `booked_by` int (user_id) Foreign key
    - `date` date
    - `status` string (requested, accepted, declined)


## 6. Classes

class User

class UserRepository

class Space

class SpaceRepository

class Booking

class BookingRepository



## 7. Routes


==== SIGN UP & LOGIN ====

GET '/login' --> shows the login form
POST '/login/new' --> Sends the login data to the database

GET '/register' --> shows the registration form
POST '/register/new' --> Sends the user data to the database



==== SPACES ====

-- Space Owner --

GET '/my-spaces' --> shows a list of all the space owners spaces

GET '/my-spaces/add' --> shows form to add details for the space

POST 'my-spaces/new' --> sends new space details to database and adds to list

GET 'my-spaces/bookings/requested' --> shows a list of booking requests for your spaces

GET 'my-spaces/bookings/requested/<booking_id>' --> shows the details of the booking for that space

POST 'my-spaces/bookings/requested/<booking_id>/accept' --> Accepts the booking, updates status of the row in db

POST 'my-spaces/bookings/requested/<booking_id>/deny' --> Deny the booking, updates status of the row in db

GET 'my-spaces/bookings/accepted' --> shows a list of bookings accepted for your spaces

-- Booker --

GET 'spaces/<space_id>' --> shows the details of the space to the customer and form containing available dates to book

POST 'spaces/<space_id>/book --> requests a booking for a space, sending form data to db

GET 'spaces/<space_id>/booking_requested' --> booking requested page




==== BOOKINGS ===

GET 'bookings/<booking_id> --> he space and the details





 


##### LATER FEATURES

-


