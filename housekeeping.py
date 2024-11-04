import mysql.connector
import streamlit as st
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def fetch_booking_data():
    """Fetch book_id, cot_id, and check_out_date from BOOKING table where payment_status is 2."""
    query = """
        SELECT book_id, cot_id, check_id, check_out_date
        FROM BOOKING
        WHERE payment_status = 2
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        return result  # Return list of dictionaries
    except Error as e:
        st.error(f"Error fetching data: {e}")
        return []  # Return empty list if there's an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()  # Close the connection

def fetch_staff_data():
    """Fetch all staff members from the STAFF table."""
    query = "SELECT staff_id, staff_name FROM STAFF"
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        return result  # Return list of dictionaries
    except Error as e:
        st.error(f"Error fetching staff data: {e}")
        return []  # Return empty list if there's an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()  # Close the connection

def fetch_housekeeping_data():
    """Fetch all records from the HOUSEKEEPING table."""
    query = "SELECT * FROM HOUSEKEEPING"
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        return result  # Return list of dictionaries
    except Error as e:
        st.error(f"Error fetching housekeeping data: {e}")
        return []  # Return empty list if there's an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()  # Close the connection

def assign_staff_to_booking(book_id, staff_id, cot_id, check_out_date):
    """Assign staff to a booking and update the HOUSEKEEPING table."""
    ct_id_stat = 3  # Assuming '3' corresponds to the status for staff assignment

    query = """
        INSERT INTO HOUSEKEEPING (book_id, cot_id, check_out_date, ct_id_stat, staff_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(query, (book_id, cot_id, check_out_date, ct_id_stat, staff_id))
        connection.commit()
        st.success("Staff assigned to booking successfully!")

        # Refresh the session state to update the DataFrames
        st.session_state.booking_data = fetch_booking_data()
        st.session_state.housekeeping_data = fetch_housekeeping_data()
        
    except Error as e:
        st.error(f"Error assigning staff to booking: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()  # Close the connection

def show_housekeeping():
    """Display housekeeping booking data with payment_status = 2 in Streamlit."""
  
    # Use session state to store data
    if 'booking_data' not in st.session_state:
        st.session_state.booking_data = fetch_booking_data()

    if 'housekeeping_data' not in st.session_state:
        st.session_state.housekeeping_data = fetch_housekeeping_data()

    booking_data = st.session_state.booking_data
    housekeeping_data = st.session_state.housekeeping_data

    # Display booking data if available
    if booking_data and housekeeping_data:
        # Create a list of cot_id's from the housekeeping data
        existing_cot_ids = [h['cot_id'] for h in housekeeping_data]

        # Filter booking data to only include cot_ids not in housekeeping
        filtered_booking_data = [b for b in booking_data if b['cot_id'] not in existing_cot_ids]

        if filtered_booking_data:
            st.write("### Available Bookings:")
            st.write(filtered_booking_data)

            # Dropdown for assigning staff
            staff_data = fetch_staff_data()
            staff_options = {staff['staff_id']: staff['staff_name'] for staff in staff_data}
            selected_staff_id = st.selectbox("Select Staff", options=list(staff_options.keys()), format_func=lambda x: staff_options[x])

            # Get the selected booking information
            selected_booking_id = st.selectbox("Select Booking", options=[b['book_id'] for b in filtered_booking_data])
            selected_booking = next(b for b in filtered_booking_data if b['book_id'] == selected_booking_id)

            # Button to assign staff
            if st.button("Assign Staff"):
                assign_staff_to_booking(selected_booking['book_id'], selected_staff_id, selected_booking['cot_id'], selected_booking['check_out_date'])

                # Automatically refresh the booking data
                st.session_state.booking_data = fetch_booking_data()
                st.session_state.housekeeping_data = fetch_housekeeping_data()

        else:
            st.warning("No booking data available that is not already assigned in housekeeping.")
    else:
        st.warning("No booking data or housekeeping data available.")

# Run the app
if __name__ == "__main__":
    st.title("Housekeeping Management")
    show_housekeeping()
