import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database configuration (update as necessary)
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def execute_query(query, params=None):
    """Execute a query with optional parameters."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        st.success("Query executed successfully.")
        return cursor
    except Error as e:
        st.error(f"Error executing query: {query} with params: {params} | Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def fetch_data(query):
    """Fetch data from the database."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# CRUD Functions for Cottages
def get_cottages():
    """Fetch all cottages."""
    query = "SELECT * FROM COTTAGE"
    return fetch_data(query) or []

def create_cottage(cot_name, cot_price):
    """Add a new cottage."""
    query = "INSERT INTO COTTAGE (cot_name, cot_price) VALUES (%s, %s)"
    execute_query(query, (cot_name, cot_price))

def update_cottage(cot_id, cot_name, cot_price):
    """Update an existing cottage."""
    query = "UPDATE COTTAGE SET cot_name = %s, cot_price = %s WHERE cot_id = %s"
    execute_query(query, (cot_name, cot_price, cot_id))

def delete_cottage(cot_id):
    """Delete a cottage by ID."""
    query = "DELETE FROM COTTAGE WHERE cot_id = %s"
    execute_query(query, (cot_id,))

def show_cottage_management():
    """Streamlit UI for managing Cottages."""
    st.write("### Cottage Management 💡")

    # List all cottages
    st.write("#### Cottage List Available in Database")
    cottages = get_cottages()
    if cottages:
        st.dataframe(cottages)

    # Add a new cottage
    st.write("#### Function to Add New Cottage")
    new_cot_name = st.text_input("Cottage Name")
    new_cot_price = st.number_input("Cottage Price", min_value=0.0)
    if st.button("Add Cottage"):
        if new_cot_name and new_cot_price:
            create_cottage(new_cot_name, new_cot_price)
            st.success(f"Added Cottage: {new_cot_name} with price: {new_cot_price}")
        else:
            st.warning("Please fill in all fields.")

    # Edit an existing cottage
    st.write("#### Function to Edit Cottage")
    cottage_names = [f"{cottage['cot_name']} (ID: {cottage['cot_id']})" for cottage in cottages]
    selected_cottage = st.selectbox("Select Cottage to Edit", options=cottage_names)
    if selected_cottage:
        selected_cot_id = int(selected_cottage.split("(ID: ")[-1][:-1])  # Extract cottage ID
        selected_cot_data = next((cot for cot in cottages if cot['cot_id'] == selected_cot_id), None)

        if selected_cot_data:
            updated_cot_name = st.text_input("Updated Cottage Name", value=selected_cot_data['cot_name'])
            updated_cot_price = st.number_input("Updated Cottage Price", value=selected_cot_data['cot_price'], min_value=0.0)
            if st.button("Update Cottage"):
                update_cottage(selected_cot_id, updated_cot_name, updated_cot_price)
                st.success(f"Updated Cottage ID: {selected_cot_id} to name: {updated_cot_name}, price: {updated_cot_price}")

    # Delete an existing cottage
    st.write("#### Function to Delete Cottage")
    selected_cottage_to_delete = st.selectbox("Select Cottage to Delete", options=cottage_names)
    if selected_cottage_to_delete:
        selected_cot_id_to_delete = int(selected_cottage_to_delete.split("(ID: ")[-1][:-1])
        if st.button("Delete Selected Cottage"):
            delete_cottage(selected_cot_id_to_delete)
            st.success(f"Deleted Cottage ID: {selected_cot_id_to_delete}")

# Main application
def main():
    """Main application entry point."""
    st.title("Cottage Management System 🏠")
    show_cottage_management()

if __name__ == "__main__":
    main()
