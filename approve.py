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
    """Execute a query with optional parameters."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(query, params if params else ())
        connection.commit()
    except Error as e:
        st.error(f"Error: {e}")
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
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to retrieve all bookings
def get_bookings():
    """Retrieve all bookings."""
    query = "SELECT * FROM BOOKING"
    return fetch_data(query)

# Function to retrieve all payment statuses
def get_payment_statuses():
    """Retrieve all payment statuses."""
    query = "SELECT * FROM PAYMENT_STATUS"
    return fetch_data(query)

# Function to retrieve all staff members
def get_staff_members():
    """Retrieve all staff members."""
    query = "SELECT * FROM STAFF"
    return fetch_data(query)

# Streamlit UI for displaying booking details
def show_booking_management():
    st.subheader("Booking Management")
    st.write("### Available Bookings")
    bookings_data = get_bookings()
    if bookings_data:
        st.dataframe(bookings_data)
    else:
        st.warning("No bookings found.")

# Approve payment and update payment status in the Booking table
def approve_payment():
    st.subheader("Approve Payment")
    bookings_data = get_bookings()
    payment_statuses = get_payment_statuses()
    staff_members = get_staff_members()

    if bookings_data and payment_statuses and staff_members:
        booking_ids = [booking['book_id'] for booking in bookings_data]
        payment_status_ids = [status['pay_id'] for status in payment_statuses]
        staff_ids = [staff['staff_id'] for staff in staff_members]

        with st.form(key='approve_payment_form'):
            selected_booking_id = st.selectbox("Select Booking ID", booking_ids)
            selected_payment_status = st.selectbox("Select Payment Status", payment_status_ids)
            selected_staff_id = st.selectbox("Select Staff Member", staff_ids)

            submit_button = st.form_submit_button(label='Approve Payment')

            if submit_button:
                # Update payment status in BOOKING table
                update_query = """
                    UPDATE BOOKING
                    SET payment_status = %s
                    WHERE book_id = %s
                """
                execute_query(update_query, (selected_payment_status, selected_booking_id))

                # Insert into PAYMENT_CONFIRMATION table
                confirmation_query = """
                    INSERT INTO PAYMENT_CONFIRMATION (book_id, staff_id)
                    VALUES (%s, %s)
                """
                execute_query(confirmation_query, (selected_booking_id, selected_staff_id))
                
                st.success("Payment approved and status updated successfully.")

# Execute the booking management function to show the UI
show_booking_management()
approve_payment()
