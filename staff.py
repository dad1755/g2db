import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database connection details
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def execute_query(query, params=None):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor  # Return the cursor for further processing if needed
    except Error as e:
        st.error(f"Error: {e}")
        return None  # Return None to signal failure
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS STAFF (
        staff_id INT AUTO_INCREMENT PRIMARY KEY,
        staff_name VARCHAR(100) NOT NULL
    )
    """
    execute_query(query)

def add_staff(staff_name):
    query = "INSERT INTO STAFF (staff_name) VALUES (%s)"
    result = execute_query(query, (staff_name,))
    if result is None:  # Check if the result is None
        st.error("Error while adding staff.")
    else:
        st.success(f"Added staff member: {staff_name}")

def delete_staff(staff_id):
    query = "DELETE FROM STAFF WHERE staff_id = %s"
    result = execute_query(query, (staff_id,))
    if result is None:
        st.error("Error while deleting staff.")
    elif result.rowcount > 0:
        st.success(f"Deleted staff member with ID: {staff_id}")
    else:
        st.warning(f"No staff member found with ID: {staff_id}")

def get_staff():
    query = "SELECT * FROM STAFF"
    return fetch_data(query)

def show_staff_management():
    st.subheader("Staff Management")
    create_table()

    # Add Staff
    st.write("### Add Staff Member")
    staff_name = st.text_input("Staff Name")
    if st.button("Add Staff"):
        if staff_name:
            add_staff(staff_name)
        else:
            st.warning("Please enter Staff Name.")

    # View Staff
    st.write("### Available Staff")
    staff_data = get_staff()
    if staff_data is not None and not staff_data.empty:
        st.dataframe(staff_data)

        # Delete Staff
        st.write("### Delete Staff Member")
        staff_id_to_delete = st.number_input("Enter Staff ID to delete", min_value=1)
        if st.button("Delete Staff"):
            if staff_id_to_delete:
                delete_staff(staff_id_to_delete)
            else:
                st.warning("Please enter a Staff ID to delete.")
    else:
        st.warning("No staff members found.")
