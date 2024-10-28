import streamlit as st
from sqlalchemy import create_engine, text

# Database connection setup
DATABASE_URL = "mysql+mysqlconnector://sql12741294:Lvu9cg9kGm@sql12.freemysqlhosting.net:3306/sql12741294"
engine = create_engine(DATABASE_URL)

# Load data function
def load_data(query, parameters=None):
    with engine.connect() as connection:
        result = connection.execute(text(query), parameters or {})
        return [dict(row) for row in result]

# Save data function
def save_data(query, parameters=None):
    with engine.connect() as connection:
        connection.execute(text(query), parameters or {})

def staff_role_section():
    st.header("Manage Staff and Roles")

    manage_roles()
    manage_staff()

# Role Management
def manage_roles():
    st.subheader("Manage Roles")

    # Function to fetch roles from the database
    def fetch_roles():
        roles = load_data("SELECT * FROM Role")
        print("Fetched Roles:", roles)  # Debugging line
        return roles

    # Load roles initially
    roles = fetch_roles()
    
    # Add Role
    new_role_name = st.text_input("New Role Name")
    if st.button("Add Role"):
        if new_role_name:
            save_data("INSERT INTO Role (role_name) VALUES (:role_name)", {"role_name": new_role_name})
            st.success("Role added successfully.")
            roles = fetch_roles()  # Re-fetch roles to update the display
            print("Roles after adding:", roles)  # Debugging line

    # Display roles
    if roles:
        st.write("Available Roles:")
        for role in roles:
            st.write(f"Role ID: {role['role_id']}, Name: {role['role_name']}")
    else:
        st.write("No roles found.")

    # Update/Delete Roles
    for role in roles:
        role_id = role['role_id']
        current_name = role['role_name']

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            new_name = st.text_input(f"Edit Role {role_id} Name", current_name, key=f"role_{role_id}")
        with col2:
            if st.button("Update", key=f"update_role_{role_id}"):
                if new_name and new_name != current_name:
                    save_data("UPDATE Role SET role_name = :new_name WHERE role_id = :role_id", 
                              {"new_name": new_name, "role_id": role_id})
                    st.success("Role updated.")
                    roles = fetch_roles()  # Refresh roles after updating
                    print("Roles after updating:", roles)  # Debugging line
        with col3:
            if st.button("Delete", key=f"delete_role_{role_id}"):
                save_data("DELETE FROM Role WHERE role_id = :role_id", {"role_id": role_id})
                st.success("Role deleted.")
                roles = fetch_roles()  # Refresh roles after deleting
                print("Roles after deleting:", roles)  # Debugging line

# Staff Management (if needed, you can implement this similarly)
def manage_staff():
    st.subheader("Manage Staff")
    # Staff management logic will go here (not fully implemented in this example)

# Run the application
if __name__ == "__main__":
    staff_role_section()
