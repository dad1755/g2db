import streamlit as st
from db import load_data, save_data

def staff_role_section():
    """Main section to manage staff and roles."""
    st.header("Manage Staff and Roles")
    manage_roles()  # Role management
    manage_staff()  # Staff management

# Role Management
def manage_roles():
    """Display, add, update, and delete roles."""
    st.subheader("Manage Roles")
    
    # Load roles
    roles = load_data("SELECT * FROM Role")
    st.write("Roles:", roles)  # Displays roles in a readable format

    # Add Role
    new_role_name = st.text_input("New Role Name")
    if st.button("Add Role"):
        if new_role_name:
            save_data("INSERT INTO Role (role_name) VALUES (:role_name)", {"role_name": new_role_name})
            st.success("Role added successfully.")
            st.rerun()  # Refresh to display new role

    # Update/Delete Roles
    for role in roles:
        role_id = role['role_id']
        current_name = role['role_name']

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            new_name = st.text_input(f"Edit Role {role_id} Name", current_name, key=f"role_{role_id}")
        with col2:
            if st.button("Update", key=f"update_role_{role_id}"):
                save_data("UPDATE Role SET role_name = :new_name WHERE role_id = :role_id", 
                          {"new_name": new_name, "role_id": role_id})
                st.success("Role updated.")
                st.rerun()
        with col3:
            if st.button("Delete", key=f"delete_role_{role_id}"):
                save_data("DELETE FROM Role WHERE role_id = :role_id", {"role_id": role_id})
                st.success("Role deleted.")
                st.rerun()

# Staff Management
def manage_staff():
    """Display, add, update, and delete staff."""
    st.subheader("Manage Staff")

    # Load staff and roles
    staff_members = load_data("SELECT * FROM Staff")
    roles = load_data("SELECT * FROM Role")
    role_options = {role['role_id']: role['role_name'] for role in roles}

    st.write("Staff Members:", staff_members)

    # Add Staff
    new_staff_name = st.text_input("New Staff Name")
    new_staff_email = st.text_input("New Staff Email")
    new_staff_phone = st.text_input("New Staff Phone")
    new_staff_role_id = st.selectbox("Role", list(role_options.keys()), format_func=lambda x: role_options[x])
    
    if st.button("Add Staff"):
        if new_staff_name and new_staff_email and new_staff_phone:
            save_data("""
                INSERT INTO Staff (staff_name, staff_phone, staff_email, role_id)
                VALUES (:name, :phone, :email, :role_id)
            """, {"name": new_staff_name, "phone": new_staff_phone, "email": new_staff_email, "role_id": new_staff_role_id})
            st.success("Staff added successfully.")
            st.rerun()

    # Update/Delete Staff
    for staff in staff_members:
        staff_id = staff['staff_id']
        current_name = staff['staff_name']
        current_phone = staff['staff_phone']
        current_role = staff['role_id']

        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        with col1:
            new_name = st.text_input(f"Edit Staff {staff_id} Name", current_name, key=f"staff_name_{staff_id}")
        with col2:
            new_phone = st.text_input(f"Edit Phone {staff_id}", current_phone, key=f"staff_phone_{staff_id}")
        with col3:
            new_role_id = st.selectbox(f"Role for {staff_id}", list(role_options.keys()), 
                                       index=list(role_options.keys()).index(current_role), format_func=lambda x: role_options[x],
                                       key=f"staff_role_{staff_id}")
        
        with col4:
            if st.button("Update", key=f"update_staff_{staff_id}"):
                save_data("""
                    UPDATE Staff SET staff_name = :name, staff_phone = :phone, role_id = :role_id WHERE staff_id = :staff_id
                """, {"name": new_name, "phone": new_phone, "role_id": new_role_id, "staff_id": staff_id})
                st.success("Staff updated.")
                st.rerun()
        
            if st.button("Delete", key=f"delete_staff_{staff_id}"):
                save_data("DELETE FROM Staff WHERE staff_id = :staff_id", {"staff_id": staff_id})
                st.success("Staff deleted.")
                st.rerun()
