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

# Roles Management Functions
def create_role(role_name):
    """Create a new role."""
    query = "INSERT INTO ROLES (role_name) VALUES (:role_name)"
    execute_query(query, {'role_name': role_name})

def get_roles():
    """Fetch all roles."""
    query = "SELECT * FROM ROLES"
    data = fetch_data(query)
    if data is None:
        return []  # Return an empty list
    return data

def update_role(role_id, role_name):
    """Update role information."""
    query = "UPDATE ROLES SET role_name = :role_name WHERE role_id = :role_id"
    execute_query(query, {'role_name': role_name, 'role_id': role_id})

def delete_role(role_id):
    """Delete a role by ID."""
    query = "DELETE FROM ROLES WHERE role_id = :role_id"
    execute_query(query, {'role_id': role_id})

def show_role_management():
    """Streamlit UI for Role Management."""
    st.subheader("Role Management 🧑‍💻")

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
    st.write("###### Roles List Available in Database")
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

# Call the show_role_management function to display the UI
if __name__ == "__main__":
    show_role_management()
