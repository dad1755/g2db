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

# CRUD Functions for Facilities
def create_facility(fac_detail):
    """Create a new facility."""
    query = "INSERT INTO FACILITIES (fac_detail) VALUES (%s)"
    execute_query(query, (fac_detail,))

def get_facilities():
    """Fetch all facilities."""
    query = "SELECT * FROM FACILITIES"
    return fetch_data(query) or []

def update_facility(fac_id, fac_detail):
    """Update facility information."""
    query = "UPDATE FACILITIES SET fac_detail = %s WHERE fac_id = %s"
    execute_query(query, (fac_detail, fac_id))

def delete_facility(fac_id):
    """Delete a facility by ID."""
    query = "DELETE FROM FACILITIES WHERE fac_id = %s"
    execute_query(query, (fac_id,))

def show_facilities_management():
    """Streamlit UI for Facility Management."""
    st.subheader("Facility Management")

    # Add Facility
    st.write("### Add Facility")
    fac_detail = st.text_input("Facility Detail")
    if st.button("Add Facility"):
        if fac_detail:
            create_facility(fac_detail)
            st.success(f"Added Facility: {fac_detail}")
        else:
            st.warning("Please fill in the Facility Detail.")

    # View Facilities
    st.write("### Facility List")
    facilities_data = get_facilities()
    if facilities_data:
        st.dataframe(facilities_data)

        # Prepare to update a facility
        st.write("### Update Facility")
        fac_names = [f"{facility['fac_detail']} (ID: {facility['fac_id']})" for facility in facilities_data]
        fac_name_to_update = st.selectbox("Select Facility to Update", options=fac_names)

        if fac_name_to_update:
            fac_id_to_update = int(fac_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
            selected_facility = next((facility for facility in facilities_data if facility['fac_id'] == fac_id_to_update), None)

            if selected_facility:
                updated_detail = st.text_input("Updated Detail", value=selected_facility['fac_detail'])

                if st.button("Update Facility"):
                    update_facility(fac_id_to_update, updated_detail)
                    st.success(f"Updated Facility: {updated_detail}")

        # Prepare to delete a facility
        st.write("### Delete Facility")
        fac_name_to_delete = st.selectbox("Select Facility to Delete", options=fac_names)

        if st.button("Delete Facility"):
            if fac_name_to_delete:
                fac_id_to_delete = int(fac_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                delete_facility(fac_id_to_delete)
                st.success(f"Deleted Facility: {fac_name_to_delete}")
            else:
                st.warning("Please select a Facility to delete.")
    else:
        st.warning("No facilities found.")
