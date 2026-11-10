
-- users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

TRUNCATE TABLE users RESTART IDENTITY CASCADE;

INSERT INTO users (name, email, password_hash) VALUES
    ('Alice Smith', 'alice@example.com', 'scrypt:32768:8:1$dX7yMVwcr8bFDmSV$11d5684e50c856f11547e10f48a49e5b2652f4367285d4ddb7e619d20cbae433e77bc6c8d4fbac8872cf20b785be576f5ecf49e850bd801541e93332a63ec9b1'),
    ('Bob Jones', 'bob@example.com', 'scrypt:32768:8:1$BQZpr0h9sjyBYAN3$81ee601f3d0181f463d20bf5ff2e95ec664657e62fa72b681919fdd03bacc80c8f25dcd36b8f483a1fdf02ca45a856924af4758998a0e41603965ac3b982da43');