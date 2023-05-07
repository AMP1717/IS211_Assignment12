CREATE TABLE student(
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT
);

CREATE TABLE quiz(
    id INTEGER PRIMARY KEY,
    subject TEXT,
    quetions INTEGER,
    date TEXT
);

CREATE TABLE result(
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    quiz_id INTEGER,
    score INTEGER
);

