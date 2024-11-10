import os
import streamlit as st
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text
import pymysql

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

# Streamlit app configuration
def execute_query(query, params=None):
    """Execute a query with optional parameters."""
    try:
        with engine.connect() as connection:
            if params:
                connection.execute(text(query), params)  # Using parameterized queries for safety
            else:
                connection.execute(text(query))
            return True  # Successful execution
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def fetch_data(query, params=None):
    """Fetch data from the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            rows = result.fetchall()  # Fetch all rows
            return rows  # Return fetched rows
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Staff Management Functions
def create_staff(staff_name):
    """Create a new staff member."""
    query = "INSERT INTO STAFF (staff_name) VALUES (:staff_name)"  # Use :staff_name as a placeholder
    execute_query(query, {'staff_name': staff_name})

def get_staff():
    """Fetch all staff members."""
    query = "SELECT * FROM STAFF"
    data = fetch_data(query)
    if data is None:
        return []  # Return an empty list if no data is found
    return data

def update_staff(staff_id, staff_name):
    """Update staff member information."""
    query = "UPDATE STAFF SET staff_name = :staff_name WHERE staff_id = :staff_id"
    execute_query(query, {'staff_name': staff_name, 'staff_id': staff_id})

def delete_staff(staff_id):
    """Delete a staff member by ID."""
    query = "DELETE FROM STAFF WHERE staff_id = :staff_id"
    execute_query(query, {'staff_id': staff_id})

# Role Management Functions
def create_role(role_name):
    """Create a new role."""
    query = "INSERT INTO ROLES (role_name) VALUES (:role_name)"
    execute_query(query, {'role_name': role_name})

def get_roles():
    """Fetch all roles."""
    query = "SELECT * FROM ROLES"
    data = fetch_data(query)
    if data is None:
        return []  # Return an empty list if no data is found
    return data

def update_role(role_id, role_name):
    """Update role name."""
    query = "UPDATE ROLES SET role_name = :role_name WHERE role_id = :role_id"
    execute_query(query, {'role_name': role_name, 'role_id': role_id})

def delete_role(role_id):
    """Delete a role by ID."""
    query = "DELETE FROM ROLES WHERE role_id = :role_id"
    execute_query(query, {'role_id': role_id})

def assign_role_to_staff(staff_id, role_id):
    """Assign a role to a staff member."""
    query = "UPDATE STAFF SET role_id = :role_id WHERE staff_id = :staff_id"
    execute_query(query, {'staff_id': staff_id, 'role_id': role_id})

# Streamlit UI to manage staff
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
                    updated_name = st.text_input("Updated Name", value=selected_staff['staff_name'])  # Use staff_name

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

# Streamlit UI to manage roles
def show_role_management():
    """Streamlit UI for Role Management."""
    st.subheader("Role Management 🔑")

    # Add Role
    st.write("###### Function To Add New Role")
    role_name = st.text_input("Role Name")
    if st.button("Add Role"):
        if role_name:
            create_role(role_name)
            st.success(f"Added Role: {role_name}")
        else:
            st.warning("Please fill in the Role Name.")

    # View Roles
    st.write("###### Roles Available in Database")
    role_data = get_roles()
    if role_data:
        st.dataframe(role_data)

        # Prepare to update and delete roles side by side
        st.write("###### Update or Delete Existing Role")
        role_names = [f"{role['role_name']} (ID: {role['role_id']})" for role in role_data]

        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Update Existing Role**")
            role_name_to_update = st.selectbox("Select Role to Update", options=role_names)

            if role_name_to_update:
                role_id_to_update = int(role_name_to_update.split("(ID: ")[-1][:-1])  # Extract ID
                selected_role = next((role for role in role_data if role['role_id'] == role_id_to_update), None)

                if selected_role:
                    updated_name = st.text_input("Updated Name", value=selected_role['role_name'])

                    if st.button("Update Role"):
                        update_role(role_id_to_update, updated_name)
                        st.success(f"Updated Role: {updated_name}")

        with col2:
            st.write("**Delete Role**")
            role_name_to_delete = st.selectbox("Select Role to Delete", options=role_names)

            if st.button("Delete Role"):
                if role_name_to_delete:
                    role_id_to_delete = int(role_name_to_delete.split("(ID: ")[-1][:-1])  # Extract ID
                    delete_role(role_id_to_delete)
                    st.success(f"Deleted Role: {role_name_to_delete}")
                else:
                    st.warning("Please select a Role to delete.")
    else:
        st.warning("No roles found.")

# Streamlit UI to assign roles to staff
def show_assign_role_to_staff():
    """Streamlit UI for assigning roles to staff."""
    st.subheader("Assign Role to Staff 👥")

    # Get staff and roles
    staff_data = get_staff()
    role_data = get_roles()

    if staff_data and role_data:
        staff_names = [f"{staff['staff_name']} (ID: {staff['staff_id']})" for staff in staff_data]
        role_names = [f"{role['role_name']} (ID: {role['role_id']})" for role in role_data]

        # Allow user to select staff member and role
        staff_name_to_assign = st.selectbox("Select Staff Member", options=staff_names)
        role_name_to_assign = st.selectbox("Select Role", options=role_names)

        if st.button("Assign Role"):
            if staff_name_to_assign and role_name_to_assign:
                staff_id_to_assign = int(staff_name_to_assign.split("(ID: ")[-1][:-1])  # Extract Staff ID
                role_id_to_assign = int(role_name_to_assign.split("(ID: ")[-1][:-1])  # Extract Role ID
                assign_role_to_staff(staff_id_to_assign, role_id_to_assign)
                st.success(f"Assigned Role: {role_name_to_assign} to Staff Member: {staff_name_to_assign}")
            else:
                st.warning("Please select both Staff Member and Role.")
    else:
        st.warning("No staff members or roles found.")

# Combine the functions to display role management and staff-role assignment
def show_staff_and_role_management():
    """Streamlit UI for Staff and Role Management."""
    show_staff_management()
    show_role_management()
    show_assign_role_to_staff()

# Call the function to display the UI
if __name__ == "__main__":
    show_staff_and_role_management()
