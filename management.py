import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Database connection details
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

# Function to create the STAFF table if it doesn't exist
def create_table():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS STAFF (
            staff_id VARCHAR(10) PRIMARY KEY,
            staff_name VARCHAR(100) NOT NULL
        )
        """)
        connection.commit()
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to add staff to the database
def add_staff(staff_id, staff_name):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO STAFF (staff_id, staff_name) VALUES (%s, %s)", (staff_id, staff_name))
        connection.commit()
        st.success(f"Added staff member: {staff_name}")
    except Error as e:
        st.error(f"Error while adding staff: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to delete staff from the database
def delete_staff(staff_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM STAFF WHERE staff_id = %s", (staff_id,))
        connection.commit()
        if cursor.rowcount > 0:
            st.success(f"Deleted staff member with ID: {staff_id}")
        else:
            st.warning(f"No staff member found with ID: {staff_id}")
    except Error as e:
        st.error(f"Error while deleting staff: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to retrieve staff data from the database
def get_staff():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        query = "SELECT * FROM STAFF"
        df = pd.read_sql(query, connection)
        return df
    except Error as e:
        st.error(f"Error while fetching staff data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        if connection.is_connected():
            connection.close()

def show_management():
    st.subheader("Management")
    st.write("This is the Management section where you can manage overall operations.")

    # Create tabs for different management functionalities
    tabs = st.tabs(["Payment", "Discount", "Cottage", "Staff"])

    with tabs[3]:  # Staff Tab
        st.subheader("Staff Management")
        
        # Create the STAFF table if it doesn't exist
        create_table()

        # Add Staff
        st.write("### Add Staff Member")
        staff_id = st.text_input("Staff ID (e.g., S001)")
        staff_name = st.text_input("Staff Name")
        if st.button("Add Staff"):
            if staff_id and staff_name:
                add_staff(staff_id, staff_name)
            else:
                st.warning("Please enter both Staff ID and Staff Name.")

        # View Staff
        st.write("### Available Staff")
        staff_data = get_staff()
        if not staff_data.empty:
            st.dataframe(staff_data)

            # Delete Staff
            st.write("### Delete Staff Member")
            staff_id_to_delete = st.text_input("Enter Staff ID to delete")
            if st.button("Delete Staff"):
                if staff_id_to_delete:
                    delete_staff(staff_id_to_delete)
                else:
                    st.warning("Please enter a Staff ID to delete.")
        else:
            st.warning("No staff members found.")
