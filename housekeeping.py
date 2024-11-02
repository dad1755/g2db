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


def get_staff_list():
    """Retrieve staff_id and staff_name from the STAFF table."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT staff_id, staff_name
                FROM STAFF
            """
            cursor.execute(query)
            staff_list = cursor.fetchall()
            if not staff_list:
                st.warning("No data returned from STAFF table.")
            return staff_list
    except Error as e:
        st.error(f"Error connecting to the database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def get_cottage_ids():
    """Retrieve only the cot_id values from the BOOKING table where payment_status is 2."""
    query = """
        SELECT cot_id
        FROM BOOKING
        WHERE payment_status = 2
    """
    cottage_ids = fetch_data(query)
    return [item['cot_id'] for item in cottage_ids]  # Return only cot_id values as a list

def get_assigned_cottage_ids():
    """Retrieve cottage IDs that are already assigned tasks in the HOUSEKEEPING table."""
    query = """
        SELECT DISTINCT cot_id
        FROM HOUSEKEEPING
    """
    assigned_cottage_ids = fetch_data(query)
    return [item['cot_id'] for item in assigned_cottage_ids]  # Return only cot_id values as a list

def show_housekeeping():
    st.subheader("Booking and Housekeeping Management")

    # Existing code for displaying bookings and assigning staff...
    
    # Add a section for marking tasks complete
    st.write("### Mark Housekeeping Task as Complete")
    
    # Fetch and display existing housekeeping tasks
    housekeeping_tasks = get_housekeeping_tasks()
    
    if housekeeping_tasks:
        housekeeping_df = pd.DataFrame(housekeeping_tasks)

        # Display existing tasks
        st.dataframe(housekeeping_df)

        # Allow user to select a task to mark as complete
        selected_task = st.selectbox("Select Housekeeping Task", housekeeping_df['housekeep_id'].values, 
                                       format_func=lambda x: f"Task ID: {x}")

        if st.button("Mark Task Complete"):
            mark_task_complete(selected_task)  # Call the modified function
            st.rerun()  # Rerun the app to refresh the display
    else:
        st.warning("No housekeeping tasks found.")

def mark_task_complete(housekeep_id):
    """Mark a housekeeping task as complete by deleting the entry in the HOUSEKEEPING table
       and updating the COTTAGE_STATUS table."""
    st.write(f"Attempting to mark task {housekeep_id} as complete.")  # Debug statement

    # First, retrieve the associated cot_id for the housekeeping task
    query_get_cot_id = """
        SELECT cot_id, ct_id_stat FROM HOUSEKEEPING WHERE housekeep_id = %s
    """
    cot_id_data = fetch_data(query_get_cot_id, (housekeep_id,))
    
    if cot_id_data:
        cot_id = cot_id_data[0]['cot_id']
        ct_id_stat = cot_id_data[0]['ct_id_stat']
        st.write(f"Cot ID retrieved: {cot_id}, ct_id_stat: {ct_id_stat}")  # Debug statement
        
        # Update the COTTAGE_STATUS table if necessary
        # You may need to update ct_id_stat to a valid status or set it to null
        query_update_cottage_status = """
            UPDATE COTTAGE_STATUS 
            SET ct_status_details = 2  -- Set status to '2'
            WHERE cottage_status_id = %s  -- Assuming cottage_status_id relates to cot_id
        """
        execute_query(query_update_cottage_status, (cot_id,))

        # Now, delete the housekeeping task from the HOUSEKEEPING table
        query_delete_housekeeping = """
            DELETE FROM HOUSEKEEPING 
            WHERE housekeep_id = %s
        """
        execute_query(query_delete_housekeeping, (housekeep_id,))
        st.success(f"Housekeeping task {housekeep_id} has been marked as complete and deleted. Cottage status updated.")
    else:
        st.error(f"Could not retrieve cottage ID for task {housekeep_id}.")





# Run this function if the script is executed directly
if __name__ == "__main__":
    show_housekeeping()
