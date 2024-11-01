import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Database configuration
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
        return cursor.rowcount
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

def get_cottages():
    """Fetch all cottages."""
    query = "SELECT * FROM COTTAGE"
    data = fetch_data(query)
    return data if data is not None else []

def get_cottage_attributes_relation():
    """Fetch all cottage attributes relations."""
    query = "SELECT * FROM COTTAGE_ATTRIBUTES_RELATION"
    data = fetch_data(query)
    return data if data is not None else []

def delete_cottage(cot_id):
    """Delete a cottage and its related data."""
    delete_discounts_query = "DELETE FROM DISCOUNT WHERE cot_id = %s"
    execute_query(delete_discounts_query, (cot_id,))

    delete_attributes_query = "DELETE FROM COTTAGE_ATTRIBUTES_RELATION WHERE cot_id = %s"
    execute_query(delete_attributes_query, (cot_id,))

    delete_cottage_query = "DELETE FROM COTTAGE WHERE cot_id = %s"
    execute_query(delete_cottage_query, (cot_id,))

    st.success(f"Cottage with ID {cot_id} and its related data have been deleted.")
    st.rerun()

def update_cottage_attributes(cot_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat):
    """Update the attributes of a cottage."""
    update_query = """
        UPDATE COTTAGE_ATTRIBUTES_RELATION
        SET pool_id = %s, loc_id = %s, room_id = %s, max_pax_id = %s, ct_id = %s, ct_id_stat = %s
        WHERE cot_id = %s
    """
    params = (pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat, cot_id)
    execute_query(update_query, params)

def create_cottage(cot_name, cot_price):
    """Create a new cottage."""
    create_query = "INSERT INTO COTTAGE (cot_name, cot_price) VALUES (%s, %s)"
    execute_query(create_query, (cot_name, cot_price))

def show_cottage_management():
    """Streamlit UI for Cottage Management."""
    st.write("#### Cottage Management 💡")

    # View Cottages
    st.write("###### Cottage List Available in Database")
    cottage_data = get_cottages()
    if cottage_data:
        cottage_df = pd.DataFrame(cottage_data)
        st.dataframe(cottage_df)
    else:
        st.warning("No cottages found.")

    # Add Cottage
    cot_name = st.text_input("Cottage Name")
    cot_price = st.number_input("Cottage Price", min_value=0.0, step=0.01)
    if st.button("Create Cottage"):
        if cot_name and cot_price:
            create_cottage(cot_name, cot_price)
            st.success(f"Added Cottage: {cot_name}")
            st.rerun()
        else:
            st.warning("Please enter both Cottage Name and Price.")

    # Delete Cottage
    if cottage_data:
        selected_cottage_name = st.selectbox("Select Cottage to Delete", options=[cottage['cot_name'] for cottage in cottage_data])
        selected_cottage_id = next((cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == selected_cottage_name), None)

        if st.button("Delete Cottage"):
            delete_cottage(selected_cottage_id)
            st.rerun()
    # View Cottage Attributes
    st.write("#### Cottage Attributes Management 📦")
    cottage_attributes_data = get_cottage_attributes_relation()
    if cottage_attributes_data:
        attributes_df = pd.DataFrame(cottage_attributes_data)
        st.dataframe(attributes_df)
    else:
        st.warning("No cottage attributes found. Displaying an empty grid.")
        empty_df = pd.DataFrame(columns=["cot_id", "pool_id", "loc_id", "room_id", "max_pax_id", "ct_id", "ct_id_stat"])
        st.dataframe(empty_df)
    # Update Cottage Attributes
    st.write("#### Update Cottage Attributes ✏️")
    if cottage_data:
        selected_cottage_name = st.selectbox("Select Cottage to Update Attributes", options=[cottage['cot_name'] for cottage in cottage_data])
        selected_cottage_id = next((cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == selected_cottage_name), None)

        # Fetch current attributes to allow editing
        current_attributes_query = "SELECT * FROM COTTAGE_ATTRIBUTES_RELATION WHERE cot_id = %s"
        current_attributes = fetch_data(current_attributes_query, (selected_cottage_id,))
        
        if current_attributes:
            current_attributes = current_attributes[0]  # Assuming one row is returned
            
            # Create input fields for attributes
            pool_id = st.number_input("Pool ID", value=current_attributes['pool_id'], min_value=0)
            loc_id = st.number_input("Location ID", value=current_attributes['loc_id'], min_value=0)
            room_id = st.number_input("Room ID", value=current_attributes['room_id'], min_value=0)
            max_pax_id = st.number_input("Max Pax ID", value=current_attributes['max_pax_id'], min_value=0)
            ct_id = st.number_input("Cottage Type ID", value=current_attributes['ct_id'], min_value=0)
            ct_id_stat = st.number_input("Cottage Status ID", value=current_attributes['ct_id_stat'], min_value=0)

            if st.button("Update Attributes"):
                update_cottage_attributes(selected_cottage_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat)
                st.success("Cottage attributes updated successfully.")
                st.rerun()  # Optionally rerun to refresh the UI after the update
        else:
            st.warning("No attributes found for the selected cottage.")



# Run the application
if __name__ == "__main__":
    show_cottage_management()
