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

    # Display roles in a table format for easier readability
    if roles:
        st.table([{"Role ID": role['role_id'], "Name": role['role_name']} for role in roles])
    else:
        st.write("No roles found.")

    # Adding new role
    new_role_name = st.text_input("New Role Name")
    if st.button("Add Role") and new_role_name:
        save_data("INSERT INTO Role (role_name) VALUES (:role_name)", {"role_name": new_role_name})
        st.success("Role added successfully.")
        st.rerun()  # Refreshes to show the new role

    for role in roles:
        # Role update fields
        new_name = st.text_input(f"Edit Name for Role {role['role_id']}", role['role_name'], key=f"edit_role_{role['role_id']}")
        
        # Update button
        if st.button("Update", key=f"update_role_{role['role_id']}"):
            save_data("UPDATE Role SET role_name = :new_name WHERE role_id = :role_id", 
                      {"new_name": new_name, "role_id": role['role_id']})
            st.success("Role updated.")
            st.experimental_rerun()  # Refreshes to show updated data
            
        # Delete button
        if st.button("Delete", key=f"delete_role_{role['role_id']}"):
            save_data("DELETE FROM Role WHERE role_id = :role_id", {"role_id": role['role_id']})
            st.success("Role deleted.")
            st.rerun()  # Refreshes to show deletion

# Staff Management
def manage_staff():
    st.subheader("Manage Staff")
    staff_members = load_data("SELECT * FROM Staff")
    roles = load_data("SELECT * FROM Role")
    role_options = {role['role_id']: role['role_name'] for role in roles}

    # Display staff in a table format
    if staff_members:
        st.table([{"Staff ID": staff['staff_id'], "Name": staff['staff_name'], "Email": staff['staff_email'], 
                   "Phone": staff['staff_phone'], "Role": role_options.get(staff['role_id'], "Unknown")}
                  for staff in staff_members])
    else:
        st.write("No staff found.")

    # Adding new staff
    new_staff_name = st.text_input("New Staff Name")
    new_staff_email = st.text_input("New Staff Email")
    new_staff_phone = st.text_input("New Staff Phone")
    new_staff_role_id = st.selectbox("Role", list(role_options.keys()), format_func=lambda x: role_options[x])
    
    if st.button("Add Staff") and new_staff_name and new_staff_email and new_staff_phone:
        save_data("""
            INSERT INTO Staff (staff_name, staff_phone, staff_email, role_id)
            VALUES (:name, :phone, :email, :role_id)
        """, {"name": new_staff_name, "phone": new_staff_phone, "email": new_staff_email, "role_id": new_staff_role_id})
        st.success("Staff added successfully.")
        st.rerun()  # Refreshes to show the new staff member

    for staff in staff_members:
        # Staff update fields
        new_name = st.text_input(f"Edit Name for Staff {staff['staff_id']}", staff['staff_name'], key=f"edit_name_{staff['staff_id']}")
        new_phone = st.text_input(f"Edit Phone for Staff {staff['staff_id']}", staff['staff_phone'], key=f"edit_phone_{staff['staff_id']}")
        new_role_id = st.selectbox(f"Edit Role for Staff {staff['staff_id']}", list(role_options.keys()), 
                                   index=list(role_options.keys()).index(staff['role_id']), format_func=lambda x: role_options[x],
                                   key=f"edit_role_{staff['staff_id']}")
        
        # Update button
        if st.button("Update", key=f"update_staff_{staff['staff_id']}"):
            save_data("""
                UPDATE Staff SET staff_name = :name, staff_phone = :phone, role_id = :role_id WHERE staff_id = :staff_id
            """, {"name": new_name, "phone": new_phone, "role_id": new_role_id, "staff_id": staff['staff_id']})
            st.success("Staff updated.")
            st.rerun()  # Refreshes to show updated data
        
        # Delete button
        if st.button("Delete", key=f"delete_staff_{staff['staff_id']}"):
            save_data("DELETE FROM Staff WHERE staff_id = :staff_id", {"staff_id": staff['staff_id']})
            st.success("Staff deleted.")
            st.experimental_rerun()  # Refreshes to show deletion
