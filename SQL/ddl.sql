CREATE TABLE users {
    id SERIAL PRIMARY KEY,
    account_type TEXT NOT NULL,
    membership_status,
    payment_method TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    user_name TEXT NOT NULL,
    pwd TEXT NOT NULL
};

CREATE TABLE training_sessions {
    session_id SERIAL PRIMARY KEY,
    trainer_id,
    member_id,
    session_date DATE,
    session_time TIME
};

CREATE TABLE rooms {
    room_id SERIAL PRIMARY KEY,
};

CREATE TABLE room_bookings {
    booking_id SERIAL PRIMARY KEY,
    room_id,
    booking_date DATE,
    booking_time TIME
};

CREATE TABLE equipment {
    equipment_id SERIAL PRIMARY KEY,
    equipment_name TEXT NOT NULL,
    equipment_status
};

CREATE TABLE fitness_classes {
    class_id SERIAL PRIMARY KEY,
    class_name TEXT NOT NULL,
    class_room,
    class_date DATE,
    class_time TIME,
};
