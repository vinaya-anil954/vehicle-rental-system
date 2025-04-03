from flask import Flask, render_template, request, redirect, session, url_for, flash
from db_config import get_db_connection
import hashlib
import os

# Configure Flask
app = Flask(
    __name__,
    template_folder=os.path.abspath('../frontend/templates'),
    static_folder=os.path.abspath('../frontend/static')
)
app.secret_key = 'your_secret_key'

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Home Route
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))
    elif 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = hash_password(request.form['password'])
        
        conn   = get_db_connection()
        cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            conn.close()
            return redirect(url_for('signup'))

        # Insert new user
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))
        conn.commit()
        conn.close()
        
        flash('Signup successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')
    # Admin: Delete Vehicle
@app.route('/delete_vehicle/<int:vehicle_id>')
def delete_vehicle(vehicle_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    conn   = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicles WHERE id=%s", (vehicle_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))
# Add Vehicle (Admin)
@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    model = request.form['model']
    brand = request.form['brand']
    price = request.form['price']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vehicles (model, brand, price, available) VALUES (%s, %s, %s, 1)",
                   (model, brand, price))
    conn.commit()
    conn.close()
    
    flash('Vehicle added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

# Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM admins WHERE email=%s AND password=%s", (email, password))
        admin = cursor.fetchone()
        conn.close()
        if admin:
            session['admin_id'] = admin[0]
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'error')
    return render_template('admin_login.html')

# User Dashboard
@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles WHERE available=1")
    vehicles = cursor.fetchall()
    conn.close()
    return render_template('user_dashboard.html', vehicles=vehicles)

# Book a Vehicle
@app.route('/book/<int:vehicle_id>')
def book_vehicle(vehicle_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (user_id, vehicle_id) VALUES (%s, %s)", (user_id, vehicle_id))
    cursor.execute("UPDATE vehicles SET available=0 WHERE id=%s", (vehicle_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('booking_history'))

# User Booking History
@app.route('/booking_history')
def booking_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT bookings.id, vehicles.model, vehicles.brand, vehicles.price, bookings.status 
        FROM bookings 
        JOIN vehicles ON bookings.vehicle_id = vehicles.id 
        WHERE bookings.user_id=%s
    """, (user_id,))
    bookings = cursor.fetchall()
    conn.close()
    return render_template('booking_history.html', bookings=bookings)

# Cancel Booking
@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT vehicle_id FROM bookings WHERE id=%s", (booking_id,))
    vehicle = cursor.fetchone()
    if vehicle:
        vehicle_id = vehicle[0]
        cursor.execute("DELETE FROM bookings WHERE id=%s", (booking_id,))
        cursor.execute("UPDATE vehicles SET available=1 WHERE id=%s", (vehicle_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('booking_history'))

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()
    cursor.execute("""
        SELECT bookings.id, users.name, vehicles.model, bookings.status 
        FROM bookings 
        JOIN users ON bookings.user_id = users.id 
        JOIN vehicles ON bookings.vehicle_id = vehicles.id
    """)
    bookings = cursor.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', vehicles=vehicles, bookings=bookings)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)  