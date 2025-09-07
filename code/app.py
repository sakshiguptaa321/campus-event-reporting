# Simple Flask app for Campus Event Reporting System
# Sakshi Gupta

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"

# create database + tables if not exists
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # College Table
    cur.execute("""CREATE TABLE IF NOT EXISTS College(
                    college_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )""")

    # Student Table
    cur.execute("""CREATE TABLE IF NOT EXISTS Student(
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    college_id INTEGER,
                    FOREIGN KEY(college_id) REFERENCES College(college_id)
                )""")

    # Event Table
    cur.execute("""CREATE TABLE IF NOT EXISTS Event(
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    type TEXT,
                    date TEXT,
                    status TEXT,
                    college_id INTEGER,
                    FOREIGN KEY(college_id) REFERENCES College(college_id)
                )""")

    # Registration (student <-> event)
    cur.execute("""CREATE TABLE IF NOT EXISTS Registration(
                    reg_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    student_id INTEGER,
                    UNIQUE(event_id, student_id),
                    FOREIGN KEY(event_id) REFERENCES Event(event_id),
                    FOREIGN KEY(student_id) REFERENCES Student(student_id)
                )""")

    # Attendance
    cur.execute("""CREATE TABLE IF NOT EXISTS Attendance(
                    att_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reg_id INTEGER,
                    status TEXT,
                    FOREIGN KEY(reg_id) REFERENCES Registration(reg_id)
                )""")

    # Feedback
    cur.execute("""CREATE TABLE IF NOT EXISTS Feedback(
                    fb_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reg_id INTEGER,
                    rating INTEGER,
                    comment TEXT,
                    FOREIGN KEY(reg_id) REFERENCES Registration(reg_id)
                )""")

    conn.commit()
    conn.close()

# initialize db
init_db()


# ------------------ APIs ------------------ #

@app.route("/create_event", methods=["POST"])
def create_event():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO Event (name, type, date, status, college_id) VALUES (?,?,?,?,?)",
                (data["name"], data["type"], data["date"], data.get("status","Active"), data["college_id"]))
    conn.commit()
    conn.close()
    return jsonify({"msg": "event created"})


@app.route("/register_student", methods=["POST"])
def register_student():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Registration (event_id, student_id) VALUES (?,?)",
                    (data["event_id"], data["student_id"]))
        conn.commit()
        return jsonify({"msg": "student registered"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "already registered"}), 400
    finally:
        conn.close()


@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO Attendance (reg_id, status) VALUES (?,?)",
                (data["reg_id"], data["status"]))
    conn.commit()
    conn.close()
    return jsonify({"msg": "attendance marked"})


@app.route("/give_feedback", methods=["POST"])
def give_feedback():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO Feedback (reg_id, rating, comment) VALUES (?,?,?)",
                (data["reg_id"], data["rating"], data.get("comment","")))
    conn.commit()
    conn.close()
    return jsonify({"msg": "feedback saved"})


# ------------------ Reports ------------------ #

@app.route("/report/event_popularity")
def report_event_popularity():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""SELECT Event.name, COUNT(Registration.reg_id)
                   FROM Event LEFT JOIN Registration
                   ON Event.event_id = Registration.event_id
                   GROUP BY Event.event_id
                   ORDER BY COUNT(Registration.reg_id) DESC""")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"event": r[0], "registrations": r[1]} for r in rows])


@app.route("/report/student_participation")
def report_student_participation():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""SELECT Student.name, COUNT(Attendance.att_id)
                   FROM Student JOIN Registration
                   ON Student.student_id = Registration.student_id
                   JOIN Attendance
                   ON Registration.reg_id = Attendance.reg_id
                   WHERE Attendance.status='Present'
                   GROUP BY Student.student_id""")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"student": r[0], "attended": r[1]} for r in rows])


@app.route("/report/top_students")
def report_top_students():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""SELECT Student.name, COUNT(Attendance.att_id) as attended
                   FROM Student JOIN Registration
                   ON Student.student_id = Registration.student_id
                   JOIN Attendance
                   ON Registration.reg_id = Attendance.reg_id
                   WHERE Attendance.status='Present'
                   GROUP BY Student.student_id
                   ORDER BY attended DESC LIMIT 3""")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"student": r[0], "attended": r[1]} for r in rows])


if __name__ == "__main__":
    app.run(debug=True)
