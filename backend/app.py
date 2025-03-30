from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from db_config import connect_db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# ---------------------------
# Page Routes (Render Templates)
# ---------------------------
@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/register')
def register_page():
    return render_template("register.html")

@app.route('/vehicles')
def vehicles_page():
    return render_template("vehicles.html")

@app.route('/booking')
def booking_page():
    return render_template("booking.html")

@app.route('/mybookings')
def mybookings_page():
    return render_template("mybookings.html")

@app.route('/logout')
def logout_page():
    session.clear()
    return redirect(url_for('home_page'))

# ---------------------------
# API Endpoints (JSON Responses)
# ---------------------------
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    db = connect_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicles WHERE availability = TRUE")
    vehicles = cursor.fetchall()
    db.close()
    return jsonify(vehicles)

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    if 'user_id' not in session:
        return jsonify({"error": "User must be logged in to create a booking"}), 401

    data = request.get_json()
    user_id = session['user_id']  # use logged-in user's id
    vehicle_id = data.get('vehicle_id')
    rent_date = data.get('rent_date')
    return_date = data.get('return_date')

    if not all([vehicle_id, rent_date, return_date]):
        return jsonify({"error": "Missing required fields"}), 400

    db = connect_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = db.cursor(dictionary=True)
    
    # Get vehicle price per day
    cursor.execute("SELECT price_per_day FROM vehicles WHERE id = %s", (vehicle_id,))
    vehicle = cursor.fetchone()
    if not vehicle:
        db.close()
        return jsonify({"error": "Vehicle not found"}), 404

    price_per_day = vehicle['price_per_day']

    try:
        rent_dt = datetime.strptime(rent_date, "%Y-%m-%d")
        return_dt = datetime.strptime(return_date, "%Y-%m-%d")
    except ValueError:
        db.close()
        return jsonify({"error": "Date format should be YYYY-MM-DD"}), 400

    delta = (return_dt - rent_dt).days
    if delta < 1:
        db.close()
        return jsonify({"error": "Return date must be after rent date"}), 400

    total_price = price_per_day * delta

    insert_query = """
        INSERT INTO bookings (user_id, vehicle_id, rent_date, return_date, total_price, status)
        VALUES (%s, %s, %s, %s, %s, 'Pending')
    """
    cursor.execute(insert_query, (user_id, vehicle_id, rent_date, return_date, total_price))
    db.commit()
    db.close()

    return jsonify({"message": "Booking created", "total_price": total_price}), 201

@app.route('/api/mybookings', methods=['GET'])
def my_bookings():
    if 'user_id' not in session:
        return jsonify({"error": "User must be logged in to view bookings"}), 401

    user_id = session['user_id']
    db = connect_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT b.id AS booking_id, b.rent_date, b.return_date, b.total_price, b.status, 
               v.model, v.brand, v.price_per_day
        FROM bookings b
        JOIN vehicles v ON b.vehicle_id = v.id
        WHERE b.user_id = %s
        ORDER BY b.rent_date DESC
    """
    cursor.execute(query, (user_id,))
    bookings = cursor.fetchall()
    db.close()
    return jsonify(bookings)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    hashed_password = generate_password_hash(password)

    db = connect_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)", 
            (name, email, phone, hashed_password)
        )
        db.commit()
    except Exception as e:
        db.close()
        if "Duplicate entry" in str(e):
            return jsonify({"error": "This email is already registered. Please use a different email."}), 400
        return jsonify({"error": str(e)}), 500
    db.close()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = connect_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    db.close()
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    session['user_id'] = user['id']
    session['user_name'] = user['name']
    
    return jsonify({"message": "Login successful. Welcome, " + user['name'], "user": user}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
