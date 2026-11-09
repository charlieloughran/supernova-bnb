# Design Recipe

## 1. Overview and Problem Statement



- **Problem**: 

- **Solution** 

---

## 2. Roles

**Space Owner:** 
**User:** 

---

## 3. User Stories

### Admin


### User




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
    - `role` (Enum: 'admin', 'actor')

2. `spaces`
    - `id`
    - `name`
    - `description`
    - `user_id (owner)`
    - `availability_start_date`
    - `availability_end_date`
    - `price_per_night`
    - `image_url`

3. `booking`
    - `id`
    - `booked_by`
    - `date`
    - `confirmation`
    - `space_id`




## 6. Routes


-- Sign Up & Login

GET '/login' --> shows the login form
POST '/login/new' --> Sends the login data to the database

GET '/users' --> shows the registration form
POST '/users/new' --> Sends the user data to the database
 


##### LATER FEATURES

-


