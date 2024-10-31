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

def get_cottage_details(cot_id):
    """Fetch detailed information for a specific cottage."""
    if cot_id is None:
        st.error("Cottage ID is None.")
        return None
    
    query = """
        SELECT C.*, P.pool_detail, L.loc_details, R.room_details, M.max_pax_details, CT.ct_details, CS.ct_details AS status_details
        FROM COTTAGE C
        LEFT JOIN COTTAGE_ATTRIBUTES_RELATION CAR ON C.cot_id = CAR.cot_id
        LEFT JOIN POOL P ON CAR.pool_id = P.pool_id
        LEFT JOIN LOCATION L ON CAR.loc_id = L.loc_id
        LEFT JOIN ROOM R ON CAR.room_id = R.room_id
        LEFT JOIN MAXIMUM_PAX M ON CAR.max_pax_id = M.max_pax_id
        LEFT JOIN COTTAGE_TYPES CT ON CAR.ct_id = CT.ct_id
        LEFT JOIN COTTAGE_STATUS CS ON CAR.ct_id_stat = CS.cottage_status_id
        WHERE C.cot_id = %s
    """
    try:
        result = fetch_data(query, (cot_id,))
        if result:
            return result[0]  # Return the first result
        else:
            st.warning("No details found for the selected cottage.")
            return None
    except Error as e:
        st.error(f"Error fetching cottage details: {e}")
        return None

def delete_cottage(cot_id):
    """Delete a cottage by ID."""
    query = "DELETE FROM COTTAGE WHERE cot_id = %s"
    execute_query(query, (cot_id,))

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

def get_cottage_attributes(cottage_id):
    """Fetch attributes for a specific cottage."""
    query = """
        SELECT CAR.*, P.pool_detail, L.loc_details, R.room_details, M.max_pax_details, CT.ct_details, CS.ct_details AS status_details
        FROM COTTAGE_ATTRIBUTES_RELATION CAR
        LEFT JOIN POOL P ON CAR.pool_id = P.pool_id
        LEFT JOIN LOCATION L ON CAR.loc_id = L.loc_id
        LEFT JOIN ROOM R ON CAR.room_id = R.room_id
        LEFT JOIN MAXIMUM_PAX M ON CAR.max_pax_id = M.max_pax_id
        LEFT JOIN COTTAGE_TYPES CT ON CAR.ct_id = CT.ct_id
        LEFT JOIN COTTAGE_STATUS CS ON CAR.ct_id_stat = CS.cottage_status_id
        WHERE CAR.cot_id = %s
    """
    return fetch_data(query, (cottage_id,))

def show_cottage_management():
    """Streamlit UI for Cottage Management."""
    st.subheader("Cottage Management")

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

                # Show the attributes grid after adding attributes
                st.write("### Cottage Attributes Relation")
                attributes_data = get_cottage_attributes(selected_cottage_id)
                if attributes_data:
                    attributes_df = pd.DataFrame(attributes_data)
                    st.dataframe(attributes_df)  # Displaying the attributes in a grid
                else:
                    st.warning("No attributes found for the selected cottage.")

            else:
                st.warning("Please select a Cottage to add attributes.")

    # View Cottages
    st.write("### Cottage List")
    cottage_data = get_cottages()
    if cottage_data:
        # Display cottage list in a grid format
        cottage_df = pd.DataFrame(cottage_data)
        st.dataframe(cottage_df)  # Displaying the cottage list in a grid
    else:
        st.warning("No cottages found.")

# Call the show_cottage_management function to display the UI
if __name__ == "__main__":
    show_cottage_management()
