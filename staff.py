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
def create_staff(staff_name):
    """Create a new staff member."""
    query = "INSERT INTO STAFF (staff_name) VALUES (%s)"
    execute_query(query, (staff_name,))

def get_staff():
    """Fetch all staff members."""
    query = "SELECT * FROM STAFF"
    return fetch_data(query)

def delete_staff(staff_name):
    """Delete a staff member by name."""
    query = "DELETE FROM STAFF WHERE staff_name = %s"
    execute_query(query, (staff_name,))

def show_staff_management():
    """Streamlit UI for Staff Management."""
    st.subheader("Staff Management")

    # Add Staff
    st.write("### Add Staff")
    staff_name = st.text_input("Staff Name")
    if st.button("Add Staff"):
        if staff_name:
            create_staff(staff_name)
            st.success(f"Added Staff: {staff_name}")
        else:
            st.warning("Please enter a Staff Name.")

    # View Staff
    st.write("### Staff List")
    staff_data = get_staff()
    if staff_data:
        st.dataframe(staff_data)

        # Delete Staff
        st.write("### Delete Staff")
        staff_name_to_delete = st.text_input("Enter Staff Name to delete")
        if st.button("Delete Staff"):
            if staff_name_to_delete:
                delete_staff(staff_name_to_delete)
                st.success(f"Deleted Staff with Name: {staff_name_to_delete}")
            else:
                st.warning("Please enter a Staff Name to delete.")
    else:
        st.warning("No staff members found.")

# Call the show_staff_management function to display the UI
if __name__ == "__main__":
    show_staff_management()
