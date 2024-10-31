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

# PAYMENT TYPES TABLE CRUD FUNCTIONS
def create_payment_type(pt_id, pt_details):
    query = "INSERT INTO PAYMENT_TYPES (pt_id, pt_details) VALUES (%s, %s)"
    execute_query(query, (pt_id, pt_details))

def get_payment_types():
    query = "SELECT * FROM PAYMENT_TYPES"
    return fetch_data(query)

def delete_payment_type(pt_id):
    query = "DELETE FROM PAYMENT_TYPES WHERE pt_id = %s"
    execute_query(query, (pt_id,))

# PAYMENT STATUS TABLE CRUD FUNCTIONS
def create_payment_status(pay_id, pay_details, staff_id):
    query = "INSERT INTO PAYMENT_STATUS (pay_id, pay_details, staff_id) VALUES (%s, %s, %s)"
    execute_query(query, (pay_id, pay_details, staff_id))

def get_payment_types():
    query = "SELECT * FROM PAYMENT_TYPES"
    data = fetch_data(query)
    if data is None:
        return []  # Return an empty list
    return data

def get_payment_statuses():
    query = "SELECT * FROM PAYMENT_STATUS"
    data = fetch_data(query)
    if data is None:
        return []  # Return an empty list
    return data


def delete_payment_status(pay_id):
    query = "DELETE FROM PAYMENT_STATUS WHERE pay_id = %s"
    execute_query(query, (pay_id,))

# Streamlit UI for Payment Management
def show_payment_management():
    st.subheader("Payment Management")

    # Payment Types Management
    st.write("### Payment Types")
    pt_id = st.text_input("Payment Type ID")
    pt_details = st.text_input("Payment Type Details")
    if st.button("Add Payment Type"):
        if pt_id and pt_details:
            create_payment_type(pt_id, pt_details)
            st.success(f"Added Payment Type: {pt_details}")
        else:
            st.warning("Please enter both Payment Type ID and Details.")

    st.write("### Available Payment Types")
    payment_types_data = get_payment_types()
    if payment_types_data:
        st.dataframe(payment_types_data)
        pt_id_to_delete = st.text_input("Enter Payment Type ID to delete")
        if st.button("Delete Payment Type"):
            if pt_id_to_delete:
                delete_payment_type(pt_id_to_delete)
                st.success(f"Deleted Payment Type with ID: {pt_id_to_delete}")
            else:
                st.warning("Please enter a Payment Type ID to delete.")
    else:
        st.warning("No payment types found.")

    # Payment Status Management
    st.write("### Payment Status")
    pay_id = st.text_input("Payment Status ID")
    pay_details = st.text_input("Payment Status Details")
    staff_id = st.text_input("Staff ID (optional)")
    if st.button("Add Payment Status"):
        if pay_id and pay_details:
            create_payment_status(pay_id, pay_details, staff_id)
            st.success(f"Added Payment Status: {pay_details}")
        else:
            st.warning("Please enter Payment Status ID and Details.")

    st.write("### Available Payment Statuses")
    payment_status_data = get_payment_statuses()
    if payment_status_data:
        st.dataframe(payment_status_data)
        pay_id_to_delete = st.text_input("Enter Payment Status ID to delete")
        if st.button("Delete Payment Status"):
            if pay_id_to_delete:
                delete_payment_status(pay_id_to_delete)
                st.success(f"Deleted Payment Status with ID: {pay_id_to_delete}")
            else:
                st.warning("Please enter a Payment Status ID to delete.")
    else:
        st.warning("No payment statuses found.")

