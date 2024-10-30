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

def create_cottage_table():
    query = """
    CREATE TABLE IF NOT EXISTS COTTAGE (
        cottage_id INT AUTO_INCREMENT PRIMARY KEY,
        cottage_name VARCHAR(100) NOT NULL,
        capacity INT NOT NULL
    )
    """
    execute_query(query)

def add_cottage(cottage_name, capacity):
    query = "INSERT INTO COTTAGE (cottage_name, capacity) VALUES (%s, %s)"
    result = execute_query(query, (cottage_name, capacity))
    if result is None:
        st.error("Error while adding cottage.")
    else:
        st.success(f"Added cottage: {cottage_name} with capacity {capacity}")

def delete_cottage(cottage_id):
    query = "DELETE FROM COTTAGE WHERE cottage_id = %s"
    result = execute_query(query, (cottage_id,))
    if result is None:
        st.error("Error while deleting cottage.")
    elif result.rowcount > 0:
        st.success(f"Deleted cottage record with ID: {cottage_id}")
    else:
        st.warning(f"No cottage record found with ID: {cottage_id}")

def get_cottages():
    query = "SELECT * FROM COTTAGE"
    return fetch_data(query)

def show_cottage_management():
    st.subheader("Cottage Management")
    create_cottage_table()

    # Add Cottage
    st.write("### Add Cottage")
    cottage_name = st.text_input("Cottage Name")
    capacity = st.number_input("Capacity", min_value=1)
    if st.button("Add Cottage"):
        if cottage_name and capacity:
            add_cottage(cottage_name, capacity)
        else:
            st.warning("Please provide both name and capacity.")

    # View Cottages
    st.write("### Cottage Records")
    cottages_data = get_cottages()
    if cottages_data is not None and not cottages_data.empty:
        st.dataframe(cottages_data)

        # Delete Cottage
        st.write("### Delete Cottage Record")
        cottage_id_to_delete = st.number_input("Enter Cottage ID to delete", min_value=1)
        if st.button("Delete Cottage"):
            if cottage_id_to_delete:
                delete_cottage(cottage_id_to_delete)
            else:
                st.warning("Please enter a Cottage ID to delete.")
    else:
        st.warning("No cottage records found.")
