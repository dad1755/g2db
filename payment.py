import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def execute_query(query, params=None):
    """Execute a query with optional parameters and return the cursor."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(query, params if params else ())
        connection.commit()
        return cursor  # Return cursor for further processing if needed
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_data(query, params=None):
    """Fetch data from the database and return it as a list of dictionaries."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params if params else ())
        rows = cursor.fetchall()
        return rows
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# PAYMENT TYPES CRUD FUNCTIONS
def create_payment_type(pt_details):
    """Add a new payment type."""
    query = "INSERT INTO PAYMENT_TYPES (pt_details) VALUES (%s)"
    execute_query(query, (pt_details,))

def get_payment_types():
    """Retrieve all payment types."""
    query = "SELECT * FROM PAYMENT_TYPES"
    return fetch_data(query)

def delete_payment_type(pt_id):
    """Delete a payment type by ID."""
    query = "DELETE FROM PAYMENT_TYPES WHERE pt_id = %s"
    execute_query(query, (pt_id,))

# PAYMENT STATUS CRUD FUNCTIONS
def create_payment_status(pay_details):
    """Add a new payment status."""
    query = "INSERT INTO PAYMENT_STATUS (pay_details) VALUES (%s)"
    execute_query(query, (pay_details,))

def get_payment_statuses():
    """Retrieve all payment statuses."""
    query = "SELECT * FROM PAYMENT_STATUS"
    data = fetch_data(query)
    return data if data else []

def delete_payment_status(pay_id):
    """Delete a payment status by ID."""
    query = "DELETE FROM PAYMENT_STATUS WHERE pay_id = %s"
    execute_query(query, (pay_id,))

# Streamlit UI for Payment Management
def show_payment_management():
    st.subheader("Payment Management")

    # Payment Types Management
    st.write("### Payment Types")
    pt_details_input = st.text_input("Payment Type Details", key="pt_details_input")  # Ensure this key is unique
    if st.button("Add Payment Type", key="add_payment_type_button"):  # Ensure this key is unique
        if pt_details_input:
            create_payment_type(pt_details_input)
            st.success(f"Added Payment Type: {pt_details_input}")
        else:
            st.warning("Please enter Payment Type Details.")

    st.write("### Available Payment Types")
    payment_types_data = get_payment_types()
    if payment_types_data:
        st.dataframe(payment_types_data)
        pt_id_to_delete_input = st.text_input("Enter Payment Type ID to delete", key="pt_id_to_delete_input")  # Ensure this key is unique
        if st.button("Delete Payment Type", key="delete_payment_type_button"):  # Ensure this key is unique
            if pt_id_to_delete_input.isdigit():
                delete_payment_type(int(pt_id_to_delete_input))
                st.success(f"Deleted Payment Type with ID: {pt_id_to_delete_input}")
            else:
                st.warning("Please enter a valid numeric Payment Type ID to delete.")
    else:
        st.warning("No payment types found.")

    # Payment Status Management
    st.write("### Payment Status")
    pay_details_input = st.text_input("Payment Status Details", key="pay_details_input_status")  # Unique key for Payment Status Details
    if st.button("Add Payment Status", key="add_payment_status_button"):  # Unique key for Add Payment Status button
        if pay_details_input:
            create_payment_status(pay_details_input)
            st.success(f"Added Payment Status: {pay_details_input}")
        else:
            st.warning("Please enter Payment Status Details.")

    st.write("### Available Payment Statuses")
    payment_status_data = get_payment_statuses()
    if payment_status_data:
        st.dataframe(payment_status_data)
        pay_id_to_delete_input = st.text_input("Enter Payment Status ID to delete", key="pay_id_to_delete_input_status")  # Unique key for delete input
        if st.button("Delete Payment Status", key="delete_payment_status_button"):  # Unique key for Delete button
            if pay_id_to_delete_input.isdigit():
                delete_payment_status(int(pay_id_to_delete_input))
                st.success(f"Deleted Payment Status with ID: {pay_id_to_delete_input}")
            else:
                st.warning("Please enter a valid numeric Payment Status ID to delete.")
    else:
        st.warning("No payment statuses found.")

# Run the payment management function to show the UI
show_payment_management()
