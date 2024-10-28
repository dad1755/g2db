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

    # View bookings to confirm payment
    pending_bookings = load_data("SELECT * FROM Reservation WHERE payment_status = 'pending'")
    for booking in pending_bookings:
        st.write(f"Booking ID: {booking['reserve_id']}, Cottage ID: {booking['cottage_id']}, Total Price: {booking['total_price']}")
    
    payment_id = st.text_input("Enter Payment ID to Approve")
    if st.button("Approve Payment"):
        # Change status of cottage to available and clear other orders
        update_payment_query = "UPDATE Payment SET status = 'approved' WHERE payment_id = :payment_id"
        save_data(update_payment_query, {"payment_id": payment_id})

        # Change cottage status back to available
        update_cottage_query = "UPDATE Cottage SET cottage_status = 'available' WHERE cottage_id = (SELECT cottage_id FROM Reservation WHERE reserve_id = (SELECT reserve_id FROM Payment WHERE payment_id = :payment_id))"
        save_data(update_cottage_query, {"payment_id": payment_id})

        st.success("Payment approved and cottage status updated.")

    # Add and view discounts
    discount = st.number_input("Enter Discount Percentage", 0, 100)
    if st.button("Add Discount"):
        add_discount_query = "INSERT INTO Discounts (percentage) VALUES (:percentage)"
        save_data(add_discount_query, {"percentage": discount})
        st.success("Discount added successfully.")

    # Add new cottage
    new_cottage_name = st.text_input("Cottage Name")
    new_cottage_price = st.number_input("Cottage Price")
    if st.button("Add Cottage"):
        add_cottage_query = "INSERT INTO Cottage (cottage_name, price) VALUES (:cottage_name, :price)"
        save_data(add_cottage_query, {"cottage_name": new_cottage_name, "price": new_cottage_price})
        st.success("New cottage added successfully.")

    # Add, view, and set roles to staff
    staff_name = st.text_input("Staff Name")
    staff_role = st.selectbox("Staff Role", ["Admin", "Housekeeper", "Manager"])
    if st.button("Add Staff"):
        add_staff_query = "INSERT INTO Staff (name, role) VALUES (:name, :role)"
        save_data(add_staff_query, {"name": staff_name, "role": staff_role})
        st.success("Staff added successfully.")
