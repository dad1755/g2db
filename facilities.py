# poolilities.py
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

# CRUD Functions for Facilities
def create_pool(pool_detail):
    """Create a new pool."""
    query = "INSERT INTO FACILITIES (pool_detail) VALUES (%s)"
    execute_query(query, (pool_detail,))

def get_pool():
    """Fetch all pool."""
    query = "SELECT * FROM POOL"
    return fetch_data(query) or []

def update_POOL(pool_id, pool_detail):
    """Update pool information."""
    query = "UPDATE POOL SET pool_detail = %s WHERE pool_id = %s"
    execute_query(query, (pool_detail, pool_id))

def delete_pool(pool_id):
    """Delete a poolility by ID."""
    query = "DELETE FROM FACILITIES WHERE pool_id = %s"
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
def show_management():
    """Streamlit UI for Facility, Location, Room, Maximum Pax, Cottage Types, and Cottage Status Management."""
    st.subheader("Management Dashboard")

    # Add Facility
    st.write("### Add Facility")
    pool_detail = st.text_input("Pool Detail")
    if st.button("Add Pool"):
        if pool_detail:
            create_pool(pool_detail)
            st.success(f"Added Facility: {pool_detail}")
        else:
            st.warning("Please fill in the Facility Detail.")

    # View Pool
    st.write("### Facility List")
    pool_data = get_pool()
    if pool_data:
        st.dataframe(pool_data)

        # Update Pool
        st.write("### Update Pool")
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
        st.write("### Delete Pool")
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
    st.write("### Add Location")
    loc_detail = st.text_input("Location Detail")
    if st.button("Add Location"):
        if loc_detail:
            create_location(loc_detail)
            st.success(f"Added Location: {loc_detail}")
        else:
            st.warning("Please fill in the Location Detail.")

    # View Locations
    st.write("### Location List")
    locations_data = get_locations()
    if locations_data:
        st.dataframe(locations_data)

        # Update Location
        st.write("### Update Location")
        loc_names = [f"{location['loc_details']} (ID: {location['loc_id']})" for location in locations_data]
        loc_name_to_update = st.selectbox("Select Location to Update", options=loc_names)

        if loc_name_to_update:
            loc_id_to_update = int(loc_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_location = next((location for location in locations_data if location['loc_id'] == loc_id_to_update), None)

            if selected_location:
                updated_loc_detail = st.text_input("Updated Location Detail", value=selected_location['loc_details'])

                if st.button("Update Location"):
                    update_location(loc_id_to_update, updated_loc_detail)
                    st.success(f"Updated Location: {updated_loc_detail}")

        # Delete Location
        st.write("### Delete Location")
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

    # Add Room
    st.write("### Add Room")
    room_detail = st.text_input("Room Detail")
    if st.button("Add Room"):
        if room_detail:
            create_room(room_detail)
            st.success(f"Added Room: {room_detail}")
        else:
            st.warning("Please fill in the Room Detail.")

    # View Rooms
    st.write("### Room List")
    rooms_data = get_rooms()
    if rooms_data:
        st.dataframe(rooms_data)

        # Update Room
        st.write("### Update Room")
        room_names = [f"{room['room_details']} (ID: {room['room_id']})" for room in rooms_data]
        room_name_to_update = st.selectbox("Select Room to Update", options=room_names)

        if room_name_to_update:
            room_id_to_update = int(room_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_room = next((room for room in rooms_data if room['room_id'] == room_id_to_update), None)

            if selected_room:
                updated_room_detail = st.text_input("Updated Room Detail", value=selected_room['room_details'])

                if st.button("Update Room"):
                    update_room(room_id_to_update, updated_room_detail)
                    st.success(f"Updated Room: {updated_room_detail}")

        # Delete Room
        st.write("### Delete Room")
        room_name_to_delete = st.selectbox("Select Room to Delete", options=room_names)

        if st.button("Delete Room"):
            if room_name_to_delete:
                room_id_to_delete = int(room_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_room(room_id_to_delete)
                st.success(f"Deleted Room: {room_name_to_delete}")
            else:
                st.warning("Please select a Room to delete.")
    else:
        st.warning("No rooms found.")

    # Add Maximum Pax
    st.write("### Add Maximum Pax")
    max_pax_detail = st.text_input("Maximum Pax Detail")
    if st.button("Add Maximum Pax"):
        if max_pax_detail:
            create_maximum_pax(max_pax_detail)
            st.success(f"Added Maximum Pax: {max_pax_detail}")
        else:
            st.warning("Please fill in the Maximum Pax Detail.")

    # View Maximum Pax
    st.write("### Maximum Pax List")
    max_pax_data = get_maximum_pax()
    if max_pax_data:
        st.dataframe(max_pax_data)

        # Update Maximum Pax
        st.write("### Update Maximum Pax")
        max_pax_names = [f"{max_pax['max_pax_details']} (ID: {max_pax['max_pax_id']})" for max_pax in max_pax_data]
        max_pax_name_to_update = st.selectbox("Select Maximum Pax to Update", options=max_pax_names)

        if max_pax_name_to_update:
            max_pax_id_to_update = int(max_pax_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_max_pax = next((max_pax for max_pax in max_pax_data if max_pax['max_pax_id'] == max_pax_id_to_update), None)

            if selected_max_pax:
                updated_max_pax_detail = st.text_input("Updated Maximum Pax Detail", value=selected_max_pax['max_pax_details'])

                if st.button("Update Maximum Pax"):
                    update_maximum_pax(max_pax_id_to_update, updated_max_pax_detail)
                    st.success(f"Updated Maximum Pax: {updated_max_pax_detail}")

        # Delete Maximum Pax
        st.write("### Delete Maximum Pax")
        max_pax_name_to_delete = st.selectbox("Select Maximum Pax to Delete", options=max_pax_names)

        if st.button("Delete Maximum Pax"):
            if max_pax_name_to_delete:
                max_pax_id_to_delete = int(max_pax_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_maximum_pax(max_pax_id_to_delete)
                st.success(f"Deleted Maximum Pax: {max_pax_name_to_delete}")
            else:
                st.warning("Please select a Maximum Pax to delete.")
    else:
        st.warning("No maximum pax details found.")

    # Add Cottage Type
    st.write("### Add Cottage Type")
    ct_detail = st.text_input("Cottage Type Detail")
    if st.button("Add Cottage Type"):
        if ct_detail:
            create_cottage_type(ct_detail)
            st.success(f"Added Cottage Type: {ct_detail}")
        else:
            st.warning("Please fill in the Cottage Type Detail.")

    # View Cottage Types
    st.write("### Cottage Type List")
    cottage_types_data = get_cottage_types()
    if cottage_types_data:
        st.dataframe(cottage_types_data)

        # Update Cottage Type
        st.write("### Update Cottage Type")
        ct_names = [f"{cottage_type['ct_details']} (ID: {cottage_type['ct_id']})" for cottage_type in cottage_types_data]
        ct_name_to_update = st.selectbox("Select Cottage Type to Update", options=ct_names)

        if ct_name_to_update:
            ct_id_to_update = int(ct_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_cottage_type = next((cottage_type for cottage_type in cottage_types_data if cottage_type['ct_id'] == ct_id_to_update), None)

            if selected_cottage_type:
                updated_ct_detail = st.text_input("Updated Cottage Type Detail", value=selected_cottage_type['ct_details'])

                if st.button("Update Cottage Type"):
                    update_cottage_type(ct_id_to_update, updated_ct_detail)
                    st.success(f"Updated Cottage Type: {updated_ct_detail}")

        # Delete Cottage Type
        st.write("### Delete Cottage Type")
        ct_name_to_delete = st.selectbox("Select Cottage Type to Delete", options=ct_names)

        if st.button("Delete Cottage Type"):
            if ct_name_to_delete:
                ct_id_to_delete = int(ct_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_cottage_type(ct_id_to_delete)
                st.success(f"Deleted Cottage Type: {ct_name_to_delete}")
            else:
                st.warning("Please select a Cottage Type to delete.")
    else:
        st.warning("No cottage types found.")

    # Add Cottage Status
    st.write("### Add Cottage Status")
    cottage_status_detail = st.text_input("Cottage Status Detail")
    if st.button("Add Cottage Status"):
        if cottage_status_detail:
            create_cottage_status(cottage_status_detail)
            st.success(f"Added Cottage Status: {cottage_status_detail}")
        else:
            st.warning("Please fill in the Cottage Status Detail.")

    # View Cottage Statuses
    st.write("### Cottage Status List")
    cottage_statuses_data = get_cottage_statuses()
    if cottage_statuses_data:
        st.dataframe(cottage_statuses_data)

        # Update Cottage Status
        st.write("### Update Cottage Status")
        cottage_status_names = [f"{cottage_status['ct_details']} (ID: {cottage_status['cottage_status_id']})" for cottage_status in cottage_statuses_data]
        cottage_status_name_to_update = st.selectbox("Select Cottage Status to Update", options=cottage_status_names)

        if cottage_status_name_to_update:
            cottage_status_id_to_update = int(cottage_status_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_cottage_status = next((cottage_status for cottage_status in cottage_statuses_data if cottage_status['cottage_status_id'] == cottage_status_id_to_update), None)

            if selected_cottage_status:
                updated_cottage_status_detail = st.text_input("Updated Cottage Status Detail", value=selected_cottage_status['ct_details'])

                if st.button("Update Cottage Status"):
                    update_cottage_status(cottage_status_id_to_update, updated_cottage_status_detail)
                    st.success(f"Updated Cottage Status: {updated_cottage_status_detail}")

        # Delete Cottage Status
        st.write("### Delete Cottage Status")
        cottage_status_name_to_delete = st.selectbox("Select Cottage Status to Delete", options=cottage_status_names)

        if st.button("Delete Cottage Status"):
            if cottage_status_name_to_delete:
                cottage_status_id_to_delete = int(cottage_status_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_cottage_status(cottage_status_id_to_delete)
                st.success(f"Deleted Cottage Status: {cottage_status_name_to_delete}")
            else:
                st.warning("Please select a Cottage Status to delete.")
    else:
        st.warning("No cottage statuses found.")

# CRUD Functions for Locations
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

# CRUD Functions for Rooms
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
    """Create a new maximum pax."""
    query = "INSERT INTO MAXIMUM_PAX (max_pax_details) VALUES (%s)"
    execute_query(query, (max_pax_detail,))

def get_maximum_pax():
    """Fetch all maximum pax."""
    query = "SELECT * FROM MAXIMUM_PAX"
    return fetch_data(query) or []

def update_maximum_pax(max_pax_id, max_pax_detail):
    """Update maximum pax information."""
    query = "UPDATE MAXIMUM_PAX SET max_pax_details = %s WHERE max_pax_id = %s"
    execute_query(query, (max_pax_detail, max_pax_id))

def delete_maximum_pax(max_pax_id):
    """Delete a maximum pax by ID."""
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
    """Delete a cottage type by ID."""
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
    """Delete a cottage status by ID."""
    query = "DELETE FROM COTTAGE_STATUS WHERE cottage_status_id = %s"
    execute_query(query, (cottage_status_id,))

def show_poolilities_management():
    """Streamlit UI for Facility Management."""
    st.subheader("Management Dashboard")

    # ===================
    # Add Facility
    # ===================
    st.write("### Add Facility")
    pool_detail = st.text_input("Facility Detail")
    if st.button("Add Facility"):
        if pool_detail:
            create_poolility(pool_detail)
            st.success(f"Added Facility: {pool_detail}")
        else:
            st.warning("Please fill in the Facility Detail.")

    # View Facilities
    st.write("### Facility List")
    poolilities_data = get_poolilities()
    if poolilities_data:
        st.dataframe(poolilities_data)
        
        # Update Facility
        st.write("### Update Facility")
        pool_names = [f"{poolility['pool_detail']} (ID: {poolility['pool_id']})" for poolility in poolilities_data]
        pool_name_to_update = st.selectbox("Select Facility to Update", options=pool_names)

        if pool_name_to_update:
            pool_id_to_update = int(pool_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_poolility = next((poolility for poolility in poolilities_data if poolility['pool_id'] == pool_id_to_update), None)

            if selected_poolility:
                updated_detail = st.text_input("Updated Facility Detail", value=selected_poolility['pool_detail'])

                if st.button("Update Facility"):
                    update_poolility(pool_id_to_update, updated_detail)
                    st.success(f"Updated Facility: {updated_detail}")

        # Delete Facility
        st.write("### Delete Facility")
        pool_name_to_delete = st.selectbox("Select Facility to Delete", options=pool_names)

        if st.button("Delete Facility"):
            if pool_name_to_delete:
                pool_id_to_delete = int(pool_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_poolility(pool_id_to_delete)
                st.success(f"Deleted Facility: {pool_name_to_delete}")
            else:
                st.warning("Please select a Facility to delete.")
    else:
        st.warning("No poolilities found.")

    # ===================
    # Add Location
    # ===================
    st.write("### Add Location")
    loc_detail = st.text_input("Location Detail")
    if st.button("Add Location"):
        if loc_detail:
            create_location(loc_detail)
            st.success(f"Added Location: {loc_detail}")
        else:
            st.warning("Please fill in the Location Detail.")

    # View Locations
    st.write("### Location List")
    locations_data = get_locations()
    if locations_data:
        st.dataframe(locations_data)

        # Update Location
        st.write("### Update Location")
        loc_names = [f"{location['loc_details']} (ID: {location['loc_id']})" for location in locations_data]
        loc_name_to_update = st.selectbox("Select Location to Update", options=loc_names)

        if loc_name_to_update:
            loc_id_to_update = int(loc_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_location = next((location for location in locations_data if location['loc_id'] == loc_id_to_update), None)

            if selected_location:
                updated_loc_detail = st.text_input("Updated Location Detail", value=selected_location['loc_details'])

                if st.button("Update Location"):
                    update_location(loc_id_to_update, updated_loc_detail)
                    st.success(f"Updated Location: {updated_loc_detail}")

        # Delete Location
        st.write("### Delete Location")
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

    # ===================
    # Add Room
    # ===================
    st.write("### Add Room")
    room_detail = st.text_input("Room Detail")
    if st.button("Add Room"):
        if room_detail:
            create_room(room_detail)
            st.success(f"Added Room: {room_detail}")
        else:
            st.warning("Please fill in the Room Detail.")

    # View Rooms
    st.write("### Room List")
    rooms_data = get_rooms()
    if rooms_data:
        st.dataframe(rooms_data)

        # Update Room
        st.write("### Update Room")
        room_names = [f"{room['room_details']} (ID: {room['room_id']})" for room in rooms_data]
        room_name_to_update = st.selectbox("Select Room to Update", options=room_names)

        if room_name_to_update:
            room_id_to_update = int(room_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_room = next((room for room in rooms_data if room['room_id'] == room_id_to_update), None)

            if selected_room:
                updated_room_detail = st.text_input("Updated Room Detail", value=selected_room['room_details'])

                if st.button("Update Room"):
                    update_room(room_id_to_update, updated_room_detail)
                    st.success(f"Updated Room: {updated_room_detail}")

        # Delete Room
        st.write("### Delete Room")
        room_name_to_delete = st.selectbox("Select Room to Delete", options=room_names)

        if st.button("Delete Room"):
            if room_name_to_delete:
                room_id_to_delete = int(room_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_room(room_id_to_delete)
                st.success(f"Deleted Room: {room_name_to_delete}")
            else:
                st.warning("Please select a Room to delete.")
    else:
        st.warning("No rooms found.")

    # ===================
    # Add Maximum Pax
    # ===================
    st.write("### Add Maximum Pax")
    max_pax_detail = st.text_input("Maximum Pax Detail")
    if st.button("Add Maximum Pax"):
        if max_pax_detail:
            create_maximum_pax(max_pax_detail)
            st.success(f"Added Maximum Pax: {max_pax_detail}")
        else:
            st.warning("Please fill in the Maximum Pax Detail.")

    # View Maximum Pax
    st.write("### Maximum Pax List")
    max_pax_data = get_maximum_pax()
    if max_pax_data:
        st.dataframe(max_pax_data)

        # Update Maximum Pax
        st.write("### Update Maximum Pax")
        max_pax_names = [f"{max_pax['max_pax_details']} (ID: {max_pax['max_pax_id']})" for max_pax in max_pax_data]
        max_pax_name_to_update = st.selectbox("Select Maximum Pax to Update", options=max_pax_names)

        if max_pax_name_to_update:
            max_pax_id_to_update = int(max_pax_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_max_pax = next((max_pax for max_pax in max_pax_data if max_pax['max_pax_id'] == max_pax_id_to_update), None)

            if selected_max_pax:
                updated_max_pax_detail = st.text_input("Updated Maximum Pax Detail", value=selected_max_pax['max_pax_details'])

                if st.button("Update Maximum Pax"):
                    update_maximum_pax(max_pax_id_to_update, updated_max_pax_detail)
                    st.success(f"Updated Maximum Pax: {updated_max_pax_detail}")

        # Delete Maximum Pax
        st.write("### Delete Maximum Pax")
        max_pax_name_to_delete = st.selectbox("Select Maximum Pax to Delete", options=max_pax_names)

        if st.button("Delete Maximum Pax"):
            if max_pax_name_to_delete:
                max_pax_id_to_delete = int(max_pax_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_maximum_pax(max_pax_id_to_delete)
                st.success(f"Deleted Maximum Pax: {max_pax_name_to_delete}")
            else:
                st.warning("Please select a Maximum Pax to delete.")
    else:
        st.warning("No maximum pax details found.")

    # ===================
    # Add Cottage Type
    # ===================
    st.write("### Add Cottage Type")
    ct_detail = st.text_input("Cottage Type Detail")
    if st.button("Add Cottage Type"):
        if ct_detail:
            create_cottage_type(ct_detail)
            st.success(f"Added Cottage Type: {ct_detail}")
        else:
            st.warning("Please fill in the Cottage Type Detail.")

    # View Cottage Types
    st.write("### Cottage Type List")
    cottage_types_data = get_cottage_types()
    if cottage_types_data:
        st.dataframe(cottage_types_data)

        # Update Cottage Type
        st.write("### Update Cottage Type")
        ct_names = [f"{cottage_type['ct_details']} (ID: {cottage_type['ct_id']})" for cottage_type in cottage_types_data]
        ct_name_to_update = st.selectbox("Select Cottage Type to Update", options=ct_names)

        if ct_name_to_update:
            ct_id_to_update = int(ct_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_cottage_type = next((cottage_type for cottage_type in cottage_types_data if cottage_type['ct_id'] == ct_id_to_update), None)

            if selected_cottage_type:
                updated_ct_detail = st.text_input("Updated Cottage Type Detail", value=selected_cottage_type['ct_details'])

                if st.button("Update Cottage Type"):
                    update_cottage_type(ct_id_to_update, updated_ct_detail)
                    st.success(f"Updated Cottage Type: {updated_ct_detail}")

        # Delete Cottage Type
        st.write("### Delete Cottage Type")
        ct_name_to_delete = st.selectbox("Select Cottage Type to Delete", options=ct_names)

        if st.button("Delete Cottage Type"):
            if ct_name_to_delete:
                ct_id_to_delete = int(ct_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_cottage_type(ct_id_to_delete)
                st.success(f"Deleted Cottage Type: {ct_name_to_delete}")
            else:
                st.warning("Please select a Cottage Type to delete.")
    else:
        st.warning("No cottage types found.")

    # ===================
    # Add Cottage Status
    # ===================
    st.write("### Add Cottage Status")
    cottage_status_detail = st.text_input("Cottage Status Detail")
    if st.button("Add Cottage Status"):
        if cottage_status_detail:
            create_cottage_status(cottage_status_detail)
            st.success(f"Added Cottage Status: {cottage_status_detail}")
        else:
            st.warning("Please fill in the Cottage Status Detail.")

    # View Cottage Status
    st.write("### Cottage Status List")
    cottage_status_data = get_cottage_statuses()
    if cottage_status_data:
        st.dataframe(cottage_status_data)

        # Update Cottage Status
        st.write("### Update Cottage Status")
        cottage_status_names = [f"{cottage_status['ct_details']} (ID: {cottage_status['cottage_status_id']})" for cottage_status in cottage_status_data]
        cottage_status_name_to_update = st.selectbox("Select Cottage Status to Update", options=cottage_status_names)

        if cottage_status_name_to_update:
            cottage_status_id_to_update = int(cottage_status_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_cottage_status = next((cottage_status for cottage_status in cottage_status_data if cottage_status['cottage_status_id'] == cottage_status_id_to_update), None)

            if selected_cottage_status:
                updated_cottage_status_detail = st.text_input("Updated Cottage Status Detail", value=selected_cottage_status['ct_details'])

                if st.button("Update Cottage Status"):
                    update_cottage_status(cottage_status_id_to_update, updated_cottage_status_detail)
                    st.success(f"Updated Cottage Status: {updated_cottage_status_detail}")

        # Delete Cottage Status
        st.write("### Delete Cottage Status")
        cottage_status_name_to_delete = st.selectbox("Select Cottage Status to Delete", options=cottage_status_names)

        if st.button("Delete Cottage Status"):
            if cottage_status_name_to_delete:
                cottage_status_id_to_delete = int(cottage_status_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_cottage_status(cottage_status_id_to_delete)
                st.success(f"Deleted Cottage Status: {cottage_status_name_to_delete}")
            else:
                st.warning("Please select a Cottage Status to delete.")
    else:
        st.warning("No cottage statuses found.")

