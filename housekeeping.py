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

def fetch_cottage_attributes_data():
    """Fetch all records from the COTTAGE_ATTRIBUTES_RELATION table."""
    query = "SELECT * FROM COTTAGE_ATTRIBUTES_RELATION"
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    except Error as e:
        st.error(f"Error fetching cottage attributes data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there's an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def assign_staff_to_booking(book_id, staff_id, cot_id, check_out_date):
    """Assign staff to a booking and update the HOUSEKEEPING table."""
    ct_id_stat = 3  # Assuming '3' corresponds to the status for staff assignment

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

        # Refresh the session state to update the DataFrames
        st.session_state.booking_data = fetch_booking_data()
        st.session_state.housekeeping_data = fetch_housekeeping_data()
        
    except Error as e:
        st.error(f"Error assigning staff to booking: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def show_housekeeping():
    """Display housekeeping booking data with payment_status = 2 in Streamlit."""
    st.subheader("Booking On Going")
    
    # Use session state to store DataFrames
    if 'booking_data' not in st.session_state:
        st.session_state.booking_data = fetch_booking_data()

    if 'housekeeping_data' not in st.session_state:
        st.session_state.housekeeping_data = fetch_housekeeping_data()

    if 'cottage_attributes_data' not in st.session_state:
        st.session_state.cottage_attributes_data = fetch_cottage_attributes_data()

    booking_data = st.session_state.booking_data
    housekeeping_data = st.session_state.housekeeping_data
    cottage_attributes_data = st.session_state.cottage_attributes_data

    if not booking_data.empty and not housekeeping_data.empty:
        # Create a list of cot_id's from the housekeeping data
        existing_cot_ids = housekeeping_data['cot_id'].unique()

        # Filter booking data to only include cot_ids not in housekeeping
        filtered_booking_data = booking_data[~booking_data['cot_id'].isin(existing_cot_ids)]

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

                # Automatically update the DataFrame displayed after assigning staff
                booking_data = fetch_booking_data()  # Refresh booking data
                housekeeping_data = fetch_housekeeping_data()  # Refresh housekeeping data
                st.session_state.booking_data = booking_data
                st.session_state.housekeeping_data = housekeeping_data

        else:
            st.warning("No booking data available that is not already assigned in housekeeping.")

    elif not booking_data.empty:
        st.warning("No booking data found with payment_status = 2.")

    # Display bookings related to ct_id_stat = 3
    st.subheader("Bookings Related to Cottage with ct_id_stat = 3")
    if not cottage_attributes_data.empty:
        # Filter cottage attributes for ct_id_stat = 3
        filtered_cottages = cottage_attributes_data[cottage_attributes_data['ct_id_stat'] == 3]
        
        if not filtered_cottages.empty:
            # Merge to get the relevant bookings
            relevant_bookings = pd.merge(
                booking_data,
                filtered_cottages[['cot_id']],  # Only need cot_id for the merge
                on='cot_id',
                how='inner'  # Only keep bookings that match
            )

            if not relevant_bookings.empty:
                # Show the relevant booking data
                st.dataframe(relevant_bookings[['book_id', 'cot_id', 'check_out_date']])
            else:
                st.warning("No bookings found for cottages with ct_id_stat = 3.")
        else:
            st.warning("No cottages found with ct_id_stat = 3.")
    else:
        st.warning("No cottage attributes data found.")

    # Filter housekeeping data by ct_id_stat = 3 and show in grid
    st.subheader("Filtered Housekeeping Records")
    if not housekeeping_data.empty:
        filtered_housekeeping = housekeeping_data[housekeeping_data['ct_id_stat'] == 3]
        if not filtered_housekeeping.empty:
            st.dataframe(filtered_housekeeping)
        else:
            st.warning("No housekeeping records found with ct_id_stat = 3.")
    else:
        st.warning("No housekeeping records found.")

# Run the app
if __name__ == "__main__":
    st.title("Housekeeping Management")
    show_housekeeping()
