import os
import streamlit as st
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

# SQLAlchemy engine for creating a database connection
engine = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Function to execute queries
def execute_query(query, params=None):
    """Execute a query with optional parameters."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            return result
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to fetch data from the database
def fetch_data(query):
    """Fetch data from the database."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            return rows  # Return fetched rows
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Staff Management Functions
def create_staff(staff_name):
    """Create a new staff member."""
    query = "INSERT INTO STAFF (staff_name) VALUES (:staff_name)"
    execute_query(query, {'staff_name': staff_name})

def get_staff():
    """Fetch all staff members."""
    query = "SELECT * FROM STAFF"
    data = fetch_data(query)
    if data is None:
        return []  # Return an empty list
    return data

def update_staff(staff_id, staff_name):
    """Update staff member information."""
    query = "UPDATE STAFF SET staff_name = :staff_name WHERE staff_id = :staff_id"
    execute_query(query, {'staff_name': staff_name, 'staff_id': staff_id})

def delete_staff(staff_id):
    """Delete a staff member by ID."""
    query = "DELETE FROM STAFF WHERE staff_id = :staff_id"
    execute_query(query, {'staff_id': staff_id})

def show_staff_management():
    """Streamlit UI for Staff Management."""
    st.subheader("Staff Management 🎤")

    # Add Staff
    st.write("###### Function To Add New Staff Member")
    staff_name = st.text_input("Staff Name")
    if st.button("Add Staff"):
        if staff_name:
            create_staff(staff_name)
            st.success(f"Added Staff Member: {staff_name}")
        else:
            st.warning("Please fill in the Staff Name.")

    # View Staff
    st.write("###### Staff List Available in Database")
    staff_data = get_staff()
    if staff_data:
        st.dataframe(staff_data)

        # Prepare to update and delete staff members side by side
        st.write("###### Update or Delete Existing Staff Member")
        staff_names = [f"{staff['staff_name']} (ID: {staff['staff_id']})" for staff in staff_data]

        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Update Existing Staff Member**")
            staff_name_to_update = st.selectbox("Select Staff Member to Update", options=staff_names)

            if staff_name_to_update:
                staff_id_to_update = int(staff_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
                selected_staff = next((staff for staff in staff_data if staff['staff_id'] == staff_id_to_update), None)

                if selected_staff:
                    updated_name = st.text_input("Updated Name", value=selected_staff['staff_name'])

                    if st.button("Update Staff"):
                        update_staff(staff_id_to_update, updated_name)
                        st.success(f"Updated Staff Member: {updated_name}")

        with col2:
            st.write("**Delete Staff Member**")
            staff_name_to_delete = st.selectbox("Select Staff Member to Delete", options=staff_names)

            if st.button("Delete Staff"):
                if staff_name_to_delete:
                    staff_id_to_delete = int(staff_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                    delete_staff(staff_id_to_delete)
                    st.success(f"Deleted Staff Member: {staff_name_to_delete}")
                else:
                    st.warning("Please select a Staff Member to delete.")
    else:
        st.warning("No staff members found.")

# Call the show_staff_management function to display the UI
if __name__ == "__main__":
    show_staff_management()
