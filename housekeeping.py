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

def get_booking_info():
    """Retrieve specific columns (cot_id and check_out_date) from the BOOKING table where payment_status is 2."""
    query = """
        SELECT cot_id, check_out_date
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

# Streamlit UI for displaying booking info and housekeeping tasks
def show_housekeeping():
    st.subheader("Booking and Housekeeping Management")
    
    # Display booking information
    st.write("### Booked Cottages (Booking Table)")
    booking_data = get_booking_info()
    if booking_data:
        booking_df = pd.DataFrame(booking_data)
        st.dataframe(booking_df)
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
            st.experimental_rerun()
    else:
        st.warning("No housekeeping tasks found.")

# Run this function if the script is executed directly
if __name__ == "__main__":
    show_housekeeping()
