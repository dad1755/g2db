import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database configuration (update as necessary)
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def execute_query(query, params=None):
    """Execute a query with optional parameters."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)  # Using parameterized queries for safety
        else:
            cursor.execute(query)
        connection.commit()
        st.success("Query executed successfully.")  # Debug message
        return cursor  # Return cursor for further processing
    except Error as e:
        st.error(f"Error executing query: {query} with params: {params} | Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def fetch_cottages_with_attributes():
    """Fetch cottages along with their attributes from COTTAGE_ATTRIBUTES_RELATION."""
    query = """
    SELECT 
        CAR.id,
        C.cottage_name,  -- Assuming cottage_name exists in COTTAGE
        CAR.pool_id,
        CAR.loc_id,
        CAR.room_id,
        CAR.max_pax_id,
        CAR.ct_id,
        CAR.ct_id_stat
    FROM COTTAGE_ATTRIBUTES_RELATION CAR
    JOIN COTTAGE C ON CAR.cot_id = C.cot_id
    """
    return fetch_data(query) or []

def fetch_data(query):
    """Fetch data from the database."""
    connection = None
    cursor = None
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
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def edit_cottage_attributes(selected_cottage_id, new_pool_id, new_loc_id, new_room_id, new_max_pax_id, new_ct_id, new_ct_stat_id):
    """Edit attributes of a cottage in the COTTAGE_ATTRIBUTES_RELATION table."""
    query = """
    UPDATE COTTAGE_ATTRIBUTES_RELATION 
    SET pool_id = %s, loc_id = %s, room_id = %s, max_pax_id = %s, ct_id = %s, ct_id_stat = %s 
    WHERE id = %s
    """
    params = (new_pool_id, new_loc_id, new_room_id, new_max_pax_id, new_ct_id, new_ct_stat_id, selected_cottage_id)
    execute_query(query, params)


# CRUD Functions for Pool
def create_pool(pool_detail):
    """Create a new pool."""
    query = "INSERT INTO POOL (pool_detail) VALUES (%s)"
    execute_query(query, (pool_detail,))

def get_pool():
    """Fetch all pools."""
    query = "SELECT * FROM POOL"
    return fetch_data(query) or []

def update_pool(pool_id, pool_detail):
    """Update pool information."""
    query = "UPDATE POOL SET pool_detail = %s WHERE pool_id = %s"
    execute_query(query, (pool_detail, pool_id))

def delete_pool(pool_id):
    """Delete a pool by ID."""
    query = "DELETE FROM POOL WHERE pool_id = %s"
    execute_query(query, (pool_id,))

# CRUD Functions for Location
def create_location(loc_detail):
    """Create a new location."""
    query = "INSERT INTO LOCATION (loc_details) VALUES (%s)"
    execute_query(query, (loc_detail,))

def get_locations():
    """Fetch all locations."""
    query = "SELECT * FROM LOCATION"
    return fetch_data(query) or []

def update_location(loc_id, loc_detail):
    """Update location information."""
    query = "UPDATE LOCATION SET loc_details = %s WHERE loc_id = %s"
    execute_query(query, (loc_detail, loc_id))

def delete_location(loc_id):
    """Delete a location by ID."""
    query = "DELETE FROM LOCATION WHERE loc_id = %s"
    execute_query(query, (loc_id,))

# CRUD Functions for Room
def create_room(room_detail):
    """Create a new room."""
    query = "INSERT INTO ROOM (room_details) VALUES (%s)"
    execute_query(query, (room_detail,))

def get_rooms():
    """Fetch all rooms."""
    query = "SELECT * FROM ROOM"
    return fetch_data(query) or []

def update_room(room_id, room_detail):
    """Update room information."""
    query = "UPDATE ROOM SET room_details = %s WHERE room_id = %s"
    execute_query(query, (room_detail, room_id))

def delete_room(room_id):
    """Delete a room by ID."""
    query = "DELETE FROM ROOM WHERE room_id = %s"
    execute_query(query, (room_id,))

# CRUD Functions for Maximum Pax
def create_maximum_pax(max_pax_detail):
    """Create a new maximum pax detail."""
    query = "INSERT INTO MAXIMUM_PAX (max_pax_details) VALUES (%s)"
    execute_query(query, (max_pax_detail,))

def get_maximum_pax():
    """Fetch all maximum pax details."""
    query = "SELECT * FROM MAXIMUM_PAX"
    return fetch_data(query) or []

def update_maximum_pax(max_pax_id, max_pax_detail):
    """Update maximum pax information."""
    query = "UPDATE MAXIMUM_PAX SET max_pax_details = %s WHERE max_pax_id = %s"
    execute_query(query, (max_pax_detail, max_pax_id))

def delete_maximum_pax(max_pax_id):
    """Delete maximum pax detail by ID."""
    query = "DELETE FROM MAXIMUM_PAX WHERE max_pax_id = %s"
    execute_query(query, (max_pax_id,))

# CRUD Functions for Cottage Types
def create_cottage_type(ct_detail):
    """Create a new cottage type."""
    query = "INSERT INTO COTTAGE_TYPES (ct_details) VALUES (%s)"
    execute_query(query, (ct_detail,))

def get_cottage_types():
    """Fetch all cottage types."""
    query = "SELECT * FROM COTTAGE_TYPES"
    return fetch_data(query) or []

def update_cottage_type(ct_id, ct_detail):
    """Update cottage type information."""
    query = "UPDATE COTTAGE_TYPES SET ct_details = %s WHERE ct_id = %s"
    execute_query(query, (ct_detail, ct_id))

def delete_cottage_type(ct_id):
    """Delete cottage type by ID."""
    query = "DELETE FROM COTTAGE_TYPES WHERE ct_id = %s"
    execute_query(query, (ct_id,))

# CRUD Functions for Cottage Status
def create_cottage_status(cottage_status_detail):
    """Create a new cottage status."""
    query = "INSERT INTO COTTAGE_STATUS (ct_details) VALUES (%s)"
    execute_query(query, (cottage_status_detail,))

def get_cottage_statuses():
    """Fetch all cottage statuses."""
    query = "SELECT * FROM COTTAGE_STATUS"
    return fetch_data(query) or []

def update_cottage_status(cottage_status_id, cottage_status_detail):
    """Update cottage status information."""
    query = "UPDATE COTTAGE_STATUS SET ct_details = %s WHERE cottage_status_id = %s"
    execute_query(query, (cottage_status_detail, cottage_status_id))

def delete_cottage_status(cottage_status_id):
    """Delete cottage status by ID."""
    query = "DELETE FROM COTTAGE_STATUS WHERE cottage_status_id = %s"
    execute_query(query, (cottage_status_id,))

def show_facilities_management():
    """Streamlit UI for Facility, Location, Room, Maximum Pax, Cottage Types, and Cottage Status Management."""
    st.write("### Facilities Management 📦")

    # Add Pool
    st.write("###### Function to Add New Pool")
    pool_detail = st.text_input("Pool Detail")
    if st.button("Add Pool"):
        if pool_detail:
            create_pool(pool_detail)
            st.success(f"Added Pool: {pool_detail}")
        else:
            st.warning("Please fill in the Pool Detail.")

    # View Pools
    st.write("###### Available Pools in Database")
    pools_data = get_pool()
    if pools_data:
        st.dataframe(pools_data)

        # Update Pool
        st.write("###### Function to Update Pool")
        pool_names = [f"{pool['pool_detail']} (ID: {pool['pool_id']})" for pool in pools_data]
        pool_name_to_update = st.selectbox("Select Pool to Update", options=pool_names)

        if pool_name_to_update:
            pool_id_to_update = int(pool_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_pool = next((pool for pool in pools_data if pool['pool_id'] == pool_id_to_update), None)

            if selected_pool:
                updated_pool_detail = st.text_input("Updated Pool Detail", value=selected_pool['pool_detail'])
                if st.button("Update Pool"):
                    update_pool(pool_id_to_update, updated_pool_detail)
                    st.success("Updated Pool successfully!")

        # Delete Pool
        st.write("###### Function to Delete Pool")
        pool_name_to_delete = st.selectbox("Select Pool to Delete", options=pool_names)
        if st.button("Delete Pool"):
            pool_id_to_delete = int(pool_name_to_delete.split("(ID: ")[-1][:-1])
            delete_pool(pool_id_to_delete)
            st.success("Deleted Pool successfully!")

    # Repeat similar blocks for Location, Room, Maximum Pax, Cottage Types, Cottage Status

def show_cottage_management():
    """Streamlit UI for managing Cottages."""
    st.write("### Cottage Management 🏡")

    cottages = fetch_cottages_with_attributes()
    if cottages:
        st.write("###### Cottages with Attributes")
        st.dataframe(cottages)

        # Editing Cottage Attributes
        st.write("###### Edit Cottage Attributes")
        cottage_names = [f"{cottage['cottage_name']} (ID: {cottage['id']})" for cottage in cottages]
        selected_cottage = st.selectbox("Select Cottage to Edit", options=cottage_names)

        if selected_cottage:
            selected_cottage_id = int(selected_cottage.split("(ID: ")[-1][:-1])
            selected_cottage_data = next((cottage for cottage in cottages if cottage['id'] == selected_cottage_id), None)

            if selected_cottage_data:
                new_pool_id = st.number_input("New Pool ID", value=selected_cottage_data['pool_id'])
                new_loc_id = st.number_input("New Location ID", value=selected_cottage_data['loc_id'])
                new_room_id = st.number_input("New Room ID", value=selected_cottage_data['room_id'])
                new_max_pax_id = st.number_input("New Maximum Pax ID", value=selected_cottage_data['max_pax_id'])
                new_ct_id = st.number_input("New Cottage Type ID", value=selected_cottage_data['ct_id'])
                new_ct_stat_id = st.number_input("New Cottage Status ID", value=selected_cottage_data['ct_id_stat'])

                if st.button("Update Cottage Attributes"):
                    st.write("Selected Cottage ID:", selected_cottage_id)
                    st.write("New Pool ID:", new_pool_id)
                    st.write("New Location ID:", new_loc_id)
                    st.write("New Room ID:", new_room_id)
                    st.write("New Maximum Pax ID:", new_max_pax_id)
                    st.write("New Cottage Type ID:", new_ct_id)
                    st.write("New Cottage Status ID:", new_ct_stat_id)
                
                    edit_cottage_attributes(selected_cottage_id, new_pool_id, new_loc_id, new_room_id, new_max_pax_id, new_ct_id, new_ct_stat_id)
                    st.success(f"Updated attributes for Cottage ID: {selected_cottage_id}")


def main():
    st.title("Cottage Management System")

    menu = ["Manage Facilities", "Manage Cottages"]
    choice = st.sidebar.selectbox("Select Activity", menu)

    if choice == "Manage Facilities":
        show_facilities_management()
    elif choice == "Manage Cottages":
        show_cottage_management()

if __name__ == "__main__":
    main()
