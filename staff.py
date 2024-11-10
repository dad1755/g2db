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

# SQLAlchemy engine for creating database connection
engine = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

def execute_query(query, params=None):
    """Execute a query with optional parameters."""
    try:
        with engine.connect() as connection:
            if params:
                connection.execute(text(query), params)  # Use parameterized queries
            else:
                connection.execute(text(query))
    except Exception as e:
        st.error(f"Error: {e}")

def fetch_data(query, params=None):
    """Fetch data from the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            rows = result.fetchall()
            return rows  # Return fetched rows
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Staff Management Functions
def create_staff(staff_name, role_id):
    """Create a new staff member."""
    query = "INSERT INTO STAFF (staff_name, role_id) VALUES (:staff_name, :role_id)"
    execute_query(query, {"staff_name": staff_name, "role_id": role_id})

def get_staff():
    """Fetch all staff members."""
    query = "SELECT * FROM STAFF"
    return fetch_data(query)

def get_roles():
    """Fetch all roles from the ROLES table."""
    query = "SELECT * FROM ROLES"
    roles = fetch_data(query)
    if roles is None:
        st.error("Failed to fetch roles from the database.")
    else:
        st.write("Roles retrieved successfully:", roles)
    return roles

def update_staff(staff_id, staff_name, role_id):
    """Update staff member information."""
    query = "UPDATE STAFF SET staff_name = :staff_name, role_id = :role_id WHERE staff_id = :staff_id"
    execute_query(query, {"staff_name": staff_name, "role_id": role_id, "staff_id": staff_id})

def delete_staff(staff_id):
    """Delete a staff member by ID."""
    query = "DELETE FROM STAFF WHERE staff_id = :staff_id"
    execute_query(query, {"staff_id": staff_id})

def create_role(role_name):
    """Create a new role."""
    query = "INSERT INTO ROLES (role_name) VALUES (:role_name)"
    try:
        execute_query(query, {"role_name": role_name})
        st.success(f"Added New Role: {role_name}")
    except Exception as e:
        st.error(f"Error adding role: {e}")

# Streamlit UI for Role Management
def show_role_management():
    """Streamlit UI for Role Management."""
    st.subheader("Role Management 👥")

    # Input field to add new role
    new_role_name = st.text_input("New Role Name")

    if st.button("Add Role"):
        if new_role_name:
            create_role(new_role_name)
            st.success(f"Added New Role: {new_role_name}")
        else:
            st.warning("Please enter a role name.")

# Streamlit UI for Staff Management
def show_staff_management():
    """Streamlit UI for Staff Management."""
    st.subheader("Staff Management 🎤")

    # Add Role Management section
    show_role_management()

    # Fetch available roles
    roles_data = get_roles()
    if not roles_data:
        st.warning("No roles available in the system. Please add roles first.")
        return

    # Display roles in the UI
    roles_dict = {role['role_id']: role['role_name'] for role in roles_data}

    # Add Staff
    st.write("###### Function To Add New Staff Member")
    staff_name = st.text_input("Staff Name")
    role_name = st.selectbox("Select Role", options=[role['role_name'] for role in roles_data])
    role_id = next((role['role_id'] for role in roles_data if role['role_name'] == role_name), None)

    if st.button("Add Staff"):
        if staff_name and role_id:
            create_staff(staff_name, role_id)
            st.success(f"Added Staff Member: {staff_name} with Role: {role_name}")
        else:
            st.warning("Please fill in the Staff Name and Role.")

    # View Staff
    st.write("###### Staff List Available in Database")
    staff_data = get_staff()
    if staff_data:
        st.dataframe(staff_data)

        # Prepare to update a staff member
        st.write("###### Update Existing Staff Member")
        staff_names = [f"{staff['staff_name']} (ID: {staff['staff_id']}, Role: {staff['role_id']})" for staff in staff_data]
        staff_name_to_update = st.selectbox("Select Staff Member to Update", options=staff_names)

        if staff_name_to_update:
            staff_id_to_update = int(staff_name_to_update.split("(ID: ")[-1].split(",")[0])
            selected_staff = next((staff for staff in staff_data if staff['staff_id'] == staff_id_to_update), None)

            if selected_staff:
                updated_name = st.text_input("Updated Name", value=selected_staff['staff_name'])
                updated_role_name = st.selectbox(
                    "Updated Role", options=[role['role_name'] for role in roles_data], index=list(roles_dict.values()).index(selected_staff['role_id'])
                )
                updated_role_id = next((role['role_id'] for role in roles_data if role['role_name'] == updated_role_name), None)

                if st.button("Update Staff"):
                    update_staff(staff_id_to_update, updated_name, updated_role_id)
                    st.success(f"Updated Staff Member: {updated_name} with Role: {updated_role_name}")

        # Prepare to delete a staff member
        st.write("###### Delete Staff Member")
        staff_name_to_delete = st.selectbox("Select Staff Member to Delete", options=staff_names)

        if st.button("Delete Staff"):
            if staff_name_to_delete:
                staff_id_to_delete = int(staff_name_to_delete.split("(ID: ")[-1].split(",")[0])
                delete_staff(staff_id_to_delete)
                st.success(f"Deleted Staff Member: {staff_name_to_delete}")
            else:
                st.warning("Please select a Staff Member to delete.")
    else:
        st.warning("No staff members found.")

# Call the show_staff_management function to display the UI
if __name__ == "__main__":
    show_staff_management()
