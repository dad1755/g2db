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

# Function to connect to the database and fetch bookings
def fetch_bookings():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            query = "SELECT * FROM BOOKING WHERE payment_status = 1"
            df = pd.read_sql(query, connection)
            return df
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

# Streamlit UI for displaying booking details
def show_approve_management():
    st.subheader("Booking Management")
    st.write("Available Bookings (Pending Confirmation Will Be Listed Here)")
    
    # Fetch and display bookings with payment_status = 1
    bookings_df = fetch_bookings()
    
    if bookings_df is not None and not bookings_df.empty:
        st.dataframe(bookings_df)
    else:
        st.write("No bookings found with payment status = 1.")

# Run this function only if this script is executed directly
if __name__ == "__main__":
    show_approve_management()
