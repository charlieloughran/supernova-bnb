
# Page Requirements & Implementation Tasks

Alright y'all, there are a few things required on each page, so I'm just keeping everything documented here.

Work in whatever order you see fit. When we meet back up, we can review where we've ended up.

**Don't worry about the navigation bar at the top.** It'll be handled separately in a reusable component that I'm taking care of.

---

## 1. My Spaces Page

- The **Add Space** link/button should direct users to the `/spaces/new` page.

- The **Accept/Deny** buttons should make a `POST` request to the `/spaces/<id>` route.
  - The request should contain the result of the user's selection (Accept or Deny).
  - This result should then be used to update the database.

### Booking Check

- When routing to this page, perform a check to see whether any booking associated with the current session owner's `user_id` appears in the `booked_by` column of any booking.
- If a matching booking exists, only the **Requests** section at the bottom of the page should be generated/displayed.

---

## 2. Space Details Page (`/spaces/<id>`)

- The **Reserve** button/link should make a `POST` request to the `/bookings/<id>` route.

- Within this route:
  - A new booking should be created.
  - The booking should contain all the necessary information.
  - The relevant information should be saved to the database.

---

## 3. Login & Signup Pages

- The login and signup forms should make `POST` requests to the appropriate sessions routes.

- The naming of the sessions routes is up to you. For example, `/sessions/new` or `/sessions/create` – use whatever makes the most sense.

### Navigation Links

- The small purple links at the bottom of the pages (not the large purple button/link) should navigate between the login and account creation pages.
- The route names are up to you.

---

## General Notes

- Use your discretion when implementing the requirements.
- Route naming conventions are flexible.
- Ensure all relevant database operations are handled by the Flask backend.
- Use `POST` requests for actions that create or update database records.
