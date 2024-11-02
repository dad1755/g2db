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

    # Get assigned cottage IDs
    assigned_cottage_ids = get_assigned_cottage_ids()

    # Display booking information
    st.write("### Booked Cottages (Booking Table)")
    booking_data = get_booking_info()
    
    if booking_data:
        booking_df = pd.DataFrame(booking_data)

        # Filter out cottages that have already been assigned tasks
        available_bookings = booking_df[~booking_df['cot_id'].isin(assigned_cottage_ids)]
        
        st.dataframe(available_bookings)

        if not available_bookings.empty:
            # Fetch and display staff list for assignment
            staff_list = get_staff_list()
            st.write("Staff List:", staff_list)  # Debugging line
            
            if staff_list:
                staff_df = pd.DataFrame(staff_list)

                # Dropdowns for task assignment
                st.write("### Assign Staff to Housekeeping Task")
                selected_booking = st.selectbox("Select Booking", available_bookings['book_id'].values, 
                                                 format_func=lambda x: f"Booking ID: {x}")

                # Use native Python types
                selected_booking_row = available_bookings.loc[available_bookings['book_id'] == selected_booking]
                selected_cot_id = int(selected_booking_row['cot_id'].values[0])  # Convert to int
                selected_check_out_date = str(selected_booking_row['check_out_date'].values[0])  # Convert to str

                selected_staff_id = st.selectbox(
                    "Select Staff Member",
                    staff_df['staff_id'].values,
                    format_func=lambda x: staff_df[staff_df['staff_id'] == x]['staff_name'].values[0]
                )

                if st.button("Assign"):
                    insert_housekeeping_task(selected_booking, selected_cot_id, selected_check_out_date, int(selected_staff_id))  # Convert to int
                    st.rerun()
            else:
                st.warning("No staff data found.")
        else:
            st.warning("All cottages have already been assigned tasks.")

    else:
        st.warning("No booking data found.")
def mark_task_complete(housekeep_id):
    """Mark a housekeeping task as complete by updating the ct_id_stat."""
    # First, update the HOUSEKEEPING table
    query_update_housekeeping = """
        UPDATE HOUSEKEEPING 
        SET ct_id_stat = 4  -- Assuming '4' indicates 'completed'
        WHERE housekeep_id = %s
    """
    execute_query(query_update_housekeeping, (housekeep_id,))

    # Now retrieve the associated cot_id for the housekeeping task
    query_get_cot_id = """
        SELECT cot_id FROM HOUSEKEEPING WHERE housekeep_id = %s
    """
    cot_id_data = fetch_data(query_get_cot_id, (housekeep_id,))
    if cot_id_data:
        cot_id = cot_id_data[0]['cot_id']

        # Update the COTTAGE_ATTRIBUTES_RELATION table
        query_update_cottage = """
            UPDATE COTTAGE_ATTRIBUTES_RELATION 
            SET ct_id_stat = 2  -- Assuming '2' indicates some specific status, e.g., 'not available'
            WHERE cot_id = %s
        """
        execute_query(query_update_cottage, (cot_id,))
        st.success(f"Housekeeping task {housekeep_id} marked as complete and cottage {cot_id} updated.")
    else:
        st.error(f"Could not retrieve cottage ID for task {housekeep_id}.")





# Run this function if the script is executed directly
if __name__ == "__main__":
    show_housekeeping()
