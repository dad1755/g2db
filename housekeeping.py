import mysql.connector
import pandas as pd
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
        SELECT book_id, cot_id, check_out_date
        FROM BOOKING
        WHERE payment_status = 2
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    except Error as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there's an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_staff_data():
    """Fetch all staff members from the STAFF table."""
    query = "SELECT staff_id, staff_name FROM STAFF"
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    except Error as e:
        st.error(f"Error fetching staff data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there's an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def assign_staff_to_booking(book_id, staff_id, cot_id, check_out_date):
    """Assign staff to a booking and update the HOUSEKEEPING table."""
    ct_id_stat = 1  # Assuming '1' corresponds to 'Out-Of-Order' status in COTTAGE_STATUS

    book_id = int(book_id)
    staff_id = int(staff_id)
    cot_id = int(cot_id)
    check_out_date = pd.to_datetime(check_out_date).date()

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
    except Error as e:
        st.error(f"Error assigning staff to booking: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_housekeeping_data():
    """Fetch all records from the HOUSEKEEPING table."""
    query = "SELECT * FROM HOUSEKEEPING"
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    except Error as e:
        st.error(f"Error fetching housekeeping data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there's an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def show_housekeeping():
    """Display housekeeping booking data with payment_status = 2 in Streamlit."""
    st.subheader("Booking On Going")
    
    # Fetch booking and housekeeping data
    booking_data = fetch_booking_data()
    housekeeping_data = fetch_housekeeping_data()

    if not booking_data.empty:
        # If housekeeping data is available, filter out cot_ids present in housekeeping
        if not housekeeping_data.empty:
            # Create a set of existing cot_id's from the housekeeping data for faster lookup
            existing_cot_ids = set(housekeeping_data['cot_id'])

            # Filter booking data to only include cot_ids not in housekeeping
            filtered_booking_data = booking_data[~booking_data['cot_id'].isin(existing_cot_ids)]
        else:
            # If there are no housekeeping records, show all booking data
            filtered_booking_data = booking_data

        if not filtered_booking_data.empty:
            st.dataframe(filtered_booking_data)

            # Fetch staff data for assignment
            staff_data = fetch_staff_data()

            # Dropdown for assigning staff
            staff_options = staff_data.set_index('staff_id')['staff_name'].to_dict()
            selected_staff = st.selectbox("Select Staff", options=list(staff_options.keys()), format_func=lambda x: staff_options[x] if x in staff_options else "")
            
            # Get the selected booking information
            selected_booking = st.selectbox("Select Booking", options=filtered_booking_data['book_id'])
            selected_row = filtered_booking_data[filtered_booking_data['book_id'] == selected_booking].iloc[0]

            # Button to assign staff
            if st.button("Assign Staff"):
                assign_staff_to_booking(selected_row['book_id'], selected_staff, selected_row['cot_id'], selected_row['check_out_date'])
        else:
            st.warning("No bookings available that are not already assigned in housekeeping.")
    else:
        st.warning("No booking data found with payment_status = 2.")

    # Always show the housekeeping records
    st.subheader("Housekeeping Records")
    if not housekeeping_data.empty:
        st.dataframe(housekeeping_data)
    else:
        st.warning("No housekeeping records found.")


    # Always show the housekeeping records
    st.subheader("Housekeeping Records")
    if not housekeeping_data.empty:
        st.dataframe(housekeeping_data)
    else:
        st.warning("No housekeeping records found.")

# Run the app
if __name__ == "__main__":
    st.title("Housekeeping Management")
    show_housekeeping()
