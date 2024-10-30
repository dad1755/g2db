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

def create_discount_table():
    query = """
    CREATE TABLE IF NOT EXISTS DISCOUNT (
        discount_id INT AUTO_INCREMENT PRIMARY KEY,
        discount_rate DECIMAL(5, 2) NOT NULL,
        description VARCHAR(255)
    )
    """
    execute_query(query)

def add_discount(discount_rate, description):
    query = "INSERT INTO DISCOUNT (discount_rate, description) VALUES (%s, %s)"
    result = execute_query(query, (discount_rate, description))
    if result is None:
        st.error("Error while adding discount.")
    else:
        st.success(f"Added discount: {discount_rate}% - {description}")

def delete_discount(discount_id):
    query = "DELETE FROM DISCOUNT WHERE discount_id = %s"
    result = execute_query(query, (discount_id,))
    if result is None:
        st.error("Error while deleting discount.")
    elif result.rowcount > 0:
        st.success(f"Deleted discount record with ID: {discount_id}")
    else:
        st.warning(f"No discount record found with ID: {discount_id}")

def get_discounts():
    query = "SELECT * FROM DISCOUNT"
    return fetch_data(query)

def show_discount_management():
    st.subheader("Discount Management")
    create_discount_table()

    # Add Discount
    st.write("### Add Discount")
    discount_rate = st.number_input("Discount Rate (%)", min_value=0.0, max_value=100.0)
    description = st.text_input("Description")
    if st.button("Add Discount"):
        if discount_rate and description:
            add_discount(discount_rate, description)
        else:
            st.warning("Please provide both rate and description.")

    # View Discounts
    st.write("### Discount Records")
    discounts_data = get_discounts()
    if discounts_data is not None and not discounts_data.empty:
        st.dataframe(discounts_data)

        # Delete Discount
        st.write("### Delete Discount Record")
        discount_id_to_delete = st.number_input("Enter Discount ID to delete", min_value=1)
        if st.button("Delete Discount"):
            if discount_id_to_delete:
                delete_discount(discount_id_to_delete)
            else:
                st.warning("Please enter a Discount ID to delete.")
    else:
        st.warning("No discount records found.")
