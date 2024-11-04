import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

# Function to fetch booking data from the database
def fetch_booking_data():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            query = "SELECT * FROM BOOKING"  # Customize this query as needed
            # Use pandas to execute the query and store result in a DataFrame
            booking_data = pd.read_sql(query, connection)
            return booking_data
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        if connection.is_connected():
            connection.close()

# Streamlit UI for displaying booking details
def show_approve_management():
    st.subheader("Booking Management")
    st.write("Available Bookings (Pending Confirmation Will Be Listed Here)")
    
    # Fetch booking data and display it as a table
    booking_data = fetch_booking_data()
    if not booking_data.empty:
        # Display data in a grid format
        st.dataframe(booking_data)
    else:
        st.write("No booking data available.")

# Run this function only if this script is executed directly
if __name__ == "__main__":
    show_approve_management()
