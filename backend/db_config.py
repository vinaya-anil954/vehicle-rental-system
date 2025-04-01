import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="flaskuser",  # Change to your MySQL username
        password="1115",  # Change to your MySQL password
        database="vehicle_rental"  # Ensure this database exists
    )
