import streamlit as st
import mysql.connector
from mysql.connector import Error

# Hardcoded database configuration (make sure to secure your credentials)
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
            cursor.execute(query, params)  # Using parameterized queries is good for safety
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

# Discount Management Functions
def create_discount(discount_name, discount_percentage):
    """Create a new discount."""
    query = "INSERT INTO DISCOUNT (discount_name, discount_percentage) VALUES (%s, %s)"
    execute_query(query, (discount_name, discount_percentage))

def get_discounts():
    """Fetch all discount."""
    query = "SELECT * FROM DISCOUNT"
    data = fetch_data(query)
    if data is None:
        return []  # Return an empty list instead of None to avoid errors in UI
    return data


def delete_discount(discount_id):
    """Delete a discount by ID."""
    query = "DELETE FROM DISCOUNT WHERE discount_id = %s"
    execute_query(query, (discount_id,))

def show_discount_management():
    """Streamlit UI for Discount Management."""
    st.subheader("Discount Management")

    # Add Discount
    st.write("### Add Discount")
    discount_name = st.text_input("Discount Name")
    discount_percentage = st.number_input("Discount Percentage", min_value=0.0, max_value=100.0, step=0.1)
    if st.button("Add Discount"):
        if discount_name:
            create_discount(discount_name, discount_percentage)
            st.success(f"Added Discount: {discount_name} with {discount_percentage}%")
        else:
            st.warning("Please enter a Discount Name.")

    # View Discounts
    st.write("### Discount List")
    discount_data = get_discounts()
    if discount_data:
        st.dataframe(discount_data)
        # Prepare to delete a discount
        st.write("### Delete Discount")
        discount_names = [discount['discount_name'] for discount in discount_data]
        discount_name_to_delete = st.selectbox("Select Discount to Delete", options=discount_names)

        if st.button("Delete Discount"):
            if discount_name_to_delete:
                discount_id_to_delete = next(discount['discount_id'] for discount in discount_data if discount['discount_name'] == discount_name_to_delete)
                delete_discount(discount_id_to_delete)
                st.success(f"Deleted Discount: {discount_name_to_delete}")
            else:
                st.warning("Please select a Discount to delete.")
    else:
        st.warning("No discounts found.")


# Call the show_discount_management function to display the UI
if __name__ == "__main__":
    show_discount_management()
