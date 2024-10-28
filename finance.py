import streamlit as st
from sqlalchemy import create_engine, text

# Database connection setup
DATABASE_URL = "mysql+mysqlconnector://sql12741294:Lvu9cg9kGm@sql12.freemysqlhosting.net:3306/sql12741294"
engine = create_engine(DATABASE_URL)

# Load data from MySQL
def load_data(query, parameters=None):
    with engine.connect() as connection:
        result = connection.execute(text(query), parameters or {})
        return [dict(row) for row in result]

def save_data(query, parameters=None):
    with engine.connect() as connection:
        connection.execute(text(query), parameters or {})

# Finance Section
def finance_section():
    st.header("Finance Management")

    # Approve Payment Section
    st.subheader("Approve Payment")
    pending_bookings = load_data("SELECT * FROM Reservation WHERE payment_status = 'pending'")
    
    if pending_bookings:
        for booking in pending_bookings:
            st.write(f"Booking ID: {booking['reserve_id']}, Cottage ID: {booking['cottage_id']}, Total Price: {booking['total_price']}")
    else:
        st.write("No pending bookings.")
    
    payment_id = st.text_input("Enter Payment ID to Approve", key="payment_id_input")
    if st.button("Approve Payment", key="approve_payment_button"):
        if payment_id:  # Check if payment_id is not empty
            try:
                update_payment_query = "UPDATE Payment SET status = 'approved' WHERE payment_id = :payment_id"
                save_data(update_payment_query, {"payment_id": payment_id})

                # Update the cottage status to available
                update_cottage_query = """
                    UPDATE Cottage 
                    SET cottage_status = 'available' 
                    WHERE cottage_id = (
                        SELECT cottage_id 
                        FROM Reservation 
                        WHERE reserve_id = (
                            SELECT reserve_id 
                            FROM Payment 
                            WHERE payment_id = :payment_id
                        )
                    )
                """
                save_data(update_cottage_query, {"payment_id": payment_id})
                st.success("Payment approved and cottage status updated.")
            except Exception as e:
                st.error(f"Error approving payment: {e}")
        else:
            st.warning("Please enter a valid Payment ID.")

    # Cottage Management Section
    st.subheader("Cottage Management")
    new_cottage_name = st.text_input("Cottage Name", key="new_cottage_name")
    new_cottage_description = st.text_area("Cottage Description", key="new_cottage_description")
    new_cottage_price = st.number_input("Cottage Price", min_value=0.0, format="%.2f", key="new_cottage_price")
    new_cottage_status = st.selectbox("Cottage Status", ["available", "not available"], key="new_cottage_status")

    if st.button("Add Cottage", key="add_cottage_button"):
        try:
            add_cottage_query = """
                INSERT INTO Cottage (cottage_name, cottage_description, cottage_status, cottage_price) 
                VALUES (:cottage_name, :cottage_description, :cottage_status, :price)
            """
            save_data(add_cottage_query, {
                "cottage_name": new_cottage_name,
                "cottage_description": new_cottage_description,
                "cottage_status": new_cottage_status,
                "price": new_cottage_price
            })
            st.success("New cottage added successfully.")
        except Exception as e:
            st.error(f"Error adding cottage: {e}")

    # View Existing Cottages
    st.subheader("View Cottages")
    cottages = load_data("SELECT * FROM Cottage")
    if cottages:
        for cottage in cottages:
            st.write(f"Cottage ID: {cottage['cottage_id']}, Name: {cottage['cottage_name']}, Price: {cottage['cottage_price']}, Status: {cottage['cottage_status']}")
            if st.button(f"Update Cottage {cottage['cottage_id']}", key=f"update_cottage_{cottage['cottage_id']}"):
                update_cottage(cottage)
    else:
        st.write("No cottages found.")

    # Staff Management Section
    st.subheader("Staff Management")
    staff_name = st.text_input("Staff Name", key="staff_name_input")
    staff_role = st.selectbox("Staff Role", ["Admin", "Housekeeper", "Manager"], key="staff_role_select")
    staff_phone = st.text_input("Staff Phone", key="staff_phone_input")
    staff_email = st.text_input("Staff Email", key="staff_email_input")

    if st.button("Add Staff", key="add_staff_button"):
        try:
            add_staff_query = """
                INSERT INTO Staff (staff_name, role_id, staff_phone, staff_email) 
                VALUES (:staff_name, (SELECT role_id FROM Role WHERE role_name = :role_name), :staff_phone, :staff_email)
            """
            save_data(add_staff_query, {
                "staff_name": staff_name,
                "role_name": staff_role,
                "staff_phone": staff_phone,
                "staff_email": staff_email
            })
            st.success("Staff added successfully.")
            
            # Debugging: Check if the staff member has been added
            st.write("Debug: Checking staff members after addition...")
            staff_members = load_data("SELECT * FROM Staff")
            st.write(staff_members)  # This will show you the current staff members

        except Exception as e:
            st.error(f"Error adding staff: {e}")

    # View Existing Staff
    st.subheader("View Staff")
    staff_members = load_data("SELECT * FROM Staff")
    if staff_members:
        for staff in staff_members:
            st.write(f"Staff ID: {staff['staff_id']}, Name: {staff['staff_name']}, Role: {staff['role_id']}, Phone: {staff['staff_phone']}, Email: {staff['staff_email']}")
            if st.button(f"Update Staff {staff['staff_id']}", key=f"update_staff_{staff['staff_id']}"):
                update_staff(staff)
    else:
        st.write("No staff members found.")

def update_cottage(cottage):
    """Function to update existing cottage information."""
    st.subheader(f"Update Cottage ID: {cottage['cottage_id']}")
    
    # Get current values
    updated_name = st.text_input("Cottage Name", value=cottage['cottage_name'], key=f"update_cottage_name_{cottage['cottage_id']}")
    updated_description = st.text_area("Cottage Description", value=cottage['cottage_description'], key=f"update_cottage_description_{cottage['cottage_id']}")
    updated_price = st.number_input("Cottage Price", value=cottage['cottage_price'], min_value=0.0, format="%.2f", key=f"update_cottage_price_{cottage['cottage_id']}")
    updated_status = st.selectbox("Cottage Status", ["available", "not available"], index=0 if cottage['cottage_status'] == 'available' else 1, key=f"update_cottage_status_{cottage['cottage_id']}")
    
    if st.button("Update Cottage", key=f"confirm_update_cottage_{cottage['cottage_id']}"):
        try:
            update_query = """
                UPDATE Cottage 
                SET cottage_name = :cottage_name, 
                    cottage_description = :cottage_description, 
                    cottage_price = :cottage_price, 
                    cottage_status = :cottage_status 
                WHERE cottage_id = :cottage_id
            """
            save_data(update_query, {
                "cottage_name": updated_name,
                "cottage_description": updated_description,
                "cottage_price": updated_price,
                "cottage_status": updated_status,
                "cottage_id": cottage['cottage_id']
            })
            st.success("Cottage updated successfully.")
        except Exception as e:
            st.error(f"Error updating cottage: {e}")

def update_staff(staff):
    """Function to update existing staff information."""
    st.subheader(f"Update Staff ID: {staff['staff_id']}")
    
    # Get current values
    updated_name = st.text_input("Staff Name", value=staff['staff_name'], key=f"update_staff_name_{staff['staff_id']}")
    updated_role = st.selectbox("Staff Role", ["Admin", "Housekeeper", "Manager"], index=0 if staff['role_id'] == 'Admin' else (1 if staff['role_id'] == 'Housekeeper' else 2), key=f"update_staff_role_{staff['staff_id']}")
    updated_phone = st.text_input("Staff Phone", value=staff['staff_phone'], key=f"update_staff_phone_{staff['staff_id']}")
    updated_email = st.text_input("Staff Email", value=staff['staff_email'], key=f"update_staff_email_{staff['staff_id']}")
    
    if st.button("Update Staff", key=f"confirm_update_staff_{staff['staff_id']}"):
        try:
            update_query = """
                UPDATE Staff 
                SET staff_name = :staff_name, 
                    role_id = (SELECT role_id FROM Role WHERE role_name = :role_name), 
                    staff_phone = :staff_phone, 
                    staff_email = :staff_email 
                WHERE staff_id = :staff_id
            """
            save_data(update_query, {
                "staff_name": updated_name,
                "role_name": updated_role,
                "staff_phone": updated_phone,
                "staff_email": updated_email,
                "staff_id": staff['staff_id']
            })
            st.success("Staff updated successfully.")
        except Exception as e:
            st.error(f"Error updating staff: {e}")

# Main app function
def main():
    finance_section()

if __name__ == "__main__":
    main()
