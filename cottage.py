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

def fetch_data(query, params=None):
    """Fetch data from the database with optional parameters."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params) if params else cursor.execute(query)
        rows = cursor.fetchall()
        return rows  # Return fetched rows
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Cottage Management Functions
def create_cottage(cot_name):
    """Create a new cottage."""
    query = "INSERT INTO COTTAGE (cot_name) VALUES (%s)"
    execute_query(query, (cot_name,))  # Only pass cot_name

def create_cottage_with_attributes(cottage_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat):
    """Link attributes to an existing cottage."""
    query = """
        INSERT INTO COTTAGE_ATTRIBUTES_RELATION 
        (cot_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (cottage_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat))

def get_last_insert_id():
    """Fetch the last inserted ID."""
    query = "SELECT LAST_INSERT_ID()"
    result = fetch_data(query)
    return result[0]['LAST_INSERT_ID()'] if result else None

def get_cottages():
    """Fetch all cottages."""
    query = "SELECT * FROM COTTAGE"
    data = fetch_data(query)
    if data is None:
        return []  # Return an empty list
    return data

def get_cottage_attributes_relation():
    """Fetch all cottage attributes relation."""
    query = "SELECT * FROM COTTAGE_ATTRIBUTES_RELATION"
    data = fetch_data(query)
    return data if data is not None else []

def delete_cottage_and_attributes(cot_id):
    """Delete a cottage and its attributes."""
    # First delete from COTTAGE_ATTRIBUTES_RELATION
    delete_attributes_query = "DELETE FROM COTTAGE_ATTRIBUTES_RELATION WHERE cot_id = %s"
    execute_query(delete_attributes_query, (cot_id,))

    # Then delete from COTTAGE
    delete_cottage_query = "DELETE FROM COTTAGE WHERE cot_id = %s"
    execute_query(delete_cottage_query, (cot_id,))

def show_cottage_management():
    """Streamlit UI for Cottage Management."""
    st.subheader("Cottage Management")

    # View Cottages
    st.write("### Cottage List")
    cottage_data = get_cottages()
    if cottage_data:
        # Display cottage list in a grid format
        cottage_df = pd.DataFrame(cottage_data)
        st.dataframe(cottage_df)  # Displaying the cottage list in a grid
    else:
        st.warning("No cottages found.")

    # Add Cottage
    st.write("### Add Cottage")
    cot_name = st.text_input("Cottage Name")

    if st.button("Create Cottage"):
        if cot_name:
            create_cottage(cot_name)  # Create the cottage
            cottage_id = get_last_insert_id()  # Get the last inserted cottage ID
            st.success(f"Added Cottage: {cot_name} (ID: {cottage_id})")
        else:
            st.warning("Please enter a Cottage Name.")

    # Add Attributes for Existing Cottage
    st.write("### Add Attributes to Cottage")
    cottage_data = get_cottages()  # Fetch existing cottages
    if cottage_data:
        selected_cottage_name = st.selectbox("Select a Cottage to Add Attributes", 
                                               options=[cottage['cot_name'] for cottage in cottage_data])
        
        # Get the cottage ID for the selected name
        selected_cottage_id = next((cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == selected_cottage_name), None)
        
        # Fetch options for cottage attributes
        pool_options = get_pools()
        loc_options = get_locations()
        room_options = get_rooms()
        max_pax_options = get_maximum_pax()
        ct_options = get_cottage_types()
        ct_stat_options = get_cottage_statuses()

        # Selection boxes for cottage attributes
        pool_selection = st.selectbox("Select Pool", 
                                       options=[f"{pool['pool_id']}: {pool['pool_detail']}" for pool in pool_options])
        loc_selection = st.selectbox("Select Location", 
                                       options=[f"{loc['loc_id']}: {loc['loc_details']}" for loc in loc_options])
        room_selection = st.selectbox("Select Room", 
                                       options=[f"{room['room_id']}: {room['room_details']}" for room in room_options])
        max_pax_selection = st.selectbox("Select Maximum Pax", 
                                           options=[f"{max_pax['max_pax_id']}: {max_pax['max_pax_details']}" for max_pax in max_pax_options])
        ct_selection = st.selectbox("Select Cottage Type", 
                                     options=[f"{ct['ct_id']}: {ct['ct_details']}" for ct in ct_options])
        ct_stat_selection = st.selectbox("Select Cottage Status", 
                                          options=[f"{cs['cottage_status_id']}: {cs['ct_details']}" for cs in ct_stat_options])

        # Extract selected IDs from the selections
        pool_id = int(pool_selection.split(":")[0])
        loc_id = int(loc_selection.split(":")[0])
        room_id = int(room_selection.split(":")[0])
        max_pax_id = int(max_pax_selection.split(":")[0])
        ct_id = int(ct_selection.split(":")[0])
        ct_id_stat = int(ct_stat_selection.split(":")[0])

        if st.button("Add Attributes"):
            if selected_cottage_id:
                create_cottage_with_attributes(selected_cottage_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat)
                st.success(f"Added Attributes to Cottage: {selected_cottage_name}")
                
                # Show the COTTAGE_ATTRIBUTES_RELATION table after adding attributes
                st.write("### Cottage Attributes Relation")
                cottage_attributes_data = get_cottage_attributes_relation()
                if cottage_attributes_data:
                    cottage_attributes_df = pd.DataFrame(cottage_attributes_data)
                    st.dataframe(cottage_attributes_df)  # Displaying the cottage attributes in a grid
                else:
                    st.warning("No cottage attributes found.")
            else:
                st.warning("Please select a Cottage to add attributes.")

    # Delete Cottage
    st.write("### Delete Cottage")
    cottage_data = get_cottages()  # Fetch existing cottages again
    if cottage_data:
        cottage_to_delete = st.selectbox("Select a Cottage to Delete", 
                                           options=[cottage['cot_name'] for cottage in cottage_data])
        
        if st.button("Delete Cottage"):
            cottage_id_to_delete = next((cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == cottage_to_delete), None)
            if cottage_id_to_delete:
                delete_cottage_and_attributes(cottage_id_to_delete)
                st.success(f"Deleted Cottage: {cottage_to_delete}")
            else:
                st.warning("Cottage not found.")
    else:
        st.warning("No cottages available to delete.")

# Call the show_cottage_management function to display the UI
if __name__ == "__main__":
    show_cottage_management()
