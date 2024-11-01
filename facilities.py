# facilities.py
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
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)  # Using parameterized queries for safety
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

# Streamlit UI for managing various entities
def show_facilities_management():
    """Streamlit UI for Facility, Location, Room, Maximum Pax, Cottage Types, and Cottage Status Management."""
    st.write("### Facilities Management 📦")

    # Add Pool
    st.write("###### Function To Add New Pool Type")
    pool_detail = st.text_input("Pool Detail")
    if st.button("Add Pool"):
        if pool_detail:
            create_pool(pool_detail)
            st.success(f"Added Facility: {pool_detail}")
        else:
            st.warning("Please fill in the Facility Detail.")

    # View Pools
    st.write("###### Pool Types Available in Database")
    pool_data = get_pool()
    if pool_data:
        st.dataframe(pool_data)

        # Update Pool
        st.write("###### Function To Update Pool")
        pool_names = [f"{pool['pool_detail']} (ID: {pool['pool_id']})" for pool in pool_data]
        pool_name_to_update = st.selectbox("Select Pool to Update", options=pool_names)

        if pool_name_to_update:
            pool_id_to_update = int(pool_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_pool = next((pool for pool in pool_data if pool['pool_id'] == pool_id_to_update), None)

            if selected_pool:
                updated_detail = st.text_input("Updated Detail", value=selected_pool['pool_detail'])

                if st.button("Update Pool"):
                    update_pool(pool_id_to_update, updated_detail)
                    st.success(f"Updated Facility: {updated_detail}")

        # Delete Pool
        st.write("###### Function To Delete Pool")
        pool_name_to_delete = st.selectbox("Select Pool to Delete", options=pool_names)

        if st.button("Delete Pool"):
            if pool_name_to_delete:
                pool_id_to_delete = int(pool_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_pool(pool_id_to_delete)
                st.success(f"Deleted Facility: {pool_name_to_delete}")
            else:
                st.warning("Please select a Facility to delete.")
    else:
        st.warning("No pool found.")

    # Add Location
    st.write("###### Function To Add New Location Cottage")
    loc_detail = st.text_input("Location Detail")
    if st.button("Add Location"):
        if loc_detail:
            create_location(loc_detail)
            st.success(f"Added Location: {loc_detail}")
        else:
            st.warning("Please fill in the Location Detail.")

    # View Locations
    st.write("###### Locations Available in Database")
    locations_data = get_locations()
    if locations_data:
        st.dataframe(locations_data)

        # Update Location
        st.write("###### Function To Update Location")
        loc_names = [f"{location['loc_details']} (ID: {location['loc_id']})" for location in locations_data]
        loc_name_to_update = st.selectbox("Select Location to Update", options=loc_names)

        if loc_name_to_update:
            loc_id_to_update = int(loc_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_location = next((loc for loc in locations_data if loc['loc_id'] == loc_id_to_update), None)

            if selected_location:
                updated_loc_detail = st.text_input("Updated Detail", value=selected_location['loc_details'])

                if st.button("Update Location"):
                    update_location(loc_id_to_update, updated_loc_detail)
                    st.success(f"Updated Location: {updated_loc_detail}")

        # Delete Location
        st.write("###### Function To Delete Location")
        loc_name_to_delete = st.selectbox("Select Location to Delete", options=loc_names)

        if st.button("Delete Location"):
            if loc_name_to_delete:
                loc_id_to_delete = int(loc_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_location(loc_id_to_delete)
                st.success(f"Deleted Location: {loc_name_to_delete}")
            else:
                st.warning("Please select a Location to delete.")
    else:
        st.warning("No locations found.")

    # Similar structures for Rooms, Maximum Pax, Cottage Types, and Cottage Statuses

# Main Application
if __name__ == "__main__":
    show_facilities_management()
