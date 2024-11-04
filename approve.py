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
            query = "SELECT book_id, cot_id FROM BOOKING WHERE payment_status = 1"
            df = pd.read_sql(query, connection)
            return df
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

# Function to confirm booking and clear others
def confirm_booking(selected_book_id, selected_cot_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Update selected booking to payment_status = 2
            update_query = "UPDATE BOOKING SET payment_status = 2 WHERE book_id = %s"
            cursor.execute(update_query, (selected_book_id,))
            
            # Clear other bookings with the same cot_id
            clear_query = "UPDATE BOOKING SET payment_status = 1 WHERE cot_id = %s AND book_id != %s"
            cursor.execute(clear_query, (selected_cot_id, selected_book_id,))
            
            # Commit changes
            connection.commit()
            st.success(f"Booking {selected_book_id} confirmed and other bookings cleared.")
    except Error as e:
        st.error(f"Error during confirmation: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Streamlit UI for displaying booking details
def show_approve_management():
    st.subheader("Booking Management")
    st.write("Available Bookings (Pending Confirmation Will Be Listed Here)")
    
    bookings_df = fetch_bookings()
    
    if bookings_df is not None and not bookings_df.empty:
        # Create a dropdown to select a book_id
        book_ids = bookings_df['book_id'].unique().tolist()
        selected_book_id = st.selectbox("Select a booking to confirm:", book_ids)
        
        # Get the cot_id of the selected book_id
        selected_cot_id = bookings_df.loc[bookings_df['book_id'] == selected_book_id, 'cot_id'].values[0]

        # Confirm button
        if st.button("Confirm Booking"):
            confirm_booking(selected_book_id, selected_cot_id)
    else:
        st.write("No bookings found with payment status = 1.")

# Run this function only if this script is executed directly
if __name__ == "__main__":
    show_approve_management()
