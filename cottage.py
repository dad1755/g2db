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
        return cursor
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

# Cottage Management Functions
def delete_cottage(cot_id):
    """Delete a cottage and its attributes."""
    delete_attributes_query = "DELETE FROM COTTAGE_ATTRIBUTES_RELATION WHERE cot_id = %s"
    execute_query(delete_attributes_query, (cot_id,))
    delete_cottage_query = "DELETE FROM COTTAGE WHERE cot_id = %s"
    execute_query(delete_cottage_query, (cot_id,))


def edit_cottage(cottage_id, new_name):
    """Edit an existing cottage's name."""
    query = "UPDATE COTTAGE SET cot_name = %s WHERE cot_id = %s"
    execute_query(query, (new_name, cottage_id))

def delete_cottage(cot_id):
    """Delete a cottage and its attributes."""
    delete_attributes_query = "DELETE FROM COTTAGE_ATTRIBUTES_RELATION WHERE cot_id = %s"
    execute_query(delete_attributes_query, (cot_id,))
    delete_cottage_query = "DELETE FROM COTTAGE WHERE cot_id = %s"
    execute_query(delete_cottage_query, (cot_id,))

def edit_cottage_attributes(cot_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat):
    """Edit attributes of an existing cottage."""
    query = """
        UPDATE COTTAGE_ATTRIBUTES_RELATION
        SET pool_id = %s, loc_id = %s, room_id = %s, max_pax_id = %s, ct_id = %s, ct_id_stat = %s
        WHERE cot_id = %s
    """
    execute_query(query, (pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat, cot_id))

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
    return data if data is not None else []

def get_cottage_attributes_relation():
    """Fetch all cottage attributes relation."""
    query = "SELECT * FROM COTTAGE_ATTRIBUTES_RELATION"
    data = fetch_data(query)
    return data if data is not None else []

def get_pools():
    """Fetch all pools."""
    query = "SELECT * FROM POOL"
    data = fetch_data(query)
    return data if data is not None else []

def get_locations():
    """Fetch all locations."""
    query = "SELECT * FROM LOCATION"
    data = fetch_data(query)
    return data if data is not None else []

def get_rooms():
    """Fetch all rooms."""
    query = "SELECT * FROM ROOM"
    data = fetch_data(query)
    return data if data is not None else []

def get_maximum_pax():
    """Fetch all maximum pax options."""
    query = "SELECT * FROM MAXIMUM_PAX"
    data = fetch_data(query)
    return data if data is not None else []

def get_cottage_types():
    """Fetch all cottage types."""
    query = "SELECT * FROM COTTAGE_TYPES"
    data = fetch_data(query)
    return data if data is not None else []

def get_cottage_statuses():
    """Fetch all cottage statuses."""
    query = "SELECT * FROM COTTAGE_STATUS"
    data = fetch_data(query)
    return data if data is not None else []

def show_cottage_management():
    """Streamlit UI for Cottage Management."""
    st.title("Cottage Management")

    # View Cottages
    st.subheader("Cottage List")
    cottage_data = get_cottages()
    if cottage_data:
        cottage_df = pd.DataFrame(cottage_data)
        st.dataframe(cottage_df)
    else:
        st.warning("No cottages found.")

    # Add Cottage
    st.write("### Add Cottage")
    cot_name = st.text_input("Cottage Name")
    if st.button("Create Cottage"):
        if cot_name:
            create_cottage(cot_name)
            cottage_id = get_last_insert_id()
            st.success(f"Added Cottage: {cot_name} (ID: {cottage_id})")
            st.rerun()
        else:
            st.warning("Please enter a Cottage Name.")

    # Edit Cottage
    st.write("### Edit Cottage")
    if cottage_data:
        selected_cottage_name = st.selectbox("Select a Cottage to Edit", 
                                             options=[cottage['cot_name'] for cottage in cottage_data])
        selected_cottage_id = next((cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == selected_cottage_name), None)
        new_cot_name = st.text_input("New Cottage Name")
        
        if st.button("Update Cottage"):
            if new_cot_name:
                edit_cottage(selected_cottage_id, new_cot_name)
                st.success(f"Updated Cottage to: {new_cot_name}")
            else:
                st.warning("Please enter a new Cottage Name.")

        if st.button("Delete Cottage"):
            delete_cottage(selected_cottage_id)
            st.success(f"Deleted Cottage: {selected_cottage_name}")

    # Cottage Attributes
    st.write("### Cottage Attributes")
    cottage_attributes_data = get_cottage_attributes_relation()
    if cottage_attributes_data:
        attributes_df = pd.DataFrame(cottage_attributes_data)
        st.dataframe(attributes_df)
    else:
        st.warning("No cottage attributes found.")

    # Edit Cottage Attributes
    st.write("### Edit Attributes for Cottage")
    if cottage_data:
        selected_cottage_name = st.selectbox("Select a Cottage to Edit Attributes", 
                                             options=[cottage['cot_name'] for cottage in cottage_data], key="cottage_select")
        selected_cottage_id = next((cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == selected_cottage_name), None)

        current_attributes = next((attr for attr in cottage_attributes_data if attr['cot_id'] == selected_cottage_id), None)

        if current_attributes:
            # Fetch options for attributes
            pool_options = get_pools()
            loc_options = get_locations()
            room_options = get_rooms()
            max_pax_options = get_maximum_pax()
            ct_options = get_cottage_types()
            ct_stat_options = get_cottage_statuses()

            # Current selections
            pool_selection = st.selectbox("Select Pool", options=[f"{pool['pool_id']}: {pool['pool_detail']}" for pool in pool_options],
                                          index=[i for i, pool in enumerate(pool_options) if pool['pool_id'] == current_attributes['pool_id']][0])
            loc_selection = st.selectbox("Select Location", options=[f"{loc['loc_id']}: {loc['loc_details']}" for loc in loc_options],
                                          index=[i for i, loc in enumerate(loc_options) if loc['loc_id'] == current_attributes['loc_id']][0])
            room_selection = st.selectbox("Select Room", options=[f"{room['room_id']}: {room['room_details']}" for room in room_options],
                                          index=[i for i, room in enumerate(room_options) if room['room_id'] == current_attributes['room_id']][0])
            max_pax_selection = st.selectbox("Select Maximum Pax", options=[f"{max_pax['max_pax_id']}: {max_pax['max_pax_detail']}" for max_pax in max_pax_options],
                                              index=[i for i, max_pax in enumerate(max_pax_options) if max_pax['max_pax_id'] == current_attributes['max_pax_id']][0])
            ct_selection = st.selectbox("Select Cottage Type", options=[f"{ct['ct_id']}: {ct['ct_details']}" for ct in ct_options],
                                         index=[i for i, ct in enumerate(ct_options) if ct['ct_id'] == current_attributes['ct_id']][0])
            ct_stat_selection = st.selectbox("Select Cottage Status", options=[f"{ct_stat['ct_id_stat']}: {ct_stat['ct_details_stat']}" for ct_stat in ct_stat_options],
                                              index=[i for i, ct_stat in enumerate(ct_stat_options) if ct_stat['ct_id_stat'] == current_attributes['ct_id_stat']][0])

            if st.button("Update Attributes"):
                new_pool_id = pool_selection.split(":")[0]
                new_loc_id = loc_selection.split(":")[0]
                new_room_id = room_selection.split(":")[0]
                new_max_pax_id = max_pax_selection.split(":")[0]
                new_ct_id = ct_selection.split(":")[0]
                new_ct_id_stat = ct_stat_selection.split(":")[0]

                edit_cottage_attributes(selected_cottage_id, new_pool_id, new_loc_id, new_room_id, new_max_pax_id, new_ct_id, new_ct_id_stat)
                st.success("Updated Cottage Attributes")
        else:
            st.warning("No attributes found for the selected cottage.")


if __name__ == "__main__":
    show_cottage_management()
