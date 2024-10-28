import streamlit as st
from sqlalchemy import create_engine, text
from datetime import datetime
import housekeeping  # Importing housekeeping module
import finance  # Importing finance module

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

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Reservation", "Housekeeping", "Finance"])

if page == "Reservation":
    reservation_section()
elif page == "Housekeeping":
    housekeeping.housekeeping_section()  # Call the housekeeping section from housekeeping.py
elif page == "Finance":
    finance.finance_section()  # Call the finance section from finance.py
