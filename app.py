from flask import Flask, render_template, request
import sqlite3
import os

# Get absolute path for database (needed for Render deployment)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'hotel.db')

app = Flask(__name__)

# --- DATABASE FUNCTIONS ---
def get_db_connection():
    """Create and return a database connection with row factory."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database - create if not exists and ensure table exists."""
    conn = sqlite3.connect(DATABASE)
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

# Initialize database on startup
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
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (guest_name, checkin, checkout, room_type)
            VALUES (?, ?, ?, ?)
        ''', (name, checkin, checkout, room))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        return f"Database error: {str(e)}", 500
    
    return render_template('success.html', guest=name, room=room)

# 3. THE NEW ADMIN DASHBOARD
@app.route('/admin')
def admin():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bookings')
        all_bookings = cursor.fetchall()
        conn.close()
    except sqlite3.Error:
        all_bookings = []
    
    return render_template('admin.html', bookings=all_bookings)

if __name__ == '__main__':
    app.run(debug=True)