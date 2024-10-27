import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Load JSON data
def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Paths to JSON files
DATA_PATH = Path("data")
CUSTOMERS_FILE = DATA_PATH / "customers.json"
COTTAGES_FILE = DATA_PATH / "cottages.json"
RESERVATIONS_FILE = DATA_PATH / "reservations.json"
PAYMENTS_FILE = DATA_PATH / "payments.json"
MAINTENANCE_FILE = DATA_PATH / "maintenance.json"
INVENTORY_FILE = DATA_PATH / "inventory.json"
UTILITY_BILLS_FILE = DATA_PATH / "utility_bills.json"
HOUSEKEEPING_FILE = DATA_PATH / "housekeeping.json"

# Load data
customers = load_data(CUSTOMERS_FILE)
cottages = load_data(COTTAGES_FILE)
reservations = load_data(RESERVATIONS_FILE)
payments = load_data(PAYMENTS_FILE)
maintenance = load_data(MAINTENANCE_FILE)
inventory = load_data(INVENTORY_FILE)
utility_bills = load_data(UTILITY_BILLS_FILE)
housekeeping = load_data(HOUSEKEEPING_FILE)

# Reservation Section
def reservation_section():
    st.header("Cottage Reservation")

    # Customer selection
    customer_email = st.selectbox("Customer Email", [c['email'] for c in customers])
    customer = next((c for c in customers if c['email'] == customer_email), None)

    # Cottage selection and availability check
    cottage_name = st.selectbox("Cottage", [c['name'] for c in cottages if c['status'] == 'available'])
    cottage = next((c for c in cottages if c['name'] == cottage_name), None)

    check_in = st.date_input("Check-in Date")
    check_out = st.date_input("Check-out Date")

    if st.button("Reserve"):
        new_reservation = {
            "reservation_id": len(reservations) + 1,
            "customer_id": customer['customer_id'],
            "cottage_id": cottage['cottage_id'],
            "reservation_date": str(datetime.now().date()),
            "check_in": str(check_in),
            "check_out": str(check_out),
            "status": "pending"
        }
        reservations.append(new_reservation)
        save_data(RESERVATIONS_FILE, reservations)
        st.success("Reservation created successfully!")

# Payment Section
def payment_section():
    st.header("Process Payment")
    
    # Show pending payments
    pending_payments = [p for p in payments if p['status'] == 'pending']
    payment_id = st.selectbox("Pending Payments", [p['payment_id'] for p in pending_payments])

    if st.button("Approve Payment"):
        payment = next((p for p in payments if p['payment_id'] == payment_id), None)
        if payment:
            payment['status'] = 'approved'
            save_data(PAYMENTS_FILE, payments)
            st.success("Payment approved.")

# Maintenance and Housekeeping
def management_section():
    st.header("Cottage Maintenance and Housekeeping")

    # Maintenance requests
    st.subheader("Maintenance Requests")
    maintenance_request = st.selectbox("Maintenance", [m['maintenance_id'] for m in maintenance if m['status'] == 'requested'])
    if st.button("Mark Maintenance as Completed"):
        req = next((m for m in maintenance if m['maintenance_id'] == maintenance_request), None)
        if req:
            req['status'] = 'completed'
            save_data(MAINTENANCE_FILE, maintenance)
            st.success("Maintenance completed.")

    # Housekeeping requests
    st.subheader("Housekeeping Requests")
    housekeeping_request = st.selectbox("Housekeeping", [h['housekeeping_id'] for h in housekeeping if h['status'] == 'pending'])
    if st.button("Mark Housekeeping as Completed"):
        house = next((h for h in housekeeping if h['housekeeping_id'] == housekeeping_request), None)
        if house:
            house['status'] = 'completed'
            save_data(HOUSEKEEPING_FILE, housekeeping)
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
