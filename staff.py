import streamlit as st
import mysql.connector
from mysql.connector import Error

# Hardcoded database configuration
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def show_staff_management():
    st.subheader("Staff Management")
    st.write("This is where you manage staff.")
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

# COTTAGE TABLE CRUD FUNCTIONS
def create_cottage(cot_id, cot_name):
    query = "INSERT INTO COTTAGE (cot_id, cot_name) VALUES (%s, %s)"
    execute_query(query, (cot_id, cot_name))

def get_cottages():
    query = "SELECT * FROM COTTAGE"
    return fetch_data(query)

def delete_cottage(cot_id):
    query = "DELETE FROM COTTAGE WHERE cot_id = %s"
    execute_query(query, (cot_id,))

# Streamlit UI for Cottage Management
def show_cottage_management():
    st.subheader("Cottage Management")

    # Add Cottage
    st.write("### Add Cottage")
    cot_id = st.text_input("Cottage ID")
    cot_name = st.text_input("Cottage Name")
    if st.button("Add Cottage"):
        if cot_id and cot_name:
            create_cottage(cot_id, cot_name)
            st.success(f"Added Cottage: {cot_name}")
        else:
            st.warning("Please enter both Cottage ID and Cottage Name.")

    # View Cottages
    st.write("### Available Cottages")
    cottages_data = get_cottages()
    if cottages_data:
        st.dataframe(cottages_data)

        # Delete Cottage
        st.write("### Delete Cottage")
        cot_id_to_delete = st.text_input("Enter Cottage ID to delete")
        if st.button("Delete Cottage"):
            if cot_id_to_delete:
                delete_cottage(cot_id_to_delete)
                st.success(f"Deleted Cottage with ID: {cot_id_to_delete}")
            else:
                st.warning("Please enter a Cottage ID to delete.")
    else:
        st.warning("No cottages found.")
