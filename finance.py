import streamlit as st
from db import load_data, save_data

def payment_section():
    st.header("Process Payment")

    # Show pending payments
    pending_payments = load_data("SELECT payment_id FROM Payment WHERE status = 'pending'")
    if not pending_payments:  # Check if there are no pending payments
        st.warning("No pending payments found.")
        return
    
    payment_id = st.selectbox("Pending Payments", [p['payment_id'] for p in pending_payments])

    if st.button("Approve Payment"):
        update_payment_query = "UPDATE Payment SET status = 'approved' WHERE payment_id = :payment_id"
        save_data(update_payment_query, {"payment_id": payment_id})
        st.success("Payment approved.")
def view_booking_to_confirm_payment():
    st.header("Bookings to Confirm Payment")
    # Implement the logic to view bookings that require payment confirmation.

def add_view_discount():
    st.header("Manage Discounts")
    # Implement the logic to add and view discounts.

def add_view_cottage():
    st.header("Add and View Cottages")
    # Implement the logic to add new cottages and view existing cottages.

def add_view_roles():
    st.header("Manage Staff Roles")
    # Implement the logic to add and view staff roles.

