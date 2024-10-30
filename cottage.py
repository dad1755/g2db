import streamlit as st
from utils.db_utils import execute_query, fetch_data

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
    if isinstance(result, Error):
        st.error(f"Error while adding cottage: {result}")
    else:
        st.success(f"Added cottage: {cottage_name} with capacity {capacity}")

def delete_cottage(cottage_id):
    query = "DELETE FROM COTTAGE WHERE cottage_id = %s"
    result = execute_query(query, (cottage_id,))
    if isinstance(result, Error):
        st.error(f"Error while deleting cottage: {result}")
    elif result.rowcount > 0:
        st.success(f"Deleted cottage with ID: {cottage_id}")
    else:
        st.warning(f"No cottage found with ID: {cottage_id}")

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
    st.write("### Available Cottages")
    cottages_data = get_cottages()
    if not cottages_data.empty:
        st.dataframe(cottages_data)

        # Delete Cottage
        st.write("### Delete Cottage")
        cottage_id_to_delete = st.number_input("Enter Cottage ID to delete", min_value=1)
        if st.button("Delete Cottage"):
            if cottage_id_to_delete:
                delete_cottage(cottage_id_to_delete)
            else:
                st.warning("Please enter a Cottage ID to delete.")
    else:
        st.warning("No cottages found.")
