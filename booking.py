import streamlit as st
from db import load_data, save_data
from datetime import datetime

def booking_section():
    st.header("Cottage Reservation")

    # Load customers
    customers = load_data("SELECT cust_id, cust_name, cust_email, cust_phone FROM Customer")
    customer_options = {c['cust_email']: c['cust_name'] for c in customers}
    customer_email = st.selectbox("Customer Email", list(customer_options.keys()), format_func=lambda x: customer_options[x])
    customer = next((c for c in customers if c['cust_email'] == customer_email), None)

    # Cottage selection and availability check
    cottages = load_data("SELECT cottage_id, cottage_name, cottage_price, cottage_description FROM Cottage WHERE cottage_status = 'available'")
    cottage_name = st.selectbox("Cottage", [c['cottage_name'] for c in cottages])
    cottage = next((c for c in cottages if c['cottage_name'] == cottage_name), None)

    check_in = st.date_input("Check-in Date")
    check_out = st.date_input("Check-out Date")

    if st.button("Reserve"):
        if cottage and customer:
            total_price = calculate_total_price(cottage['cottage_price'], check_in, check_out)
            if total_price > 0:
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
                    "total_price": total_price
                }
                try:
                    save_data(new_reservation_query, parameters)
                    st.success("Reservation created successfully!")
                except Exception as e:
                    st.error(f"Error creating reservation: {e}")
            else:
                st.error("Invalid check-in and check-out dates.")
        else:
            st.error("Please select a customer and a cottage.")

def calculate_total_price(cottage_price, check_in, check_out):
    nights = (check_out - check_in).days
    return cottage_price * nights if nights > 0 else 0
