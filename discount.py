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

# DISCOUNT TABLE CRUD FUNCTIONS
def create_discount(dis_id, cot_id, dis_amount, staff_id):
    query = "INSERT INTO DISCOUNT (dis_id, cot_id, dis_amount, staff_id) VALUES (%s, %s, %s, %s)"
    execute_query(query, (dis_id, cot_id, dis_amount, staff_id))

def get_discounts():
    query = """
    SELECT d.dis_id, d.dis_amount, c.cot_name, s.staff_name 
    FROM DISCOUNT d 
    JOIN COTTAGE c ON d.cot_id = c.cot_id 
    JOIN STAFF s ON d.staff_id = s.staff_id
    """
    return fetch_data(query)

def delete_discount(dis_id):
    query = "DELETE FROM DISCOUNT WHERE dis_id = %s"
    execute_query(query, (dis_id,))

# Streamlit UI for Discount Management
def show_discount_management():
    st.subheader("Discount Management")

    # Add Discount
    st.write("### Add Discount")
    dis_id = st.text_input("Discount ID")
    cot_id = st.text_input("Cottage ID")
    dis_amount = st.number_input("Discount Amount", format="%.2f", step=0.01)
    staff_id = st.text_input("Staff ID (optional)")
    if st.button("Add Discount"):
        if dis_id and cot_id and dis_amount is not None:
            create_discount(dis_id, cot_id, dis_amount, staff_id)
            st.success(f"Added Discount: {dis_amount} for Cottage ID: {cot_id}")
        else:
            st.warning("Please enter all required fields.")

    # View Discounts
    st.write("### Available Discounts")
    discount_data = get_discounts()
    if discount_data:
        st.dataframe(discount_data)
        dis_id_to_delete = st.text_input("Enter Discount ID to delete")
        if st.button("Delete Discount"):
            if dis_id_to_delete:
                delete_discount(dis_id_to_delete)
                st.success(f"Deleted Discount with ID: {dis_id_to_delete}")
            else:
                st.warning("Please enter a Discount ID to delete.")
    else:
        st.warning("No discounts found.")
