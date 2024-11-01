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

def create_cottage_with_attributes(cottage_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat):
    """Link attributes to an existing cottage."""
    query = """
        INSERT INTO COTTAGE_ATTRIBUTES_RELATION 
        (cot_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (cottage_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat))

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

# Additional functions for fetching data omitted for brevity...

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

    # Cottage Attributes
    st.write("###### Cottage Attributes@Facilities, Please Refer To Next Tab For Details")
    cottage_attributes_data = get_cottage_attributes_relation()
    if cottage_attributes_data:
        attributes_df = pd.DataFrame(cottage_attributes_data)
        st.dataframe(attributes_df)
    else:
        st.warning("No cottage attributes found. ----> VIEW GRID HERE")
    
    # Add Cottage Attributes
    st.write("### Add Attributes for Cottage")
    if cottage_data:
        selected_cottage_name = st.selectbox("Select a Cottage to Add Attributes", 
                                             options=[cottage['cot_name'] for cottage in cottage_data], key="cottage_select")
        selected_cottage_id = next((cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == selected_cottage_name), None)
    
        # Fetch options for attributes
        pool_options = get_pools()
        loc_options = get_locations()
        room_options = get_rooms()
        max_pax_options = get_maximum_pax()
        ct_options = get_cottage_types()
        ct_stat_options = get_cottage_statuses()
    
        # Select attribute options
        pool_selection = st.selectbox("Select Pool", options=[f"{pool['pool_id']}: {pool['pool_detail']}" for pool in pool_options])
        loc_selection = st.selectbox("Select Location", options=[f"{loc['loc_id']}: {loc['loc_details']}" for loc in loc_options])
        room_selection = st.selectbox("Select Room", options=[f"{room['room_id']}: {room['room_details']}" for room in room_options])
        max_pax_selection = st.selectbox("Select Maximum Pax", options=[f"{max_pax['max_pax_id']}: {max_pax['max_pax_details']}" for max_pax in max_pax_options])
        ct_selection = st.selectbox("Select Cottage Type", options=[f"{ct['ct_id']}: {ct['ct_details']}" for ct in ct_options])
        ct_stat_selection = st.selectbox("Select Cottage Status", options=[f"{ct_stat['cottage_status_id']}: {ct_stat['ct_details']}" for ct_stat in ct_stat_options])
    
        if st.button("Add Attributes"):
            new_pool_id = pool_selection.split(":")[0]
            new_loc_id = loc_selection.split(":")[0]
            new_room_id = room_selection.split(":")[0]
            new_max_pax_id = max_pax_selection.split(":")[0]
            new_ct_id = ct_selection.split(":")[0]
            new_ct_stat_id = ct_stat_selection.split(":")[0]
            
            create_cottage_with_attributes(selected_cottage_id, new_pool_id, new_loc_id, new_room_id, new_max_pax_id, new_ct_id, new_ct_stat_id)
            st.success(f"Added attributes for Cottage ID: {selected_cottage_id}")


# Run the application
if __name__ == "__main__":
    show_cottage_management()
