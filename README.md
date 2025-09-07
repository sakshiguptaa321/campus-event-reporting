Campus Event Reporting System
This is my project for the Webknot campus drive task.
The idea is to build a simple system where colleges can manage events and later generate reports for them.

My Understanding
In college events, we usually have a lot of registrations but tracking who actually attended or gave feedback is not done properly.
So in this project:
Admin/staff can create events.
Students can register for events.
Attendance can be marked on the event day.
Feedback can also be collected from students.
At the end, we can generate reports like which event was most popular, how many attended, and which students are most active.
I kept it simple so it is easy to test and run.

Tech Used
Python (Flask)
SQLite database
VS Code, SQLite Viewer, Postman

How to Run
Clone the repo or unzip the folder
Go into the code folder:
cd code

Install dependencies:
pip install -r requirements.txt

Insert sample data:
python sample_data.py

Run the server:
python app.py


