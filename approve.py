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
    """Retrieve all bookings with formatted dates for readability."""
    query = "SELECT * FROM BOOKING"
    bookings = fetch_data(query)
    
    # Format dates to readable string format
    for booking in bookings:
        if booking.get("check_in_date"):
            booking["check_in_date"] = booking["check_in_date"].strftime("%Y-%m-%d")
        if booking.get("check_out_date"):
            booking["check_out_date"] = booking["check_out_date"].strftime("%Y-%m-%d")

    return bookings

def confirm_payment(book_id, staff_id, cottage_id):
    """Confirm payment for a booking, update booking and cottage status."""
    
    try:
        # Insert a new record into PAYMENT_CONFIRMATION
        payment_query = """
            INSERT INTO PAYMENT_CONFIRMATION (book_id, staff_id)
            VALUES (%s, %s)
        """
        execute_query(payment_query, (book_id, staff_id))

        # Check for existing bookings to delete
        check_query = "SELECT * FROM BOOKING WHERE cot_id = %s AND book_id != %s"
        existing_bookings = fetch_data(check_query, (cottage_id, book_id))
        
        if not existing_bookings:
            st.warning("No overlapping bookings found to delete.")
        else:
            # Debugging output
            st.write(f"Deleting bookings with cottage_id: {cottage_id} and book_id: {book_id}")

            # Delete overlapping bookings with the same cot_id
            delete_query = """
                DELETE FROM BOOKING WHERE cot_id = %s AND book_id != %s
            """
            execute_query(delete_query, (cottage_id, book_id))

        # Update the cottage status to "Unavailable" in the COTTAGE_STATUS table
        update_status_query = """
            UPDATE COTTAGE_STATUS SET ct_details = 'Unavailable' WHERE cottage_status_id = %s
        """
        execute_query(update_status_query, (cottage_id,))
        
        st.success("Payment confirmed and cottage status updated.")

    except Error as e:
        st.error(f"Error confirming payment: {e}")

# Streamlit UI for displaying booking details
def show_approve_management():
    st.subheader("Booking Management")
    st.write("### Available Bookings")
    
    bookings_data = get_bookings()
    if bookings_data:
        # Display bookings as a DataFrame for a cleaner output
        bookings_df = pd.DataFrame(bookings_data)
        st.dataframe(bookings_df)

        # Payment confirmation form
        st.write("### Confirm Payment")
        selected_book_id = st.selectbox("Select Booking ID to Confirm", bookings_df['book_id'].values)
        selected_staff_id = st.number_input("Enter Staff ID", min_value=1, step=1)
        
        # Retrieve cottage ID based on selected booking
        selected_booking = bookings_df[bookings_df['book_id'] == selected_book_id].iloc[0]
        
        # Access the correct column name 'cot_id'
        selected_cottage_id = selected_booking['cot_id']  # Ensure it's using cot_id
        
        if st.button("CONFIRM"):
            confirm_payment(selected_book_id, selected_staff_id, selected_cottage_id)
            
    else:
        st.warning("No bookings found.")

# Run this function only if approve.py is executed directly
if __name__ == "__main__":
    show_approve_management()
