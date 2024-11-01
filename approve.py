import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def execute_query(query, params=None):
    """Execute a query with optional parameters and return the cursor."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(query, params if params else ())
        connection.commit()
        return cursor  # Return cursor for further processing if needed
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_data(query, params=None):
    """Fetch data from the database and return it as a list of dictionaries."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params if params else ())
        rows = cursor.fetchall()
        return rows
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# BOOKING CRUD FUNCTIONS
def get_bookings():
    """Retrieve all bookings."""
    query = "SELECT * FROM BOOKING"
    return fetch_data(query)

# Streamlit UI for Booking Management
def show_booking_management():
    st.subheader("Booking Management")

    st.write("### Available Bookings")
    bookings_data = get_bookings()
    if bookings_data:
        st.dataframe(bookings_data)
    else:
        st.warning("No bookings found.")

# Run the booking management function to show the UI
show_booking_management()

