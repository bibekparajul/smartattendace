from flask import Flask, render_template, request, send_file, redirect, url_for
import sqlite3
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Login route
@app.route('/')
def login():
    return render_template('login.html')

# Authentication route
@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the username and password match
    if username == 'admin' and password == 'admin':
        # Redirect to the attendance page if authentication is successful
        return redirect(url_for('index'))
    else:
        # Redirect back to the login page if authentication fails
        return redirect(url_for('login', error='Invalid credentials'))

# Main page route
@app.route('/index')
def index():
    # Ensure user is logged in before accessing this page
    # Here you can place your existing attendance functionality
    return render_template('base.html', selected_date='', no_data=False)

# Attendance route
@app.route('/attendance', methods=['POST'])
def attendance():
    selected_date = request.form.get('selected_date')
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, time FROM attendance WHERE date = ?", (formatted_date,))
    attendance_data = cursor.fetchall()

    conn.close()

    if not attendance_data:
        return render_template('base.html', selected_date=selected_date, no_data=True)

    return render_template('base.html', selected_date=selected_date, attendance_data=attendance_data)

# Download attendance route
@app.route('/download_attendance', methods=['POST'])
def download_attendance():
    selected_date = request.form.get('selected_date')
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, time FROM attendance WHERE date = ?", (selected_date,))
    attendance_data = cursor.fetchall()

    conn.close()

    if not attendance_data:
        return "No attendance data available for the selected date."

    excel_filename = f"attendance_{selected_date}.xlsx"
    df = pd.DataFrame(attendance_data, columns=['Name', 'Time'])
    df.to_excel(excel_filename, index=False)

    return send_file(excel_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
