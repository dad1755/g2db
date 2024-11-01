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

def insert_housekeeping_task(book_id, cot_id, check_out_date, staff_id):
    """Insert a new housekeeping task into the HOUSEKEEPING table."""
    query = """
        INSERT INTO HOUSEKEEPING (book_id, cot_id, check_out_date, ct_id_stat, staff_id) 
        VALUES (%s, %s, %s, 1, %s)  -- Assuming '1' indicates 'assigned'
    """
    execute_query(query, (book_id, cot_id, check_out_date, staff_id))
    st.success("New housekeeping task created successfully.")

def get_booking_info():
    """Retrieve specific columns (cot_id and check_out_date) from the BOOKING table where payment_status is 2."""
    query = """
        SELECT book_id, cot_id, check_out_date
        FROM BOOKING
        WHERE payment_status = 2
    """
    booking_info = fetch_data(query)
    return booking_info

def get_housekeeping_tasks():
    """Retrieve housekeeping tasks from HOUSEKEEPING table."""
    query = """
        SELECT housekeep_id, book_id, cot_id, check_out_date, ct_id_stat, staff_id 
        FROM HOUSEKEEPING
    """
    housekeeping_tasks = fetch_data(query)
    return housekeeping_tasks

def mark_task_complete(housekeep_id):
    """Mark a housekeeping task as complete by updating the ct_id_stat."""
    query = """
        UPDATE HOUSEKEEPING 
        SET ct_id_stat = 4  -- Assuming '4' indicates 'completed'
        WHERE housekeep_id = %s
    """
    execute_query(query, (housekeep_id,))
    st.success(f"Housekeeping task {housekeep_id} marked as complete.")

def get_staff_list():
    """Retrieve staff_id and staff_name from the STAFF table."""
    query = """
        SELECT staff_id, staff_name
        FROM STAFF
    """
    staff_list = fetch_data(query)
    return staff_list

def get_cottage_ids():
    """Retrieve only the `cot_id` values from the `BOOKING` table where `payment_status` is 2."""
    query = """
        SELECT cot_id
        FROM BOOKING
        WHERE payment_status = 2
    """
    cottage_ids = fetch_data(query)
    return [item['cot_id'] for item in cottage_ids]  # Return only `cot_id` values as a list

def show_housekeeping():
    st.subheader("Booking and Housekeeping Management")

    # Display booking information
    st.write("### Booked Cottages (Booking Table)")
    booking_data = get_booking_info()
    if booking_data:
        booking_df = pd.DataFrame(booking_data)
        st.dataframe(booking_df)

        # Fetch and display staff list for assignment
        staff_list = get_staff_list()
        
        if staff_list:
            staff_df = pd.DataFrame(staff_list)

            # Dropdowns for task assignment
            st.write("### Assign Staff to Housekeeping Task")
            selected_booking = st.selectbox("Select Booking", booking_df['book_id'].values, 
                                             format_func=lambda x: f"Booking ID: {x}")

            # Use native Python types
            selected_booking_row = booking_df.loc[booking_df['book_id'] == selected_booking]
            selected_cot_id = int(selected_booking_row['cot_id'].values[0])  # Convert to int
            selected_check_out_date = str(selected_booking_row['check_out_date'].values[0])  # Convert to str

            selected_staff_id = st.selectbox(
                "Select Staff Member",
                staff_df['staff_id'].values,
                format_func=lambda x: staff_df[staff_df['staff_id'] == x]['staff_name'].values[0]
            )

            if st.button("Assign"):
                insert_housekeeping_task(selected_booking, selected_cot_id, selected_check_out_date, int(selected_staff_id))  # Convert to int
                st.experimental_rerun()
        else:
            st.warning("No staff data found.")

    else:
        st.warning("No booking data found.")

    # Display housekeeping tasks
    st.write("### Housekeeping Tasks (Housekeeping Table)")
    housekeeping_data = get_housekeeping_tasks()
    if housekeeping_data:
        housekeeping_df = pd.DataFrame(housekeeping_data)
        st.dataframe(housekeeping_df)

        # Selection for marking task complete
        selected_task_id = st.selectbox("Select Task ID to Mark as Complete", housekeeping_df['housekeep_id'].values)
        
        if st.button("Mark Task Complete"):
            mark_task_complete(selected_task_id)
            st.rerun()
    else:
        st.warning("No housekeeping tasks found.")


# Run this function if the script is executed directly
if __name__ == "__main__":
    show_housekeeping()
