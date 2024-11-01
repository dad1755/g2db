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

def create_cottage(cot_name, cot_price):
    """Create a new cottage with a name and price."""
    query = "INSERT INTO COTTAGE (cot_name, cot_price) VALUES (%s, %s)"
    execute_query(query, (cot_name, cot_price))

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

def delete_cottage(cot_id):
    """Delete a cottage, its attributes, and associated discounts."""
    
    # Step 1: Get the cottage name for the given cottage ID
    get_cottage_name_query = "SELECT cot_name FROM COTTAGE WHERE cot_id = %s"
    cottage_name_result = fetch_data(get_cottage_name_query, (cot_id,))
    
    if not cottage_name_result:
        st.warning(f"Cottage with ID {cot_id} does not exist.")
        return

    cottage_name = cottage_name_result[0]['cot_name']  # Extract the cottage name

    # Step 2: Delete discounts related to this cottage
    delete_discounts_query = "DELETE FROM DISCOUNT WHERE cot_id = %s"
    discount_count = execute_query(delete_discounts_query, (cot_id,))
    
    if discount_count:
        st.success(f"Deleted {discount_count} discount(s) associated with cottage '{cottage_name}'.")
    else:
        st.info(f"No discounts found for cottage '{cottage_name}'.")

    # Step 3: Delete attributes related to the cottage
    delete_attributes_query = "DELETE FROM COTTAGE_ATTRIBUTES_RELATION WHERE cot_id = %s"
    execute_query(delete_attributes_query, (cot_id,))

    # Step 4: Delete the cottage itself
    delete_cottage_query = "DELETE FROM COTTAGE WHERE cot_id = %s"
    execute_query(delete_cottage_query, (cot_id,))
    
    st.success(f"Cottage '{cottage_name}' with ID {cot_id} and its related data have been deleted.")
    st.rerun()





def edit_cottage(cottage_id, new_name):
    """Edit an existing cottage's name."""
    query = "UPDATE COTTAGE SET cot_name = %s WHERE cot_id = %s"
    execute_query(query, (new_name, cottage_id))

def edit_cottage(cottage_id, new_name, new_price):
    """Edit an existing cottage's name and price."""
    query = "UPDATE COTTAGE SET cot_name = %s, cot_price = %s WHERE cot_id = %s"
    execute_query(query, (new_name, new_price, cottage_id))


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
    if result and 'LAST_INSERT_ID()' in result[0]:
        return result[0]['LAST_INSERT_ID()']
    return None


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
def cottage_has_attributes(cot_id):
    """Check if a cottage has existing attributes."""
    query = "SELECT COUNT(*) as count FROM COTTAGE_ATTRIBUTES_RELATION WHERE cot_id = %s"
    result = fetch_data(query, (cot_id,))
    return result[0]['count'] > 0 if result else False

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

    # Add Cottage
    st.write("###### Function To Add New Cottage")
    cot_name = st.text_input("Cottage Name")
    cot_price = st.number_input("Cottage Price", min_value=0.0, step=0.01)  # Input for price
    if st.button("Create Cottage"):
        if cot_name and cot_price:
            create_cottage(cot_name, cot_price)
            cottage_id = get_last_insert_id()
            st.success(f"Added Cottage: {cot_name} (ID: {cottage_id})")
            st.rerun()
        else:
            st.warning("Please enter both Cottage Name and Price.")

    # Edit Cottage
    st.write("###### Function To Add Facilities To Cottage")
    if cottage_data:
        selected_cottage_name = st.selectbox("Select a Cottage to Edit", 
                                             options=[cottage['cot_name'] for cottage in cottage_data])
        selected_cottage_id = next((cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == selected_cottage_name), None)
        new_cot_name = st.text_input("New Cottage Name")
        new_cot_price = st.number_input("New Cottage Price", min_value=0.0, step=0.01)  # Input for new price
        
        if st.button("Update Cottage"):
            if new_cot_name and new_cot_price:
                edit_cottage(selected_cottage_id, new_cot_name, new_cot_price)  # Update to include price
                st.success(f"Updated Cottage to: {new_cot_name} with price: {new_cot_price}")
            else:
                st.warning("Please enter a new Cottage Name and Price.")

        if st.button("Delete Cottage"):
            delete_cottage(selected_cottage_id)
            st.success(f"Deleted Cottage: {selected_cottage_name}")
            st.rerun()

   
    # Cottage Attributes
    st.write("###### Cottage Attributes@Facilities, Please Refer To Next Tab For Details")
    cottage_attributes_data = get_cottage_attributes_relation()
    if cottage_attributes_data:
        attributes_df = pd.DataFrame(cottage_attributes_data)
        st.dataframe(attributes_df)  # Display the attributes in a grid format
    else:
        st.warning("No cottage attributes found. ----> VIEW GRID HERE")
        # Create an empty DataFrame for display
        empty_df = pd.DataFrame(columns=["cot_id", "pool_id", "loc_id", "room_id", "max_pax_id", "ct_id", "ct_id_stat"])
        st.dataframe(empty_df)  # Display an empty grid for better UX
    
    # Add Cottage Attributes
    st.write("### Add Attributes for Cottage")
    if cottage_data:
        selected_cottage_name = st.selectbox("Select a Cottage to Add Attributes", 
                                             options=[cottage['cot_name'] for cottage in cottage_data], key="cottage_select")
        selected_cottage_id = next((cottage['cot_id'] for cottage in cottage_data if cottage['cot_name'] == selected_cottage_name), None)
    
        # Check if the cottage already has attributes
        if cottage_has_attributes(selected_cottage_id):
            st.warning(f"The cottage '{selected_cottage_name}' already has attributes. You can edit them instead.")
            
            # Fetch existing attributes for editing
            existing_attributes_query = "SELECT * FROM COTTAGE_ATTRIBUTES_RELATION WHERE cot_id = %s"
            existing_attributes = fetch_data(existing_attributes_query, (selected_cottage_id,))
            
            if existing_attributes:
                attr = existing_attributes[0]  # Assuming one-to-one relationship for attributes
                pool_id = attr['pool_id']
                loc_id = attr['loc_id']
                room_id = attr['room_id']
                max_pax_id = attr['max_pax_id']
                ct_id = attr['ct_id']
                ct_id_stat = attr['ct_id_stat']
                
                # Select attribute options for editing
                pool_options = get_pools()
                loc_options = get_locations()
                room_options = get_rooms()
                max_pax_options = get_maximum_pax()
                ct_options = get_cottage_types()
                ct_stat_options = get_cottage_statuses()
    
                # Select attribute options with current values pre-filled
                pool_selection = st.selectbox("Select Pool", options=[f"{pool['pool_id']}: {pool['pool_detail']}" for pool in pool_options], index=next(i for i, pool in enumerate(pool_options) if pool['pool_id'] == pool_id))
                loc_selection = st.selectbox("Select Location", options=[f"{loc['loc_id']}: {loc['loc_details']}" for loc in loc_options], index=next(i for i, loc in enumerate(loc_options) if loc['loc_id'] == loc_id))
                room_selection = st.selectbox("Select Room", options=[f"{room['room_id']}: {room['room_details']}" for room in room_options], index=next(i for i, room in enumerate(room_options) if room['room_id'] == room_id))
                max_pax_selection = st.selectbox("Select Maximum Pax", options=[f"{max_pax['max_pax_id']}: {max_pax['max_pax_details']}" for max_pax in max_pax_options], index=next(i for i, max_pax in enumerate(max_pax_options) if max_pax['max_pax_id'] == max_pax_id))
                ct_selection = st.selectbox("Select Cottage Type", options=[f"{ct['ct_id']}: {ct['ct_details']}" for ct in ct_options], index=next(i for i, ct in enumerate(ct_options) if ct['ct_id'] == ct_id))
                ct_stat_selection = st.selectbox("Select Cottage Status", options=[f"{ct_stat['cottage_status_id']}: {ct_stat['ct_details']}" for ct_stat in ct_stat_options], index=next(i for i, ct_stat in enumerate(ct_stat_options) if ct_stat['cottage_status_id'] == ct_id_stat))
    
                if st.button("Update Attributes"):
                    new_pool_id = pool_selection.split(":")[0]
                    new_loc_id = loc_selection.split(":")[0]
                    new_room_id = room_selection.split(":")[0]
                    new_max_pax_id = max_pax_selection.split(":")[0]
                    new_ct_id = ct_selection.split(":")[0]
                    new_ct_stat_id = ct_stat_selection.split(":")[0]
                    
                    edit_cottage_attributes(selected_cottage_id, new_pool_id, new_loc_id, new_room_id, new_max_pax_id, new_ct_id, new_ct_stat_id)
                    st.success(f"Updated attributes for Cottage ID: {selected_cottage_id}")
    
        else:
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
