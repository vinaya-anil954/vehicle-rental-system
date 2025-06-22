import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your MySQL username
        password="arjithsingh",  # Change to your MySQL password
        database="vehicle_rental"  # Ensure this database exists
    )
