import streamlit as st
import mysql.connector
from mysql.connector import Error

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

# Cottage Management Functions
def create_cottage(cot_name):
    """Create a new cottage."""
    query = "INSERT INTO COTTAGE (cot_name) VALUES (%s)"
    execute_query(query, (cot_name,))  # Only pass cot_name

def create_cottage_with_attributes(cot_name, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat):
    """Create a new cottage and link it to its attributes."""
    create_cottage(cot_name)  # First, create the cottage
    cottage_id = get_last_insert_id()  # Get the last inserted ID for the cottage
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
    result = fetch_data(query, (cot_id,))
    return result[0] if result else None

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

def show_cottage_management():
    """Streamlit UI for Cottage Management."""
    st.subheader("Cottage Management")

    # Add Cottage
    st.write("### Add Cottage")
    cot_name = st.text_input("Cottage Name")

    # Fetch options for cottage attributes
    pool_options = get_pools()
    loc_options = get_locations()
    room_options = get_rooms()
    max_pax_options = get_maximum_pax()
    ct_options = get_cottage_types()
    ct_stat_options = get_cottage_statuses()

    # Selection boxes for cottage attributes
    pool_id = st.selectbox("Select Pool", [pool['pool_id'] for pool in pool_options])
    loc_id = st.selectbox("Select Location", [loc['loc_id'] for loc in loc_options])
    room_id = st.selectbox("Select Room", [room['room_id'] for room in room_options])
    max_pax_id = st.selectbox("Select Maximum Pax", [max_pax['max_pax_id'] for max_pax in max_pax_options])
    ct_id = st.selectbox("Select Cottage Type", [ct['ct_id'] for ct in ct_options])
    ct_id_stat = st.selectbox("Select Cottage Status", [cs['cottage_status_id'] for cs in ct_stat_options])

    if st.button("Add Cottage"):
        if cot_name:
            create_cottage_with_attributes(cot_name, pool_id, loc_id, room_id, max_pax_id, ct_id, ct_id_stat)
            st.success(f"Added Cottage: {cot_name}")
        else:
            st.warning("Please enter a Cottage Name.")

    # View Cottages
    st.write("### Cottage List")
    cottage_data = get_cottages()
    if cottage_data:
        selected_cottage_name = st.selectbox("Select a Cottage to View Details", options=[cottage['cot_name'] for cottage in cottage_data])
        
        # Fetch and display the selected cottage details
        if selected_cottage_name:
            selected_cottage_id = next(cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == selected_cottage_name)
            cottage_details = get_cottage_details(selected_cottage_id)

            if cottage_details:
                st.write("#### Cottage Details")
                st.write(f"**Cottage Name:** {cottage_details['cot_name']}")
                st.write(f"**Pool:** {cottage_details['pool_detail']}")
                st.write(f"**Location:** {cottage_details['loc_details']}")
                st.write(f"**Room Details:** {cottage_details['room_details']}")
                st.write(f"**Maximum Pax:** {cottage_details['max_pax_details']}")
                st.write(f"**Cottage Type:** {cottage_details['ct_details']}")
                st.write(f"**Cottage Status:** {cottage_details['status_details']}")

        # Prepare to delete a cottage
        st.write("### Delete Cottage")
        cottage_names = [cottage['cot_name'] for cottage in cottage_data]
        cot_name_to_delete = st.selectbox("Select Cottage to Delete", options=cottage_names)

        if st.button("Delete Cottage"):
            if cot_name_to_delete:
                cot_id_to_delete = next(cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == cot_name_to_delete)
                delete_cottage(cot_id_to_delete)
                st.success(f"Deleted Cottage: {cot_name_to_delete}")
            else:
                st.warning("Please select a Cottage to delete.")
    else:
        st.warning("No cottages found.")

# Call the show_cottage_management function to display the UI
if __name__ == "__main__":
    show_cottage_management()
