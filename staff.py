import streamlit as st
from utils.db_utils import execute_query, fetch_data

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
    if isinstance(result, Error):
        st.error(f"Error while adding staff: {result}")
    else:
        st.success(f"Added staff member: {staff_name}")

def delete_staff(staff_id):
    query = "DELETE FROM STAFF WHERE staff_id = %s"
    result = execute_query(query, (staff_id,))
    if isinstance(result, Error):
        st.error(f"Error while deleting staff: {result}")
    elif result.rowcount > 0:
        st.success(f"Deleted staff member with ID: {staff_id}")
    else:
        st.warning(f"No staff member found with ID: {staff_id}")

def get_staff():
    query = "SELECT * FROM STAFF"
    return fetch_data(query)

def show_staff_management():
    st.subheader("Staff Management")
    
    # Ensure STAFF table exists
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
    if not staff_data.empty:
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
