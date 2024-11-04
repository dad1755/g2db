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

def get_staff():
    """Retrieve all staff members."""
    query = "SELECT staff_id, staff_name FROM STAFF"
    staff = fetch_data(query)
    return staff

def confirm_payment(book_id, staff_id, cottage_id):
   




# Streamlit UI for displaying booking details
def show_approve_management():
    st.subheader("Booking Management")
    st.write("Available Bookings (Pending Confirmation Will Be List Here)")
    
    bookings_data = get_bookings()
    if bookings_data:
        # Display bookings as a DataFrame for a cleaner output
        bookings_df = pd.DataFrame(bookings_data)
        st.dataframe(bookings_df)

        # Fetch staff data for selection
        staff_data = get_staff()
        staff_options = {f"{staff['staff_name']} (ID: {staff['staff_id']})": staff['staff_id'] for staff in staff_data}

        # Payment confirmation form
        st.write("### Confirm Payment")
        selected_book_id = st.selectbox("Select Booking ID to Confirm", bookings_df['book_id'].values)
        
        # Staff selection
        selected_staff_name = st.selectbox("Select Staff", options=list(staff_options.keys()))
        selected_staff_id = staff_options[selected_staff_name]  # Get the ID based on the selected name
        
        # Retrieve cottage ID based on selected booking
        selected_booking = bookings_df[bookings_df['book_id'] == selected_book_id].iloc[0]
        selected_cottage_id = selected_booking['cot_id']  # Ensure it's using cot_id
        
        if st.button("CONFIRM"):
            confirm_payment(selected_book_id, selected_staff_id, selected_cottage_id)
            
    else:
        st.warning("All bookings with confirm payment status 👋.")

# Run this function only if this script is executed directly
if __name__ == "__main__":
    show_approve_management()
