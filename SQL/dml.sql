INSERT INTO members (first_name, last_name, user_name, email, pwd) VALUES
('Thanos', 'Jia', 'thanosjia', 'thanosjia@email.com', 'member');

INSERT INTO trainers (first_name, last_name, user_name, pwd) VALUES
('John', 'Cena', 'johncena', 'trainer');

INSERT INTO admins (user_name, pwd) VALUES
('joeAdmin', 'admin');

INSERT INTO trainer_availability (trainer_id, available_date, available_time) VALUES
(1, '2024-05-01', '11:00');

INSERT INTO rooms (room_name, room_capacity) VALUES
('Cardio Room', '30');

INSERT INTO fitness_classes (class_name, class_room, class_date, class_time) VALUES
('Group HIIT', '1', '2024-05-01', '11:00');

INSERT INTO equipment (equipment_name) VALUES
('Assault Bike');