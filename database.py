import sqlite3

FILENAME = 'hw13.db'

"""
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
"""

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(FILENAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def get_student(self, id=None):
        if id == None:
            return self.cursor.execute("SELECT * FROM student;").fetchall()
        else:
            return self.cursor.execute(f"SELECT * FROM student WHERE id={id};").fetchone()

    def get_quiz(self, id=None):
        if id == None:
            return self.cursor.execute("SELECT * FROM quiz;").fetchall()
        else:
            return self.cursor.execute(f"SELECT * FROM quiz WHERE id={id};").fetchone()
    
    def get_result(self, id=None):
        if id == None:
            return self.cursor.execute("SELECT * FROM result;").fetchall()
        else:
            return self.cursor.execute(f"SELECT * FROM result WHERE id={id};").fetchone()

    def add_student(self, first_name, last_name):
        new_id = self.cursor.execute("SELECT MAX(id) FROM student;").fetchone()[0] + 1
        self.cursor.execute("INSERT INTO student VALUES(?, ?, ?);", (new_id, first_name, last_name))
        self.conn.commit()

    def add_quiz(self, subject, number, date):
        new_id = self.cursor.execute("SELECT MAX(id) FROM quiz;").fetchone()[0] + 1
        self.cursor.execute("INSERT INTO quiz VALUES(?, ?, ?, ?);", (new_id, subject, number, date))
        self.conn.commit()
    
    def add_result(self, student, quiz, score):
        new_id = self.cursor.execute("SELECT MAX(id) FROM result;").fetchone()[0] + 1
        self.cursor.execute("INSERT INTO result VALUES(?, ?, ?, ?);", (new_id, student, quiz, score))
        self.conn.commit()

    def full_join(self, student_id):
        results =  self.cursor.execute(f"""
            SELECT * FROM student
            INNER JOIN result on student.id = result.student_id 
            INNER JOIN quiz on result.quiz_id = quiz.id
            WHERE student.id={student_id};
        """).fetchall()
        results = [{
            "student_id" : res[0],
            "first_name" : res[1],
            "last_name" : res[2],
            "result_id" : res[3],
            "quiz_id" : res[5],
            "score" : res[6],
            "subject" : res[8],
            "date" : res[10]

        }
            for res in results
        ]
        return results




def create_database():
    with open(FILENAME, 'w'):
        pass
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()

    with open("schema.sql", "r") as f:
        schema = f.read()
    
    cursor.executescript(schema)

    cursor.execute("INSERT INTO student VALUES(0, 'John', 'Smith')")
    cursor.execute("INSERT INTO quiz VALUES(0, 'Python Basics', 5, '2015-02-05')")
    cursor.execute("INSERT INTO result VALUES(0, 0, 0, 85)")

    cursor.close()
    conn.commit()


def test():
    d = Database()
    print("students:")
    print(d.get_student())
    print()

    print("quizes:")
    print(d.get_quiz())
    print()

    print("results:")
    print(d.get_result())
    print()

    print(d.get_student(0))
    print(d.full_join(0))




if __name__ == "__main__":
    create_database()
    print("Database created.")
    #test()
