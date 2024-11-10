import os
import streamlit as st
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text
from mysql.connector import Error

# Retrieve the service account JSON from st.secrets
service_account_info = st.secrets["google_cloud"]["credentials"]

# Write the JSON to a file
with open("service_account.json", "w") as f:
    f.write(service_account_info)

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

# Retrieve database credentials from st.secrets
INSTANCE_CONNECTION_NAME = st.secrets["database"]["instance_connection_name"]
DB_USER = st.secrets["database"]["db_user"]
DB_PASSWORD = st.secrets["database"]["db_password"]
DB_NAME = st.secrets["database"]["db_name"]

# Initialize Connector object
connector = Connector()

# Function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )
    return conn

# SQLAlchemy engine for creating database connection
engine = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Function to execute queries
def execute_query(query, params=None):
    """Execute a query with optional parameters."""
    connection = None
    try:
        with engine.connect() as connection:
            if params:
                connection.execute(text(query), params)
            else:
                connection.execute(text(query))
            st.success("Query executed successfully.")  # Inform the user of success
    except Exception as e:
        st.error(f"Error executing query: {query} | Error: {e}")

# Function to fetch data from the database
def fetch_data(query, params=None):
    """Fetch data from the database."""
    connection = None
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            rows = result.fetchall()
            return rows
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Fetch cottages with their attributes
def fetch_cottages_with_attributes():
    query = """
    SELECT 
        CAR.id,
        C.cottage_name,
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

# Edit cottage attributes
def edit_cottage_attributes(selected_cottage_id, new_pool_id, new_loc_id, new_room_id, new_max_pax_id, new_ct_id, new_ct_stat_id):
    query = """
    UPDATE COTTAGE_ATTRIBUTES_RELATION 
    SET pool_id = %s, loc_id = %s, room_id = %s, max_pax_id = %s, ct_id = %s, ct_id_stat = %s 
    WHERE id = %s
    """
    params = (new_pool_id, new_loc_id, new_room_id, new_max_pax_id, new_ct_id, new_ct_stat_id, selected_cottage_id)
    execute_query(query, params)

# CRUD Functions for Pool
def create_pool(pool_detail):
    query = "INSERT INTO POOL (pool_detail) VALUES (%s)"
    execute_query(query, (pool_detail,))

def get_pool():
    query = "SELECT * FROM POOL"
    return fetch_data(query) or []

def update_pool(pool_id, pool_detail):
    query = "UPDATE POOL SET pool_detail = %s WHERE pool_id = %s"
    execute_query(query, (pool_detail, pool_id))

def delete_pool(pool_id):
    query = "DELETE FROM POOL WHERE pool_id = %s"
    execute_query(query, (pool_id,))

# CRUD Functions for Location
def create_location(loc_detail):
    query = "INSERT INTO LOCATION (loc_details) VALUES (%s)"
    execute_query(query, (loc_detail,))

def get_locations():
    query = "SELECT * FROM LOCATION"
    return fetch_data(query) or []

def update_location(loc_id, loc_detail):
    query = "UPDATE LOCATION SET loc_details = %s WHERE loc_id = %s"
    execute_query(query, (loc_detail, loc_id))

def delete_location(loc_id):
    query = "DELETE FROM LOCATION WHERE loc_id = %s"
    execute_query(query, (loc_id,))

# CRUD Functions for Room
def create_room(room_detail):
    query = "INSERT INTO ROOM (room_details) VALUES (%s)"
    execute_query(query, (room_detail,))

def get_rooms():
    query = "SELECT * FROM ROOM"
    return fetch_data(query) or []

def update_room(room_id, room_detail):
    query = "UPDATE ROOM SET room_details = %s WHERE room_id = %s"
    execute_query(query, (room_detail, room_id))

def delete_room(room_id):
    query = "DELETE FROM ROOM WHERE room_id = %s"
    execute_query(query, (room_id,))

# CRUD Functions for Maximum Pax
def create_maximum_pax(max_pax_detail):
    query = "INSERT INTO MAXIMUM_PAX (max_pax_details) VALUES (%s)"
    execute_query(query, (max_pax_detail,))

def get_maximum_pax():
    query = "SELECT * FROM MAXIMUM_PAX"
    return fetch_data(query) or []

def update_maximum_pax(max_pax_id, max_pax_detail):
    query = "UPDATE MAXIMUM_PAX SET max_pax_details = %s WHERE max_pax_id = %s"
    execute_query(query, (max_pax_detail, max_pax_id))

def delete_maximum_pax(max_pax_id):
    query = "DELETE FROM MAXIMUM_PAX WHERE max_pax_id = %s"
    execute_query(query, (max_pax_id,))

# CRUD Functions for Cottage Types
def create_cottage_type(ct_detail):
    query = "INSERT INTO COTTAGE_TYPES (ct_details) VALUES (%s)"
    execute_query(query, (ct_detail,))

def get_cottage_types():
    query = "SELECT * FROM COTTAGE_TYPES"
    return fetch_data(query) or []

def update_cottage_type(ct_id, ct_detail):
    query = "UPDATE COTTAGE_TYPES SET ct_details = %s WHERE ct_id = %s"
    execute_query(query, (ct_detail, ct_id))

def delete_cottage_type(ct_id):
    query = "DELETE FROM COTTAGE_TYPES WHERE ct_id = %s"
    execute_query(query, (ct_id,))

# CRUD Functions for Cottage Status
def create_cottage_status(cottage_status_detail):
    query = "INSERT INTO COTTAGE_STATUS (ct_status_details) VALUES (%s)"
    execute_query(query, (cottage_status_detail,))

def get_cottage_statuses():
    query = "SELECT * FROM COTTAGE_STATUS"
    return fetch_data(query) or []

def update_cottage_status(cottage_status_id, cottage_status_detail):
    query = "UPDATE COTTAGE_STATUS SET ct_status_details = %s WHERE cottage_status_id = %s"
    execute_query(query, (cottage_status_detail, cottage_status_id))

def delete_cottage_status(cottage_status_id):
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
            selected_pool_id = int(pool_name_to_update.split("(ID: ")[-1][:-1])
            new_pool_detail = st.text_input("New Pool Detail")
            if st.button("Update Pool"):
                if new_pool_detail:
                    update_pool(selected_pool_id, new_pool_detail)
                    st.success(f"Updated Pool ID: {selected_pool_id} with new detail: {new_pool_detail}")
                else:
                    st.warning("Please provide a new Pool Detail.")

            # Delete Pool
            if st.button("Delete Selected Pool"):
                delete_pool(selected_pool_id)
                st.success(f"Deleted Pool ID: {selected_pool_id}")

    # Add Location
    st.write("###### Function to Add New Location")
    loc_detail = st.text_input("Location Detail")
    if st.button("Add Location"):
        if loc_detail:
            create_location(loc_detail)
            st.success(f"Added Location: {loc_detail}")
        else:
            st.warning("Please fill in the Location Detail.")

    # View Locations
    st.write("###### Available Locations in Database")
    locations_data = get_locations()
    if locations_data:
        st.dataframe(locations_data)

        # Update Location
        st.write("###### Function to Update Location")
        loc_names = [f"{loc['loc_details']} (ID: {loc['loc_id']})" for loc in locations_data]
        loc_name_to_update = st.selectbox("Select Location to Update", options=loc_names)
        if loc_name_to_update:
            selected_loc_id = int(loc_name_to_update.split("(ID: ")[-1][:-1])
            new_loc_detail = st.text_input("New Location Detail")
            if st.button("Update Location"):
                if new_loc_detail:
                    update_location(selected_loc_id, new_loc_detail)
                    st.success(f"Updated Location ID: {selected_loc_id} with new detail: {new_loc_detail}")
                else:
                    st.warning("Please provide a new Location Detail.")

            # Delete Location
            if st.button("Delete Selected Location"):
                delete_location(selected_loc_id)
                st.success(f"Deleted Location ID: {selected_loc_id}")

    # Add Room
    st.write("###### Function to Add New Room")
    room_detail = st.text_input("Room Detail")
    if st.button("Add Room"):
        if room_detail:
            create_room(room_detail)
            st.success(f"Added Room: {room_detail}")
        else:
            st.warning("Please fill in the Room Detail.")

    # View Rooms
    st.write("###### Available Rooms in Database")
    rooms_data = get_rooms()
    if rooms_data:
        st.dataframe(rooms_data)

        # Update Room
        st.write("###### Function to Update Room")
        room_names = [f"{room['room_details']} (ID: {room['room_id']})" for room in rooms_data]
        room_name_to_update = st.selectbox("Select Room to Update", options=room_names)
        if room_name_to_update:
            selected_room_id = int(room_name_to_update.split("(ID: ")[-1][:-1])
            new_room_detail = st.text_input("New Room Detail")
            if st.button("Update Room"):
                if new_room_detail:
                    update_room(selected_room_id, new_room_detail)
                    st.success(f"Updated Room ID: {selected_room_id} with new detail: {new_room_detail}")
                else:
                    st.warning("Please provide a new Room Detail.")

            # Delete Room
            if st.button("Delete Selected Room"):
                delete_room(selected_room_id)
                st.success(f"Deleted Room ID: {selected_room_id}")

    # Add Maximum Pax
    st.write("###### Function to Add New Maximum Pax")
    max_pax_detail = st.text_input("Maximum Pax Detail")
    if st.button("Add Maximum Pax"):
        if max_pax_detail:
            create_maximum_pax(max_pax_detail)
            st.success(f"Added Maximum Pax: {max_pax_detail}")
        else:
            st.warning("Please fill in the Maximum Pax Detail.")

    # View Maximum Pax
    st.write("###### Available Maximum Pax in Database")
    max_pax_data = get_maximum_pax()
    if max_pax_data:
        st.dataframe(max_pax_data)

        # Update Maximum Pax
        st.write("###### Function to Update Maximum Pax")
        max_pax_names = [f"{max_pax['max_pax_details']} (ID: {max_pax['max_pax_id']})" for max_pax in max_pax_data]
        max_pax_name_to_update = st.selectbox("Select Maximum Pax to Update", options=max_pax_names)
        if max_pax_name_to_update:
            selected_max_pax_id = int(max_pax_name_to_update.split("(ID: ")[-1][:-1])
            new_max_pax_detail = st.text_input("New Maximum Pax Detail")
            if st.button("Update Maximum Pax"):
                if new_max_pax_detail:
                    update_maximum_pax(selected_max_pax_id, new_max_pax_detail)
                    st.success(f"Updated Maximum Pax ID: {selected_max_pax_id} with new detail: {new_max_pax_detail}")
                else:
                    st.warning("Please provide a new Maximum Pax Detail.")

            # Delete Maximum Pax
            if st.button("Delete Selected Maximum Pax"):
                delete_maximum_pax(selected_max_pax_id)
                st.success(f"Deleted Maximum Pax ID: {selected_max_pax_id}")

    # Add Cottage Type
    st.write("###### Function to Add New Cottage Type")
    ct_detail = st.text_input("Cottage Type Detail")
    if st.button("Add Cottage Type"):
        if ct_detail:
            create_cottage_type(ct_detail)
            st.success(f"Added Cottage Type: {ct_detail}")
        else:
            st.warning("Please fill in the Cottage Type Detail.")

    # View Cottage Types
    st.write("###### Available Cottage Types in Database")
    cottage_types_data = get_cottage_types()
    if cottage_types_data:
        st.dataframe(cottage_types_data)

        # Update Cottage Type
        st.write("###### Function to Update Cottage Type")
        ct_names = [f"{ct['ct_details']} (ID: {ct['ct_id']})" for ct in cottage_types_data]
        ct_name_to_update = st.selectbox("Select Cottage Type to Update", options=ct_names)
        if ct_name_to_update:
            selected_ct_id = int(ct_name_to_update.split("(ID: ")[-1][:-1])
            new_ct_detail = st.text_input("New Cottage Type Detail")
            if st.button("Update Cottage Type"):
                if new_ct_detail:
                    update_cottage_type(selected_ct_id, new_ct_detail)
                    st.success(f"Updated Cottage Type ID: {selected_ct_id} with new detail: {new_ct_detail}")
                else:
                    st.warning("Please provide a new Cottage Type Detail.")

            # Delete Cottage Type
            if st.button("Delete Selected Cottage Type"):
                delete_cottage_type(selected_ct_id)
                st.success(f"Deleted Cottage Type ID: {selected_ct_id}")

    # Add Cottage Status
    st.write("###### Function to Add New Cottage Status")
    cottage_status_detail = st.text_input("Cottage Status Detail")
    if st.button("Add Cottage Status"):
        if cottage_status_detail:
            create_cottage_status(cottage_status_detail)
            st.success(f"Added Cottage Status: {cottage_status_detail}")
        else:
            st.warning("Please fill in the Cottage Status Detail.")

    # View Cottage Statuses
    st.write("###### Available Cottage Statuses in Database")
    cottage_statuses_data = get_cottage_statuses()
    if cottage_statuses_data:
        st.dataframe(cottage_statuses_data)

        # Update Cottage Status
        st.write("###### Function to Update Cottage Status")
        cottage_status_names = [f"{status['ct_status_details']} (ID: {status['cottage_status_id']})" for status in cottage_statuses_data]
        cottage_status_name_to_update = st.selectbox("Select Cottage Status to Update", options=cottage_status_names)
        if cottage_status_name_to_update:
            selected_cottage_status_id = int(cottage_status_name_to_update.split("(ID: ")[-1][:-1])
            new_cottage_status_detail = st.text_input("New Cottage Status Detail")
            if st.button("Update Cottage Status"):
                if new_cottage_status_detail:
                    update_cottage_status(selected_cottage_status_id, new_cottage_status_detail)
                    st.success(f"Updated Cottage Status ID: {selected_cottage_status_id} with new detail: {new_cottage_status_detail}")
                else:
                    st.warning("Please provide a new Cottage Status Detail.")

            # Delete Cottage Status
            if st.button("Delete Selected Cottage Status"):
                delete_cottage_status(selected_cottage_status_id)
                st.success(f"Deleted Cottage Status ID: {selected_cottage_status_id}")

def show_cottage_management():
    """Streamlit UI for managing Cottages."""
    st.write("### Cottage Management 🏡")

    cottages = fetch_cottages_with_attributes()  # Fetch cottage data
    if cottages:
        st.write("###### Cottages with Attributes")
        st.dataframe(cottages)

        # Editing Cottage Attributes
        st.write("###### Edit Cottage Attributes")
        cottage_names = [f"{cottage['cottage_name']} (ID: {cottage['id']})" for cottage in cottages]
        selected_cottage = st.selectbox("Select Cottage to Edit", options=cottage_names)

        if selected_cottage:
            selected_cottage_id = int(selected_cottage.split("(ID: ")[-1][:-1])  # Extract cottage ID
            selected_cottage_data = next((cottage for cottage in cottages if cottage['id'] == selected_cottage_id), None)

            if selected_cottage_data:
                # Use text_input but validate or convert inputs
                new_pool_id = st.text_input("New Pool ID", value=selected_cottage_data['pool_id'])
                new_loc_id = st.text_input("New Location ID", value=selected_cottage_data['loc_id'])
                new_room_id = st.text_input("New Room ID", value=selected_cottage_data['room_id'])
                new_max_pax_id = st.text_input("New Maximum Pax ID", value=selected_cottage_data['max_pax_id'])
                new_ct_id = st.text_input("New Cottage Type ID", value=selected_cottage_data['ct_id'])
                new_ct_stat_id = st.text_input("New Cottage Status ID", value=selected_cottage_data['ct_id_stat'])

                if st.button("Update Cottage Attributes"):
                    # Ensure all inputs are valid before proceeding
                    try:
                        # Convert IDs to integers
                        new_pool_id = int(new_pool_id)
                        new_loc_id = int(new_loc_id)
                        new_room_id = int(new_room_id)
                        new_max_pax_id = int(new_max_pax_id)
                        new_ct_id = int(new_ct_id)
                        new_ct_stat_id = int(new_ct_stat_id)

                        edit_cottage_attributes(selected_cottage_id, new_pool_id, new_loc_id, new_room_id, new_max_pax_id, new_ct_id, new_ct_stat_id)
                        st.success(f"Updated attributes for Cottage ID: {selected_cottage_id}")
                    except ValueError:
                        st.error("Please ensure all ID fields are valid integers.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")


# Main application
def main():
    """Main application entry point."""
    st.title("Cottage Management System 🏠")
    menu = ["Facilities Management", "Cottage Management"]
    choice = st.sidebar.selectbox("Select Activity", menu)

    if choice == "Facilities Management":
        show_facilities_management()
    elif choice == "Cottage Management":
        show_cottage_management()

if __name__ == "__main__":
    main()
