import streamlit as st
from sqlalchemy import create_engine, text
from datetime import datetime

# Database connection setup
DATABASE_URL = "mysql+mysqlconnector://sql12741294:Lvu9cg9kGm@sql12.freemysqlhosting.net:3306/sql12741294"
engine = create_engine(DATABASE_URL)

# Load data from MySQL
def load_data(query):
    with engine.connect() as connection:
        result = connection.execute(text(query))
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
            "person_check_in": 1,  # default to 1; adjust as needed
            "total_price": 100.00  # example, replace with calculation if needed
        }
        save_data(new_reservation_query, parameters)
        st.success("Reservation created successfully!")

# Payment Section
def payment_section():
    st.header("Process Payment")
    
    # Show pending payments
    pending_payments = load_data("SELECT payment_id FROM Payment WHERE status = 'pending'")
    payment_id = st.selectbox("Pending Payments", [p['payment_id'] for p in pending_payments])

    if st.button("Approve Payment"):
        update_payment_query = "UPDATE Payment SET status = 'approved' WHERE payment_id = :payment_id"
        save_data(update_payment_query, {"payment_id": payment_id})
        st.success("Payment approved.")

# Maintenance and Housekeeping
def management_section():
    st.header("Cottage Maintenance and Housekeeping")

    # Maintenance requests
    maintenance_requests = load_data("SELECT maintenance_id FROM Maintenance WHERE status = 'requested'")
    maintenance_request = st.selectbox("Maintenance", [m['maintenance_id'] for m in maintenance_requests])
    if st.button("Mark Maintenance as Completed"):
        update_maintenance_query = "UPDATE Maintenance SET status = 'completed' WHERE maintenance_id = :maintenance_id"
        save_data(update_maintenance_query, {"maintenance_id": maintenance_request})
        st.success("Maintenance completed.")

    # Housekeeping requests
    housekeeping_requests = load_data("SELECT hk_id FROM Housekeeping WHERE status = 'pending'")
    housekeeping_request = st.selectbox("Housekeeping", [h['hk_id'] for h in housekeeping_requests])
    if st.button("Mark Housekeeping as Completed"):
        update_housekeeping_query = "UPDATE Housekeeping SET status = 'completed' WHERE hk_id = :hk_id"
        save_data(update_housekeeping_query, {"hk_id": housekeeping_request})
        st.success("Housekeeping completed.")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Reservation", "Payment", "Management"])

if page == "Reservation":
    reservation_section()
elif page == "Payment":
    payment_section()
elif page == "Management":
    management_section()
