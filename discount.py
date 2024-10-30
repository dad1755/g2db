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

# Fetch cottage names
def get_cottages():
    """Fetch all cottages and return their names and IDs."""
    query = "SELECT cot_id, cot_name FROM COTTAGE"
    return fetch_data(query)

# Fetch staff names
def get_staff():
    """Fetch all staff members and return their names and IDs."""
    query = "SELECT staff_id, staff_name FROM STAFF"
    return fetch_data(query)

# Create discount function
def create_discount(cot_id, dis_amount, staff_id):
    """Create a new discount without a visible discount ID."""
    # Generate a new discount ID (e.g., D001, D002, etc.)
    query = "SELECT COUNT(*) AS count FROM DISCOUNT"
    count = fetch_data(query)[0]['count']
    dis_id = f"D{count + 1:03}"  # e.g., D001, D002, etc.

    insert_query = "INSERT INTO DISCOUNT (dis_id, cot_id, dis_amount, staff_id) VALUES (%s, %s, %s, %s)"
    execute_query(insert_query, (dis_id, cot_id, dis_amount, staff_id))

def get_discounts():
    """Fetch all discounts with cottage and staff names."""
    query = """
    SELECT d.dis_id, c.cot_name, d.dis_amount, s.staff_name 
    FROM DISCOUNT d
    JOIN COTTAGE c ON d.cot_id = c.cot_id
    JOIN STAFF s ON d.staff_id = s.staff_id
    """
    return fetch_data(query)

def delete_discount(dis_id):
    """Delete a discount by ID."""
    query = "DELETE FROM DISCOUNT WHERE dis_id = %s"
    execute_query(query, (dis_id,))

def show_discount_management():
    """Streamlit UI for Discount Management."""
    st.subheader("Discount Management")

    # Add Discount
    st.write("### Add Discount")
    
    # Fetch and display cottages in a dropdown
    cottages = get_cottages()
    cottage_options = {cot['cot_name']: cot['cot_id'] for cot in cottages}
    selected_cottage_name = st.selectbox("Select Cottage", list(cottage_options.keys()))
    selected_cottage_id = cottage_options[selected_cottage_name]

    # Fetch and display staff in a dropdown
    staff = get_staff()
    staff_options = {s['staff_name']: s['staff_id'] for s in staff}
    selected_staff_name = st.selectbox("Select Staff", list(staff_options.keys()))
    selected_staff_id = staff_options[selected_staff_name]

    dis_amount = st.number_input("Discount Amount", min_value=0.0, format="%.2f")
    
    if st.button("Add Discount"):
        if dis_amount:
            create_discount(selected_cottage_id, dis_amount, selected_staff_id)
            st.success(f"Added Discount for Cottage: {selected_cottage_name} with amount: {dis_amount}")
        else:
            st.warning("Please enter a Discount Amount.")

    # View Discounts
    st.write("### Discount List")
    discount_data = get_discounts()
    if discount_data:
        st.dataframe(discount_data)

        # Delete Discount
        st.write("### Delete Discount")
        dis_id_to_delete = st.text_input("Enter Discount ID to delete")
        if st.button("Delete Discount"):
            if dis_id_to_delete:
                delete_discount(dis_id_to_delete)
                st.success(f"Deleted Discount with ID: {dis_id_to_delete}")
            else:
                st.warning("Please enter a Discount ID to delete.")
    else:
        st.warning("No discounts found.")

# Call the show_discount_management function to display the UI
if __name__ == "__main__":
    show_discount_management()
