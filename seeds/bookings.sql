DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS bookings_id_seq;

CREATE SEQUENCE IF NOT EXISTS bookings_id_seq;
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    space_id INT,
    booked_by INT,
    date DATE,
    status VARCHAR(20) CHECK (
        status IN ('requested', 'accepted', 'declined', 'expired')
    )
);

INSERT INTO bookings (space_id, booked_by, date, status) VALUES (3, 2, '2027-03-01', 'requested');
INSERT INTO bookings (space_id, booked_by, date, status) VALUES (2, 1, '2027-01-01', 'declined');
INSERT INTO bookings (space_id, booked_by, date, status) VALUES (2, 4, '2027-01-02', 'accepted');
INSERT INTO bookings (space_id, booked_by, date, status) VALUES (1, 2, '2027-02-11', 'requested');
INSERT INTO bookings (space_id, booked_by, date, status) VALUES (2, 2, '2027-02-11', 'requested'); --- Added in to test link between spaces and bookings (joining on space_id)