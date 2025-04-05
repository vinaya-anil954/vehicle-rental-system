from flask import Flask, render_template, request, redirect, session, url_for, flash, current_app
from flask import Flask, render_template, request, redirect, session, url_for, flash
from db_config import get_db_connection
import hashlib
from datetime import datetime, timedelta,date
import os
import logging  # Add this import at the top

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
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

# ... [previous imports and setup remain the same] ...

@app.route('/book/<int:vehicle_id>', methods=['GET', 'POST'])
def book_vehicle(vehicle_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get vehicle details - unchanged
    cursor.execute("SELECT id, model, brand, price FROM vehicles WHERE id=%s", (vehicle_id,))
    vehicle = cursor.fetchone()
    
    if request.method == 'POST':
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        needs_driver = request.form.get('needs_driver') == 'true'  
        try:
            # Date validation (unchanged)
            from_dt = datetime.strptime(from_date, '%Y-%m-%d')
            to_dt = datetime.strptime(to_date, '%Y-%m-%d')
            total_days = (to_dt - from_dt).days
            
            if total_days <= 0:
                flash('Invalid date range', 'error')
                return redirect(url_for('book_vehicle', vehicle_id=vehicle_id))

            # NEW: Driver assignment logic
            driver_id = None
            if needs_driver:
                cursor.execute("""
                    SELECT id FROM drivers 
                    WHERE available = TRUE 
                    LIMIT 1
                """)
                driver = cursor.fetchone()
                
                if not driver:
                    flash('No drivers currently available', 'error')
                    return redirect(url_for('book_vehicle', vehicle_id=vehicle_id))
                
                driver_id = driver[0]
                cursor.execute("UPDATE drivers SET available=FALSE WHERE id=%s", (driver_id,))

            # Calculate total price
            base_price = float(vehicle[3]) * total_days
            driver_fee = 20 * total_days if needs_driver else 0
            total_price = base_price + driver_fee

            # Insert booking with driver info
            cursor.execute("""
                INSERT INTO bookings 
                (user_id, vehicle_id, from_date, to_date, total_days, status, needs_driver, driver_id, total_price) 
                VALUES (%s, %s, %s, %s, %s, 'pending', %s, %s, %s)
            """, (
                session['user_id'], vehicle_id, from_date, to_date, 
                total_days, needs_driver, driver_id, total_price
            ))

            cursor.execute("UPDATE vehicles SET available=0 WHERE id=%s", (vehicle_id,))
            conn.commit()
            
            flash('Booking successful!', 'success')
            return redirect(url_for('booking_history'))

        except ValueError:
            flash('Invalid date format', 'error')
        finally:
            conn.close()

    min_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('book_vehicle.html',
                         vehicle=vehicle,
                         min_date=min_date)
@app.route('/booking_history')
def booking_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all necessary booking information including driver details
        cursor.execute("""
            SELECT 
                b.id, 
                v.model, 
                v.brand, 
                v.price,
                b.from_date,
                b.to_date,
                b.total_days,
                b.status,
                b.needs_driver,
                b.driver_id,
                d.name as driver_name,
                d.contact_number as driver_contact,
                d.license_number as driver_license
            FROM bookings b
            JOIN vehicles v ON b.vehicle_id = v.id
            LEFT JOIN drivers d ON b.driver_id = d.id
            WHERE b.user_id = %s
            ORDER BY b.from_date DESC
        """, (session['user_id'],))
        
        bookings = []
        for booking in cursor.fetchall():
            try:
                bookings.append({
                    'id': booking[0],
                    'model': booking[1],
                    'brand': booking[2],
                    'price': float(booking[3]),
                    'from_date': booking[4].strftime('%Y-%m-%d') if hasattr(booking[4], 'strftime') else str(booking[4]),
                    'to_date': booking[5].strftime('%Y-%m-%d') if hasattr(booking[5], 'strftime') else str(booking[5]),
                    'total_days': booking[6],
                    'status': booking[7],
                    'needs_driver': booking[8],
                    'driver_id': booking[9],
                    'driver_name': booking[10],
                    'driver_contact': booking[11],
                    'driver_license': booking[12]
                })
            except Exception as e:
                logger.error(f"Error processing booking: {str(e)}")
                continue
        
        return render_template('booking_history.html', bookings=bookings)
        
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        flash('Error loading booking history', 'error')
        return redirect(url_for('user_dashboard'))
    finally:
        if conn:
            conn.close()
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