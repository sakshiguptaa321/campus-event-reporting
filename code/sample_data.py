# Script to add some sample data into the DB
# run this once

import sqlite3

DB_NAME = "database.db"

def add_data():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # add colleges
    cur.execute("INSERT INTO College (name) VALUES ('ABC College')")
    cur.execute("INSERT INTO College (name) VALUES ('XYZ Institute')")

    # add students
    cur.execute("INSERT INTO Student (name,email,college_id) VALUES ('Sakshi Gupta','sakshi@example.com',1)")
    cur.execute("INSERT INTO Student (name,email,college_id) VALUES ('Rohit Kumar','rohit@example.com',1)")
    cur.execute("INSERT INTO Student (name,email,college_id) VALUES ('Anita Sen','anita@example.com',2)")

    # add events
    cur.execute("INSERT INTO Event (name,type,date,status,college_id) VALUES ('AI Workshop','Workshop','2025-09-10','Active',1)")
    cur.execute("INSERT INTO Event (name,type,date,status,college_id) VALUES ('HackFest','Fest','2025-09-12','Active',1)")
    cur.execute("INSERT INTO Event (name,type,date,status,college_id) VALUES ('Guest Lecture','Seminar','2025-09-15','Active',2)")

    conn.commit()
    conn.close()
    print("Sample data inserted!")

if __name__ == "__main__":
    add_data()
