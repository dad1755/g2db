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

# Function to connect to the database and execute queries
def get_database_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Fetch booking data from the database
def fetch_booking_data():
    connection = get_database_connection()
    if connection:
        query = "SELECT * FROM BOOKING WHERE payment_status <> 2"  # Only fetch bookings with payment_status not equal to 2
        booking_data = pd.read_sql(query, connection)
        connection.close()
        return booking_data
    return pd.DataFrame()

# Function to update payment_status for a specific booking
def update_payment_status(book_id):
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            update_query = "UPDATE BOOKING SET payment_status = 2 WHERE book_id = %s"
            cursor.execute(update_query, (book_id,))
            connection.commit()
            st.success(f"Booking ID {book_id} has been confirmed!")
        except Error as e:
            st.error(f"Error updating booking: {e}")
        finally:
            cursor.close()
            connection.close()

# Streamlit UI for displaying and managing booking confirmation
def show_approve_management():
    st.subheader("Booking Management")
    st.write("Available Bookings (Pending Confirmation Will Be Listed Here)")
    
    # Fetch and display booking data
    booking_data = fetch_booking_data()
    if not booking_data.empty:
        # Display data in a table/grid
        st.dataframe(booking_data)
        
        # Dropdown to select a booking ID
        book_id_list = booking_data['book_id'].tolist()
        selected_book_id = st.selectbox("Select Booking ID to Confirm", book_id_list)
        
        # Confirm button
        if st.button("CONFIRM"):
            update_payment_status(selected_book_id)
    else:
        st.write("No pending bookings available.")

# Run this function only if this script is executed directly
if __name__ == "__main__":
    show_approve_management()
