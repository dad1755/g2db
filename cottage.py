import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

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
        return cursor.rowcount  # Return number of affected rows
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_data(query, params=None):
    """Fetch data from the database with optional parameters."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params) if params else cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_cottage(cot_name, cot_price):
    """Create a new cottage with a name and price."""
    query = "INSERT INTO COTTAGE (cot_name, cot_price) VALUES (%s, %s)"
    execute_query(query, (cot_name, cot_price))

def delete_cottage(cot_id):
    """Delete a cottage, its attributes, and associated discounts."""
    # Step 1: Get the cottage name for the given cottage ID
    get_cottage_name_query = "SELECT cot_name FROM COTTAGE WHERE cot_id = %s"
    cottage_name_result = fetch_data(get_cottage_name_query, (cot_id,))
    
    if not cottage_name_result:
        st.warning(f"Cottage with ID {cot_id} does not exist.")
        return

    cottage_name = cottage_name_result[0]['cot_name']  # Extract the cottage name

    # Step 2: Delete discounts related to this cottage
    delete_discounts_query = "DELETE FROM DISCOUNT WHERE cot_id = %s"
    discount_count = execute_query(delete_discounts_query, (cot_id,))
    
    if discount_count:
        st.success(f"Deleted {discount_count} discount(s) associated with cottage '{cottage_name}'.")
    else:
        st.info(f"No discounts found for cottage '{cottage_name}'.")

    # Step 3: Delete attributes related to the cottage
    delete_attributes_query = "DELETE FROM COTTAGE_ATTRIBUTES_RELATION WHERE cot_id = %s"
    execute_query(delete_attributes_query, (cot_id,))

    # Step 4: Delete the cottage itself
    delete_cottage_query = "DELETE FROM COTTAGE WHERE cot_id = %s"
    execute_query(delete_cottage_query, (cot_id,))
    
    st.success(f"Cottage '{cottage_name}' with ID {cot_id} and its related data have been deleted.")
    st.rerun()

def edit_cottage(cottage_id, new_name, new_price):
    """Edit an existing cottage's name and price."""
    query = "UPDATE COTTAGE SET cot_name = %s, cot_price = %s WHERE cot_id = %s"
    execute_query(query, (new_name, new_price, cottage_id))

def get_last_insert_id():
    """Fetch the last inserted ID."""
    query = "SELECT LAST_INSERT_ID()"
    result = fetch_data(query)
    if result and 'LAST_INSERT_ID()' in result[0]:
        return result[0]['LAST_INSERT_ID()']
    return None

def get_cottages():
    """Fetch all cottages."""
    query = "SELECT * FROM COTTAGE"
    data = fetch_data(query)
    return data if data is not None else []

def show_cottage_management():
    """Streamlit UI for Cottage Management."""
    st.write("### Cottage Management 💡")

    # View Cottages
    st.write("###### Cottage List Available in Database")
    cottage_data = get_cottages()
    if cottage_data:
        cottage_df = pd.DataFrame(cottage_data)
        st.dataframe(cottage_df)
    else:
        st.warning("No cottages found.")

    # Add Cottage
    st.write("###### Function To Add New Cottage")
    cot_name = st.text_input("Cottage Name")
    cot_price = st.number_input("Cottage Price", min_value=0.0, step=0.01)  # Input for price
    if st.button("Create Cottage"):
        if cot_name and cot_price:
            create_cottage(cot_name, cot_price)
            cottage_id = get_last_insert_id()
            st.success(f"Added Cottage: {cot_name} (ID: {cottage_id})")
            st.rerun()
        else:
            st.warning("Please enter both Cottage Name and Price.")

    # Edit Cottage
    if cottage_data:
        selected_cottage_name = st.selectbox("Select a Cottage to Edit", 
                                             options=[cottage['cot_name'] for cottage in cottage_data])
        selected_cottage_id = next((cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == selected_cottage_name), None)
        new_cot_name = st.text_input("New Cottage Name")
        new_cot_price = st.number_input("New Cottage Price", min_value=0.0, step=0.01)  # Input for new price
        
        if st.button("Update Cottage"):
            if new_cot_name and new_cot_price:
                edit_cottage(selected_cottage_id, new_cot_name, new_cot_price)  # Update to include price
                st.success(f"Updated Cottage to: {new_cot_name} with price: {new_cot_price}")
            else:
                st.warning("Please enter a new Cottage Name and Price.")

        if st.button("Delete Cottage"):
            delete_cottage(selected_cottage_id)
            st.success(f"Deleted Cottage: {selected_cottage_name}")
            st.rerun()

# Run the application
if __name__ == "__main__":
    show_cottage_management()
