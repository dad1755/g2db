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

# Database Management Functions
def execute_query(query, params=None):
    """Execute a query with optional parameters."""
    try:
        with engine.connect() as connection:
            if params:
                connection.execute(text(query), params)  # Using parameterized queries is good for safety
            else:
                connection.execute(text(query))
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def fetch_data(query):
    """Fetch data from the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = result.fetchall()
            return rows  # Return fetched rows
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Role Management Functions
def create_role(role_name):
    """Create a new role."""
    query = "INSERT INTO ROLES (role_name) VALUES (%s)"
    execute_query(query, (role_name,))

def get_roles():
    """Fetch all roles."""
    query = "SELECT * FROM ROLES"
    return fetch_data(query)

def get_role_id_by_name(role_name):
    """Get role_id by role_name."""
    query = "SELECT role_id FROM ROLES WHERE role_name = %s"
    result = fetch_data(query)
    if result:
        return result[0]['role_id']
    return None

# Staff Management Functions (Modified to include role selection)
def create_staff(staff_name, role_id=None):
    """Create a new staff member with optional role."""
    query = "INSERT INTO STAFF (staff_name, role_id) VALUES (%s, %s)"
    execute_query(query, (staff_name, role_id))

def get_staff():
    """Fetch all staff members."""
    query = "SELECT * FROM STAFF"
    return fetch_data(query)

def update_staff(staff_id, staff_name, role_id=None):
    """Update staff member information and role."""
    query = "UPDATE STAFF SET staff_name = %s, role_id = %s WHERE staff_id = %s"
    execute_query(query, (staff_name, role_id, staff_id))

def delete_staff(staff_id):
    """Delete a staff member by ID."""
    query = "DELETE FROM STAFF WHERE staff_id = %s"
    execute_query(query, (staff_id,))

# Streamlit UI for Staff and Role Management
def show_staff_management():
    """Streamlit UI for Staff Management with Role Assignment."""
    st.subheader("Staff Management 🎤")

    # Add Staff
    st.write("###### Function To Add New Staff Member")
    staff_name = st.text_input("Staff Name")
    roles = get_roles()  # Fetch available roles
    role_options = [role['role_name'] for role in roles]
    role_name = st.selectbox("Select Role", options=role_options)

    if st.button("Add Staff"):
        if staff_name and role_name:
            role_id = get_role_id_by_name(role_name)  # Get the role ID based on the selected role
            create_staff(staff_name, role_id)
            st.success(f"Added Staff Member: {staff_name} with Role: {role_name}")
        else:
            st.warning("Please fill in the Staff Name and select a Role.")

    # View Staff
    st.write("###### Staff List Available in Database")
    staff_data = get_staff()
    if staff_data:
        st.dataframe(staff_data)

        # Prepare to update and delete staff members side by side
        st.write("###### Update or Delete Existing Staff Member")
        staff_names = [f"{staff['staff_name']} (ID: {staff['staff_id']})" for staff in staff_data]  # Use staff_name

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
                    current_role_id = selected_staff['role_id']
                    roles_for_select = {role['role_id']: role['role_name'] for role in roles}
                    updated_role_name = st.selectbox("Updated Role", options=roles_for_select.values(), index=list(roles_for_select.values()).index(next((role['role_name'] for role in roles if role['role_id'] == current_role_id), None)))

                    updated_role_id = get_role_id_by_name(updated_role_name)

                    if st.button("Update Staff"):
                        update_staff(staff_id_to_update, updated_name, updated_role_id)
                        st.success(f"Updated Staff Member: {updated_name} to Role: {updated_role_name}")

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

def show_role_management():
    """Streamlit UI for Role Management."""
    st.subheader("Role Management 🛠️")

    # Add Role
    st.write("###### Function To Add New Role")
    role_name = st.text_input("Role Name")
    if st.button("Add Role"):
        if role_name:
            create_role(role_name)
            st.success(f"Added Role: {role_name}")
        else:
            st.warning("Please fill in the Role Name.")

# Call the show_role_management and show_staff_management functions to display the UI
if __name__ == "__main__":
    show_role_management()
    show_staff_management()
