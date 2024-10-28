import streamlit as st
from db import load_data, save_data

def staff_role_section():
    st.header("Manage Staff and Roles")

    manage_roles()
    manage_staff()

# Role Management
def manage_roles():
    st.subheader("Manage Roles")
    roles = load_data("SELECT * FROM Role")

    new_role_name = st.text_input("New Role Name")
    if st.button("Add Role"):
        if new_role_name:
            save_data("INSERT INTO Role (role_name) VALUES (:role_name)", {"role_name": new_role_name})
            st.success("Role added successfully.")

    for role in roles:
        st.write(f"Role ID: {role['role_id']}, Name: {role['role_name']}")
        new_name = st.text_input(f"Edit Name for Role {role['role_id']}", role['role_name'])
        
        if st.button("Update", key=f"update_role_{role['role_id']}"):
            save_data("UPDATE Role SET role_name = :new_name WHERE role_id = :role_id", 
                      {"new_name": new_name, "role_id": role['role_id']})
            st.success("Role updated.")
            
        if st.button("Delete", key=f"delete_role_{role['role_id']}"):
            save_data("DELETE FROM Role WHERE role_id = :role_id", {"role_id": role['role_id']})
            st.success("Role deleted.")

# Staff Management
def manage_staff():
    st.subheader("Manage Staff")
    staff_members = load_data("SELECT * FROM Staff")
    roles = load_data("SELECT * FROM Role")
    role_options = {role['role_id']: role['role_name'] for role in roles}

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

    for staff in staff_members:
        st.write(f"Staff ID: {staff['staff_id']}, Name: {staff['staff_name']}, Email: {staff['staff_email']}")
        
        new_name = st.text_input(f"Edit Name for Staff {staff['staff_id']}", staff['staff_name'])
        new_phone = st.text_input(f"Edit Phone for Staff {staff['staff_id']}", staff['staff_phone'])
        new_role_id = st.selectbox(f"Edit Role for Staff {staff['staff_id']}", list(role_options.keys()), 
                                   index=list(role_options.keys()).index(staff['role_id']), format_func=lambda x: role_options[x])
        
        if st.button("Update", key=f"update_staff_{staff['staff_id']}"):
            save_data("""
                UPDATE Staff SET staff_name = :name, staff_phone = :phone, role_id = :role_id WHERE staff_id = :staff_id
            """, {"name": new_name, "phone": new_phone, "role_id": new_role_id, "staff_id": staff['staff_id']})
            st.success("Staff updated.")
        
        if st.button("Delete", key=f"delete_staff_{staff['staff_id']}"):
            save_data("DELETE FROM Staff WHERE staff_id = :staff_id", {"staff_id": staff['staff_id']})
            st.success("Staff deleted.")
