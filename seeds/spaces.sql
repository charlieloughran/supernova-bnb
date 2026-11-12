DROP TABLE IF EXISTS spaces;
DROP SEQUENCE IF EXISTS spaces_seq_id; 


CREATE SEQUENCE IF NOT EXISTS spaces_seq_id;
CREATE TABLE spaces (

    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    availability_start_date DATE,
    availability_end_date DATE,
    price_per_night FLOAT,
    image_url TEXT,
    owner_id INT


);


INSERT INTO spaces (name, description, availability_start_date, availability_end_date, price_per_night, image_url, owner_id) 
VALUES
    ('Mercury', 'For the queen worshipers', '2026-04-25', '2027-04-25', 220.13, 'static/mercury-space.png', 1),
    ('Venus', 'For the fly trap lovers', '2026-04-25', '2027-04-25', 220.13, 'static/venus-space.png', 2),
    ('Earth', 'For the life lovers', '2026-04-25', '2027-04-25', 220.13, 'static/earth-space.png', 3),
    ('Mars', 'For the wanna-be earth leavers', '2026-04-25', '2027-04-25', 220.13, 'static/mars-space.png', 4),
    ('Jupiter', 'For the grand regent lovers', '2026-04-25', '2027-04-25', 220.13, 'static/jupiter-space.png', 5),
    ('Saturn', 'For the ring lovers', '2026-04-25', '2027-04-25', 220.13, 'static/saturn-space.png', 2),
    ('Uranus', 'For the lovers', '2026-12-25', '2027-04-25', 220.13, 'static/uranus-space.png', 3);