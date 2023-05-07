from flask import Flask, render_template, request, redirect, url_for, session

import database


logins = {
    "admin" : "password"
}

app = Flask(__name__)
app.secret_key = "my_super_secret_key"
db = database.Database()

def add_message(name, msg):
    if "messages" not in session:
        session["messages"] = {}
    session["messages"][name] = msg
    session.modified = True
    print(session["messages"])

def parse_messages():
    if "messages" not in session:
        session["messages"] = {}
    
    messages = session["messages"]
    session["messages"] = {}
    return messages



@app.route("/")
def index():
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        if username not in logins:
            session["logged_in"] = False
            return render_template("login.html", error=f"Username '{username}' is invalid.")
        
        if password != logins[username]:
            session["logged_in"] = False
            return render_template("login.html", error=f"Invalid password.")
        
        session["logged_in"] = True
        return redirect(url_for("dashboard"))

    elif session.get("logged_in"):
        add_message("already_logged_in", "You are already logged in.")
        return render_template("login.html", **parse_messages()) 
    
    return render_template("login.html", **parse_messages()) 

@app.route("/dashboard")
def dashboard():
    if session.get("logged_in"):
        return render_template("dashboard.html", students=db.get_student(), quizes=db.get_quiz(), **parse_messages())
    else:
        add_message("error", "You must be logged in to see dashboard.")
        return redirect(url_for("login"))

@app.route("/student/add", methods=["POST", "GET"])
def student_add():
    if not session.get("logged_in"):
        add_message("error", "You must be logged in to add student.")
        return redirect(url_for("login"))

    if request.method == 'POST':
        first = request.form["first_name"]
        last = request.form["last_name"]
        db.add_student(first, last)

        add_message("msg_student", f"Student '{first} {last}' added to database.")
        return redirect(url_for("dashboard"))
    
    else:
        return render_template("add_student.html")

@app.route("/quiz/add", methods=["POST", "GET"])
def quiz_add():
    if not session.get("logged_in"):
        add_message("error", "You must be logged in to add quiz.")
        return redirect(url_for("login"))

    if request.method == 'POST':
        subject = request.form["subject"]
        number = int(request.form["number"])
        date = request.form["date"]
        
        db.add_quiz(subject, number, date)

        add_message("msg_quiz", f"Quiz from {subject} with {number} questions on {date} added to database.")
        return redirect(url_for("dashboard"))
    
    else:
        return render_template("add_quiz.html")

@app.route('/student/<id>')
def student(id):
    if not session.get("logged_in"):
        add_message("error", "You must be logged in to see student details.")
        return redirect(url_for("login"))
    
    return render_template("student.html", student=db.get_student(id), results=db.full_join(id))

@app.route('/result/add', methods=["POST", "GET"])
def result_add():
    if not session.get("logged_in"):
        add_message("error", "You must be logged in to add results.")
        return redirect(url_for("login"))
    
    if request.method == "GET":
        students = db.get_student()
        quizes = db.get_quiz()

        students = [(student[0], f"ID: {student[0]}, {student[1]} {student[2]}")
                    for student in students]

        quizes = [(quiz[0], f"ID: {quiz[0]}, {quiz[1]}")
                    for quiz in quizes]
        
        return render_template("add_result.html", students=students, quizes=quizes)

    if request.method == "POST":
        student_id = int(request.form["student"])
        quiz_id = int(request.form["quiz"])
        score = int(request.form["score"])

        db.add_result(student_id, quiz_id, score)

        add_message("msg_result", f"Quiz result added to database")
        return redirect(url_for("dashboard"))



if __name__ == '__main__':
    app.run(debug=True)