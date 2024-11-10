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

# Staff and Role Management Functions
def create_role(role_name):
    """Create a new role."""
    query = "INSERT INTO Roles (role_name) VALUES (%s)"
    execute_query(query, (role_name,))

def get_roles():
    """Fetch all roles."""
    query = "SELECT * FROM Roles"
    return fetch_data(query)

def assign_role_to_staff(staff_id, role_id):
    """Assign a role to a staff member."""
    query = "INSERT INTO StaffRoles (staff_id, role_id) VALUES (%s, %s)"
    execute_query(query, (staff_id, role_id))

def get_staff_with_roles():
    """Fetch staff members with their roles."""
    query = """
    SELECT s.staff_id, s.staff_name, r.role_name
    FROM STAFF s
    JOIN StaffRoles sr ON s.staff_id = sr.staff_id
    JOIN Roles r ON r.role_id = sr.role_id
    """
    return fetch_data(query)

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
                staff_id_to_update = int(staff_name_to_update.split("(ID: ")[-1][:-1])
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
                    staff_id_to_delete = int(staff_name_to_delete.split("(ID: ")[-1][:-1])
                    delete_staff(staff_id_to_delete)
                    st.success(f"Deleted Staff Member: {staff_name_to_delete}")
                else:
                    st.warning("Please select a Staff Member to delete.")

    else:
        st.warning("No staff members found.")

    # Role Management
    st.subheader("Role Management 👑")

    # Add Role
    role_name = st.text_input("New Role Name")
    if st.button("Add Role"):
        if role_name:
            create_role(role_name)
            st.success(f"Added Role: {role_name}")
        else:
            st.warning("Please fill in the Role Name.")

    # Assign Role to Staff
    st.write("###### Assign Role to Staff Member")
    roles = get_roles()
    staff_with_roles = get_staff()

    if roles and staff_with_roles:
        staff_names_with_ids = [f"{staff['staff_name']} (ID: {staff['staff_id']})" for staff in staff_with_roles]
        role_names = [role['role_name'] for role in roles]

        staff_to_assign_role = st.selectbox("Select Staff Member", staff_names_with_ids)
        role_to_assign = st.selectbox("Select Role", role_names)

        if st.button("Assign Role"):
            staff_id = int(staff_to_assign_role.split("(ID: ")[-1][:-1])
            role_id = next(role['role_id'] for role in roles if role['role_name'] == role_to_assign)
            assign_role_to_staff(staff_id, role_id)
            st.success(f"Assigned Role '{role_to_assign}' to {staff_to_assign_role}")

    # View Staff with Roles
    st.write("###### View Staff with Assigned Roles")
    staff_with_roles_data = get_staff_with_roles()
    if staff_with_roles_data:
        st.dataframe(staff_with_roles_data)
    else:
        st.warning("No staff with roles found.")

# Call the show_staff_management function to display the UI
if __name__ == "__main__":
    show_staff_management()
