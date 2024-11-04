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

def execute_query(query, params=None):
    """Execute a query with optional parameters."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(query, params if params else ())
        connection.commit()
    except Error as e:
        st.error(f"Error executing query: {e}")
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
        st.error(f"Error fetching data: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_bookings():
    """Retrieve all bookings with payment_status = 1."""
    query = """
        SELECT book_id, cust_id, cot_id, check_in_date, check_out_date, payment_types, payment_status, dis_id 
        FROM BOOKING 
        WHERE payment_status = 1
    """
    bookings = fetch_data(query)
    return bookings

def confirm_payment(book_id, cottage_id):
    """Confirm the payment for the booking and delete other bookings with the same cottage ID if any exist."""
    try:
        # Update the booking status to confirmed (assuming 2 indicates confirmed)
        update_query = """
            UPDATE BOOKING 
            SET payment_status = 2
            WHERE book_id = %s
        """
        execute_query(update_query, (book_id,))  # Update only the payment_status

        # Check for other bookings with the same cottage ID
        check_query = """
            SELECT book_id FROM BOOKING 
            WHERE cot_id = %s AND book_id != %s
        """
        other_bookings = fetch_data(check_query, (cottage_id, book_id))
        
        # If there are other bookings, delete them
        if other_bookings:
            delete_query = """
                DELETE FROM BOOKING 
                WHERE cot_id = %s AND book_id != %s
            """
            execute_query(delete_query, (cottage_id, book_id))  # Delete other bookings with the same cot_id
            st.success(f"Other bookings with cottage ID {cottage_id} have been deleted.")
        else:
            st.info(f"No other bookings with cottage ID {cottage_id} to delete.")

        # Notify the user of the successful payment confirmation
        st.success(f"Payment for booking ID {book_id} has been confirmed successfully.")
        
    except Error as e:
        st.error(f"An error occurred while confirming payment: {e}")

# Streamlit UI for displaying booking details
def show_approve_management():
    st.subheader("Booking Management")
    st.write("Available Bookings (Pending Confirmation Will Be Listed Here)")
    
    bookings_data = get_bookings()
    if bookings_data:
        # Display bookings as a DataFrame for a cleaner output
        bookings_df = pd.DataFrame(bookings_data)
        st.dataframe(bookings_df)

        # Payment confirmation form
        st.write("### Confirm Payment")
        selected_book_id = st.selectbox("Select Booking ID to Confirm", bookings_df['book_id'].values)
        
        # Retrieve cottage ID based on selected booking
        selected_booking = bookings_df[bookings_df['book_id'] == selected_book_id].iloc[0]
        selected_cottage_id = int(selected_booking['cot_id'])  # Ensure it's using cot_id and convert to int
        
        if st.button("CONFIRM"):
            confirm_payment(selected_book_id, selected_cottage_id)
            
    else:
        st.warning("All bookings with confirm payment status 👋.")

# Run this function only if this script is executed directly
if __name__ == "__main__":
    show_approve_management()
