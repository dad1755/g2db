
import streamlit as st
from db import load_data, save_data
from datetime import datetime

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
            "person_check_in": 1,
            "total_price": 100.00  # Replace with calculation as needed
        }
        save_data(new_reservation_query, parameters)
        st.success("Reservation created successfully!")

def view_bookings():
    st.header("View Your Bookings")
    # Implement the logic to fetch and display bookings for the customer.

def notify_booking_confirmation():
    st.header("Booking Confirmation Notification")
    # Implement the logic to notify customers about booking confirmations.

def review_past_orders():
    st.header("Review Past Orders")
    # Implement the logic to fetch and display past orders for the customer.
