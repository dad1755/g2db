import streamlit as st
import mysql.connector
from mysql.connector import Error

# Hardcoded database configuration (make sure to secure your credentials)
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
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor  # Return cursor for further processing
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_data(query):
    """Fetch data from the database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows  # Return fetched rows
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Staff Management Functions
def create_staff(name, role):
    """Create a new staff member."""
    query = "INSERT INTO STAFF (name, role) VALUES (%s, %s)"
    execute_query(query, (name, role))

def get_staff():
    """Fetch all staff members."""
    query = "SELECT * FROM STAFF"
    return fetch_data(query)

def delete_staff(staff_id):
    """Delete a staff member by ID."""
    query = "DELETE FROM STAFF WHERE id = %s"
    execute_query(query, (staff_id,))

def show_staff_management():
    """Streamlit UI for Staff Management."""
    st.subheader("Staff Management")

    # Add Staff
    st.write("### Add Staff")
    name = st.text_input("Staff Name")
    role = st.text_input("Staff Role")
    if st.button("Add Staff"):
        if name and role:
            create_staff(name, role)
            st.success(f"Added Staff: {name}")
        else:
            st.warning("Please enter both Staff Name and Role.")

    # View Staff
    st.write("### Staff List")
    staff_data = get_staff()
    if staff_data:
        st.dataframe(staff_data)

        # Delete Staff
        st.write("### Delete Staff")
        staff_id_to_delete = st.text_input("Enter Staff ID to delete")
        if st.button("Delete Staff"):
            if staff_id_to_delete:
                delete_staff(staff_id_to_delete)
                st.success(f"Deleted Staff with ID: {staff_id_to_delete}")
            else:
                st.warning("Please enter a Staff ID to delete.")
    else:
        st.warning("No staff members found.")
