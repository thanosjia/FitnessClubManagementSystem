CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    user_name TEXT NOT NULL UNIQUE,
    pwd TEXT NOT NULL,
    membership_status BOOLEAN NOT NULL DEFAULT FALSE,
    payment_method TEXT NOT NULL
);

CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    user_name TEXT NOT NULL UNIQUE,
    pwd TEXT NOT NULL
);

CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    user_name TEXT NOT NULL UNIQUE,
    pwd TEXT NOT NULL
);

CREATE TABLE training_sessions (
    session_id SERIAL PRIMARY KEY,
    trainer_id INT,
    member_id INT,
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_name TEXT NOT NULL,
    room_capacity INT NOT NULL
);

CREATE TABLE room_bookings (
    booking_id SERIAL PRIMARY KEY,
    room_id INT,
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name TEXT NOT NULL,
    equipment_status TEXT NOT NULL
);

CREATE TABLE fitness_classes (
    class_id SERIAL PRIMARY KEY,
    class_name TEXT NOT NULL,
    class_room INT,
    class_date DATE NOT NULL,
    class_time TIME NOT NULL,
    FOREIGN KEY (class_room) REFERENCES rooms(room_id)
);

CREATE TABLE fitness_goals (
    goal_id SERIAL PRIMARY KEY,
    member_id INT,
    goal_type TEXT NOT NULL,
    goal_value INT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);
