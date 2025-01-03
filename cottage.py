import os
import streamlit as st
import pandas as pd
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text

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

def execute_query(query, params=None):
    """Execute a query with optional parameters using SQLAlchemy."""
    try:
        with engine.connect() as connection:
            if params:
                result = connection.execute(text(query), params)
            else:
                result = connection.execute(text(query))
            connection.commit()
            return result.rowcount
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def fetch_data(query, params=None):
    """Fetch data from the database with optional parameters using SQLAlchemy."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            rows = result.fetchall()
            # Convert results to a list of dictionaries for easy handling
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Database Query Functions
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
    
            # Fetch options for dropdowns
            pools = get_pools()
            locations = get_locations()
            rooms = get_rooms()
            maximum_pax = get_maximum_pax()
            cottage_types = get_cottage_types()
            cottage_statuses = get_cottage_statuses()
    
           # Create input fields for attributes
            #pool_id = st.selectbox("Pool", options=[f"{pool['pool_id']} : {pool['pool_detail']}" for pool in pools], index=0)
           #loc_id = st.selectbox("Location", options=[f"{location['loc_id']} : {location['loc_details']}" for location in locations], index=0)
           # room_id = st.selectbox("Room", options=[f"{room['room_id']} : {room['room_details']}" for room in rooms], index=0)
           # max_pax_id = st.selectbox("Max Pax", options=[f"{max_pax['max_pax_id']} : {max_pax['max_pax_details']}" for max_pax in maximum_pax], index=0)
           # ct_id = st.selectbox("Cottage Type", options=[f"{ct['ct_id']} : {ct['ct_details']}" for ct in cottage_types], index=0)
           # ct_id_stat = st.selectbox("Cottage Status", options=[f"{cs['cottage_status_id']} : {cs['ct_status_details']}" for cs in cottage_status], index=0)
            # Create input fields for attributes
            if pools:
                pool_options = [f"{pool['pool_id']} : {pool['pool_detail']}" for pool in pools]
                current_pool_index = next((i for i, pool in enumerate(pools) if pool['pool_id'] == current_attributes['pool_id']), 0)
                pool_id = st.selectbox("Pool", options=pool_options, index=current_pool_index)
            
            if locations:
                loc_options = [f"{location['loc_id']} : {location['loc_details']}" for location in locations]
                current_loc_index = next((i for i, loc in enumerate(locations) if loc['loc_id'] == current_attributes['loc_id']), 0)
                loc_id = st.selectbox("Location", options=loc_options, index=current_loc_index)
            
            if rooms:
                room_options = [f"{room['room_id']} : {room['room_details']}" for room in rooms]
                current_room_index = next((i for i, room in enumerate(rooms) if room['room_id'] == current_attributes['room_id']), 0)
                room_id = st.selectbox("Room", options=room_options, index=current_room_index)
            
            if maximum_pax:
                max_pax_options = [f"{max_pax['max_pax_id']} : {max_pax['max_pax_details']}" for max_pax in maximum_pax]
                current_max_pax_index = next((i for i, pax in enumerate(maximum_pax) if pax['max_pax_id'] == current_attributes['max_pax_id']), 0)
                max_pax_id = st.selectbox("Max Pax", options=max_pax_options, index=current_max_pax_index)
            
            if cottage_types:
                ct_options = [f"{ct['ct_id']} : {ct['ct_details']}" for ct in cottage_types]
                current_ct_index = next((i for i, ct in enumerate(cottage_types) if ct['ct_id'] == current_attributes['ct_id']), 0)
                ct_id = st.selectbox("Cottage Type", options=ct_options, index=current_ct_index)
            
            # Cottage Status
            if cottage_statuses:
                current_status_index = next((i for i, cs in enumerate(cottage_statuses) if cs['cottage_status_id'] == current_attributes['ct_id_stat']), 0)
                ct_id_stat = st.selectbox(
                    "Cottage Status", 
                    options=[f"{cs['cottage_status_id']} : {cs['ct_status_details']}" for cs in cottage_statuses], 
                    index=current_status_index
                )

        if st.button("Update Attributes"):
            update_cottage_attributes(selected_cottage_id, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat)
            st.success("Cottage attributes updated successfully.")
            st.rerun()  # Optionally rerun to refresh the UI after the update
    else:
            st.warning("No attributes found for the selected cottage.")




# Run the application
if __name__ == "__main__":
    show_cottage_management()
