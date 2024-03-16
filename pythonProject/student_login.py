# #
# # #
# # #
# # # from flask import Flask, render_template, request, redirect, url_for
# # # import sqlite3
# # # import os
# # # from datetime import datetime, timedelta
# # #
# # # app = Flask(__name__)
# # #
# # # # Path of cropped faces
# # # path_images_from_camera = "data/data_faces_from_camera/"
# # #
# # # # Load attendance data from SQLite database
# # # def fetch_attendance(username):
# # #     conn = sqlite3.connect('attendance.db')
# # #     cursor = conn.cursor()
# # #
# # #     # Get all dates in the current month
# # #     today = datetime.today()
# # #     start_of_month = today.replace(day=1)
# # #     end_of_month = start_of_month.replace(month=today.month+1) - timedelta(days=1)
# # #
# # #     # Fetch attendance data for the current month
# # #     cursor.execute("SELECT date, time FROM attendance WHERE name = ? AND date BETWEEN ? AND ?",
# # #                    (username, start_of_month.strftime('%Y-%m-%d'), end_of_month.strftime('%Y-%m-%d')))
# # #     attendance_data = cursor.fetchall()
# # #
# # #     conn.close()
# # #
# # #     # Prepare attendance details for each date in the month
# # #     attendance_details = []
# # #     current_date = start_of_month
# # #     while current_date <= end_of_month:
# # #         formatted_date = current_date.strftime('%Y-%m-%d')
# # #         present = any(entry[0] == formatted_date for entry in attendance_data)
# # #         attendance_details.append((formatted_date, 'Present' if present else 'Absent'))
# # #         current_date += timedelta(days=1)
# # #
# # #     return attendance_details
# # #
# # # # Load student directories and extract names for authentication
# # # student_directories = os.listdir(path_images_from_camera)
# # # student_usernames = [directory.split('_')[2] for directory in student_directories]
# # #
# # # # Login route
# # # @app.route('/', methods=['GET', 'POST'])
# # # def login():
# # #     if request.method == 'POST':
# # #         name = request.form.get('username')  # Use 'name' instead of 'username' for student authentication
# # #         password = request.form.get('password')
# # #
# # #         # Check if the name exists in the student directories and if it matches both the username and password
# # #         if name in student_usernames and name == password:
# # #             return redirect(url_for('attendance', username=name))
# # #         else:
# # #             return render_template('login.html', error='Invalid credentials')
# # #
# # #     return render_template('login.html')
# # #
# # #
# # # # Authentication route
# # # @app.route('/authenticate', methods=['POST'])
# # # def authenticate():
# # #     name = request.form.get('username')  # Use 'name' instead of 'username' for student authentication
# # #     password = request.form.get('password')
# # #
# # #     # Check if the name exists in the student directories and if it matches both the username and password
# # #     if name in student_usernames and name == password:
# # #         return redirect(url_for('attendance', username=name))
# # #     else:
# # #         return render_template('login.html', error='Invalid credentials')
# # #
# # # # Attendance route
# # # @app.route('/attendance/<username>')
# # # def attendance(username):
# # #     # Ensure only authenticated users can access their own attendance
# # #     if username not in student_usernames:
# # #         return redirect(url_for('login'))
# # #
# # #     attendance_data = fetch_attendance(username)
# # #
# # #     if not attendance_data:
# # #         return render_template('attendance.html', username=username, no_data=True)
# # #     else:
# # #         return render_template('attendance.html', username=username, attendance_data=attendance_data)
# # #
# # # if __name__ == '__main__':
# # #     app.run(debug=True)
# #
# #
# # from flask import Flask, render_template, request, redirect, url_for
# # import sqlite3
# # import os
# # from datetime import datetime, timedelta
# #
# # app = Flask(__name__)
# #
# # # Path of cropped faces
# # path_images_from_camera = "data/data_faces_from_camera/"
# #
# # # Load attendance data from SQLite database
# # def fetch_attendance(username):
# #     conn = sqlite3.connect('attendance.db')
# #     cursor = conn.cursor()
# #
# #     # Get all dates in the current month
# #     today = datetime.today()
# #     start_of_month = today.replace(day=1)
# #     end_of_month = start_of_month.replace(month=today.month+1) - timedelta(days=1)
# #
# #     # Fetch attendance data for the current month
# #     cursor.execute("SELECT date, time FROM attendance WHERE name = ? AND date BETWEEN ? AND ?",
# #                    (username, start_of_month.strftime('%Y-%m-%d'), end_of_month.strftime('%Y-%m-%d')))
# #     attendance_data = cursor.fetchall()
# #
# #     conn.close()
# #
# #     # Prepare attendance details for each date in the month
# #     attendance_details = []
# #     current_date = start_of_month
# #     while current_date <= end_of_month:
# #         formatted_date = current_date.strftime('%Y-%m-%d')
# #         present = any(entry[0] == formatted_date for entry in attendance_data)
# #         # Fetch time if present, else set to empty string
# #         time_present = next((entry[1] for entry in attendance_data if entry[0] == formatted_date), '')
# #         status = 'Present' if present else 'Absent'
# #         attendance_details.append((formatted_date, status, time_present))
# #         current_date += timedelta(days=1)
# #
# #     return attendance_details
# #
# # # Load student directories and extract names for authentication
# # student_directories = os.listdir(path_images_from_camera)
# # student_usernames = [directory.split('_')[2] for directory in student_directories]
# #
# # # Login route
# # @app.route('/', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         name = request.form.get('username')  # Use 'name' instead of 'username' for student authentication
# #         password = request.form.get('password')
# #
# #         # Check if the name exists in the student directories and if it matches both the username and password
# #         if name in student_usernames and name == password:
# #             return redirect(url_for('attendance', username=name))
# #         else:
# #             return render_template('login.html', error='Invalid credentials')
# #
# #     return render_template('login.html')
# #
# #
# # # Authentication route
# # @app.route('/authenticate', methods=['POST'])
# # def authenticate():
# #     name = request.form.get('username')  # Use 'name' instead of 'username' for student authentication
# #     password = request.form.get('password')
# #
# #     # Check if the name exists in the student directories and if it matches both the username and password
# #     if name in student_usernames and name == password:
# #         return redirect(url_for('attendance', username=name))
# #     else:
# #         return render_template('login.html', error='Invalid credentials')
# #
# # # Attendance route
# # @app.route('/attendance/<username>')
# # def attendance(username):
# #     # Ensure only authenticated users can access their own attendance
# #     if username not in student_usernames:
# #         return redirect(url_for('login'))
# #
# #     attendance_data = fetch_attendance(username)
# #
# #     if not attendance_data:
# #         return render_template('attendance.html', username=username, no_data=True)
# #     else:
# #         return render_template('attendance.html', username=username, attendance_data=attendance_data)
# #
# # if __name__ == '__main__':
# #     app.run(debug=True)
#
#
#
# from flask import Flask, render_template, request, redirect, url_for
# import sqlite3
# import os
# from datetime import datetime, timedelta
#
# app = Flask(__name__)
#
# # Path of cropped faces
# path_images_from_camera = "data/data_faces_from_camera/"
#
# # Load attendance data from SQLite database
# def fetch_attendance(username):
#     conn = sqlite3.connect('attendance.db')
#     cursor = conn.cursor()
#
#     # Get start and end date for current month
#     today = datetime.today()
#     start_of_month = today.replace(day=1)
#     end_of_month = start_of_month.replace(month=today.month+1) - timedelta(days=1)
#
#     # Fetch attendance data up to current date of the month
#     cursor.execute("SELECT date, time FROM attendance WHERE name = ? AND date BETWEEN ? AND ?",
#                    (username, start_of_month.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')))
#     attendance_data = cursor.fetchall()
#
#     conn.close()
#
#     # Prepare attendance details for each date up to current date in the month
#     attendance_details = []
#     current_date = start_of_month
#     while current_date <= today:
#         formatted_date = current_date.strftime('%Y-%m-%d')
#         present = any(entry[0] == formatted_date for entry in attendance_data)
#         # Fetch time if present, else set to empty string
#         time_present = next((entry[1] for entry in attendance_data if entry[0] == formatted_date), '')
#         status = 'Present' if present else 'Absent'
#         attendance_details.append((formatted_date, status, time_present))
#         current_date += timedelta(days=1)
#
#     return attendance_details
#
# # Load student directories and extract names for authentication
# student_directories = os.listdir(path_images_from_camera)
# student_usernames = [directory.split('_')[2] for directory in student_directories]
#
# # Login route
# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         name = request.form.get('username')  # Use 'name' instead of 'username' for student authentication
#         password = request.form.get('password')
#
#         # Check if the name exists in the student directories and if it matches both the username and password
#         if name in student_usernames and name == password:
#             return redirect(url_for('attendance', username=name))
#         else:
#             return render_template('login.html', error='Invalid credentials')
#
#     return render_template('login.html')
#
#
# # Authentication route
# @app.route('/authenticate', methods=['POST'])
# def authenticate():
#     name = request.form.get('username')  # Use 'name' instead of 'username' for student authentication
#     password = request.form.get('password')
#
#     # Check if the name exists in the student directories and if it matches both the username and password
#     if name in student_usernames and name == password:
#         return redirect(url_for('attendance', username=name))
#     else:
#         return render_template('login.html', error='Invalid credentials')
#
# # Attendance route
# @app.route('/attendance/<username>')
# def attendance(username):
#     # Ensure only authenticated users can access their own attendance
#     if username not in student_usernames:
#         return redirect(url_for('login'))
#
#     attendance_data = fetch_attendance(username)
#
#     if not attendance_data:
#         return render_template('attendance.html', username=username, no_data=True)
#     else:
#         return render_template('attendance.html', username=username, attendance_data=attendance_data)
#
# if __name__ == '__main__':
#     app.run(debug=True)
#




from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = 'abcd'  # Change this to a random string


# Path of cropped faces
path_images_from_camera = "data/data_faces_from_camera/"

# Load attendance data from SQLite database
def fetch_attendance(username):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Get start and end date for current month
    today = datetime.today()
    start_of_month = today.replace(day=1)
    end_of_month = start_of_month.replace(month=today.month+1) - timedelta(days=1)

    # Fetch attendance data up to current date of the month
    cursor.execute("SELECT date, time FROM attendance WHERE name = ? AND date BETWEEN ? AND ?",
                   (username, start_of_month.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')))
    attendance_data = cursor.fetchall()

    conn.close()

    # Prepare attendance details for each date up to current date in the month
    attendance_details = []
    present_count = 0
    total_days = (today - start_of_month).days + 1  # Total number of days up to today in the month
    current_date = start_of_month
    while current_date <= today:
        formatted_date = current_date.strftime('%Y-%m-%d')
        present = any(entry[0] == formatted_date for entry in attendance_data)
        # Fetch time if present, else set to empty string
        time_present = next((entry[1] for entry in attendance_data if entry[0] == formatted_date), '')
        status = 'Present' if present else 'Absent'
        attendance_details.append((formatted_date, status, time_present))
        if present:
            present_count += 1
        current_date += timedelta(days=1)

    # Calculate attendance percentage
    attendance_percentage = (present_count / total_days) * 100 if total_days > 0 else 0

    return attendance_details, attendance_percentage, total_days, present_count

# Load student directories and extract names for authentication
student_directories = os.listdir(path_images_from_camera)
student_usernames = [directory.split('_')[2] for directory in student_directories]

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')  # Use 'name' instead of 'username' for student authentication
        password = request.form.get('password')

        # Check if the name exists in the student directories and if it matches both the username and password
        if name in student_usernames and name == password:
            return redirect(url_for('attendance', username=name))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


# Authentication route
@app.route('/authenticate', methods=['POST'])
def authenticate():
    name = request.form.get('username')  # Use 'name' instead of 'username' for student authentication
    password = request.form.get('password')

    # Check if the name exists in the student directories and if it matches both the username and password
    if name in student_usernames and name == password:
        return redirect(url_for('attendance', username=name))
    else:
        return render_template('login.html', error='Invalid credentials')


# Logout route
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('login'))

# Attendance route
@app.route('/attendance/<username>')
def attendance(username):
    # Ensure only authenticated users can access their own attendance
    if username not in student_usernames:
        return redirect(url_for('login'))

    attendance_data, attendance_percentage, total_days, present_count = fetch_attendance(username)

    if not attendance_data:
        return render_template('attendance.html', username=username, no_data=True, attendance_percentage=attendance_percentage, total_days=total_days,present_count=present_count)
    else:
        return render_template('attendance.html', username=username, attendance_data=attendance_data, attendance_percentage=attendance_percentage, total_days=total_days, present_count=present_count)

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except RuntimeError as e:
        if 'The session is unavailable because no secret key was set' in str(e):
            print("Error: Please set the 'secret_key' for the application.")
