from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name TEXT NOT NULL,
            checkin TEXT NOT NULL,
            checkout TEXT NOT NULL,
            room_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- ROUTES ---
# 1. The Home Page
@app.route('/')
def home():
    return render_template('index.html')

# 2. Catching the Form Data
@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    name = request.form['guest_name']
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    room = request.form['room_type']
    
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (guest_name, checkin, checkout, room_type)
        VALUES (?, ?, ?, ?)
    ''', (name, checkin, checkout, room))
    conn.commit()
    conn.close()
    
    return render_template('success.html', guest=name, room=room)

# 3. THE NEW ADMIN DASHBOARD
@app.route('/admin')
def admin():
    # Open the database and grab ALL records
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    all_bookings = cursor.fetchall() # This fetches everything as a list
    conn.close()
    
    # Send that list of data to a new admin webpage
    return render_template('admin.html', bookings=all_bookings)

if __name__ == '__main__':
    app.run(debug=True)