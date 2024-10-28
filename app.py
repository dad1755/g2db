import streamlit as st
from sqlalchemy import create_engine, text
from datetime import datetime

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

# Reservation Section
def reservation_section():
    st.header("Cottage Reservation")

    # Customer selection
    customers = load_data("SELECT cust_id, cust_email FROM Customer")
    customer_email = st.selectbox("Customer Email", [c['cust_email'] for c in customers])
    customer = next((c for c in customers if c['cust_email'] == customer_email), None)

    # Booking functionality
    booking_action = st.selectbox("Choose an action", ["Make a Booking", "View My Bookings"])

    if booking_action == "Make a Booking":
        # Cottage selection and availability check
        cottages = load_data("SELECT cottage_id, cottage_name FROM Cottage WHERE cottage_status = 'available'")
        cottage_name = st.selectbox("Cottage", [c['cottage_name'] for c in cottages])
        cottage = next((c for c in cottages if c['cottage_name'] == cottage_name), None)

        check_in = st.date_input("Check-in Date")
        check_out = st.date_input("Check-out Date")

        if st.button("Reserve"):
            new_reservation_query = """
                INSERT INTO Reservation (cust_id, cottage_id, reserve_date, check_in_date, check_out_date, payment_status, person_check_in, total_price)
                VALUES (:cust_id, :cottage_id, :reserve_date, :check_in_date, :check_out_date, :payment_status, :person_check_in, :total_price)
            """
            parameters = {
                "cust_id": customer['cust_id'],
                "cottage_id": cottage['cottage_id'],
                "reserve_date": str(datetime.now().date()),
                "check_in_date": str(check_in),
                "check_out_date": str(check_out),
                "payment_status": "pending",
                "person_check_in": 1,
                "total_price": 100.00  # example, replace with calculation if needed
            }
            save_data(new_reservation_query, parameters)

            # Update cottage status to unavailable
            update_cottage_query = "UPDATE Cottage SET cottage_status = 'unavailable' WHERE cottage_id = :cottage_id"
            save_data(update_cottage_query, {"cottage_id": cottage['cottage_id']})
            st.success("Reservation created successfully! Confirmation notification sent.")

    elif booking_action == "View My Bookings":
        reservations = load_data("SELECT * FROM Reservation WHERE cust_id = :cust_id", {"cust_id": customer['cust_id']})
        if reservations:
            for res in reservations:
                st.write(f"Cottage ID: {res['cottage_id']}, Check-in: {res['check_in_date']}, Check-out: {res['check_out_date']}, Status: {res['payment_status']}")
        else:
            st.write("No bookings found.")

# Housekeeping Section
def housekeeping_section():
    st.header("Housekeeping Management")
    
    # View housekeeping requests
    housekeeping_requests = load_data("SELECT hk_id, cottage_id, status FROM Housekeeping")
    for request in housekeeping_requests:
        st.write(f"Housekeeping ID: {request['hk_id']}, Cottage ID: {request['cottage_id']}, Status: {request['status']}")

    # Manual update of status
    cottage_id = st.selectbox("Select Cottage ID for Housekeeping", [request['cottage_id'] for request in housekeeping_requests])
    staff_id = st.text_input("Enter Staff ID")
    if st.button("Mark as Available"):
        update_status_query = "UPDATE Housekeeping SET status = 'available' WHERE cottage_id = :cottage_id AND staff_id = :staff_id"
        save_data(update_status_query, {"cottage_id": cottage_id, "staff_id": staff_id})
        st.success("Cottage status updated to available.")

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

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Reservation", "Housekeeping", "Finance"])

if page == "Reservation":
    reservation_section()
elif page == "Housekeeping":
    housekeeping_section()
elif page == "Finance":
    finance_section()
