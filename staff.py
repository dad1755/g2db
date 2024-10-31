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
            cursor.execute(query, params)  # Using parameterized queries is good for safety
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
def create_staff(name, role, contact):
    """Create a new staff member."""
    query = "INSERT INTO STAFF (name, role, contact) VALUES (%s, %s, %s)"
    execute_query(query, (name, role, contact))

def get_staff():
    """Fetch all staff members."""
    query = "SELECT * FROM STAFF"
    return fetch_data(query)

def update_staff(staff_id, name, role, contact):
    """Update staff member information."""
    query = "UPDATE STAFF SET name = %s, role = %s, contact = %s WHERE staff_id = %s"
    execute_query(query, (name, role, contact, staff_id))

def delete_staff(staff_id):
    """Delete a staff member by ID."""
    query = "DELETE FROM STAFF WHERE staff_id = %s"
    execute_query(query, (staff_id,))

def show_staff_management():
    """Streamlit UI for Staff Management."""
    st.subheader("Staff Management")

    # Add Staff
    st.write("### Add Staff Member")
    staff_name = st.text_input("Staff Name")
    staff_role = st.text_input("Role")
    staff_contact = st.text_input("Contact")
    if st.button("Add Staff"):
        if staff_name and staff_role and staff_contact:
            create_staff(staff_name, staff_role, staff_contact)
            st.success(f"Added Staff Member: {staff_name}")
        else:
            st.warning("Please fill in all fields.")

    # View Staff
    st.write("### Staff List")
    staff_data = get_staff()
    if staff_data:
        # Display staff data in a dataframe
        st.dataframe(staff_data)

        # Prepare to update a staff member
        st.write("### Update Staff Member")
        staff_names = [f"{staff['name']} (ID: {staff['staff_id']})" for staff in staff_data]
        staff_name_to_update = st.selectbox("Select Staff Member to Update", options=staff_names)
        
        # Extract selected staff ID
        staff_id_to_update = int(staff_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID

        selected_staff = next((staff for staff in staff_data if staff['staff_id'] == staff_id_to_update), None)
        
        if selected_staff:
            updated_name = st.text_input("Updated Name", value=selected_staff['name'])
            updated_role = st.text_input("Updated Role", value=selected_staff['role'])
            updated_contact = st.text_input("Updated Contact", value=selected_staff['contact'])

            if st.button("Update Staff"):
                update_staff(staff_id_to_update, updated_name, updated_role, updated_contact)
                st.success(f"Updated Staff Member: {updated_name}")

        # Prepare to delete a staff member
        st.write("### Delete Staff Member")
        staff_name_to_delete = st.selectbox("Select Staff Member to Delete", options=staff_names)
        
        if st.button("Delete Staff"):
            if staff_name_to_delete:
                delete_staff(staff_id_to_update)
                st.success(f"Deleted Staff Member: {staff_name_to_delete}")
            else:
                st.warning("Please select a Staff Member to delete.")
    else:
        st.warning("No staff members found.")

# Call the show_staff_management function to display the UI
if __name__ == "__main__":
    show_staff_management()
