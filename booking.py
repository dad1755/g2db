import streamlit as st
from db import load_data, save_data
from datetime import datetime

def calculate_total_price(cottage_price, check_in, check_out):
    # Calculate the number of nights based on the check-in and check-out dates
    nights = (check_out - check_in).days
    return cottage_price * nights if nights > 0 else 0

def reservation_section():
    st.header("Cottage Reservation")

    # Customer selection
    customers = load_data("SELECT cust_id, cust_email FROM Customer")
    customer_email = st.selectbox("Customer Email", [c['cust_email'] for c in customers])
    customer = next((c for c in customers if c['cust_email'] == customer_email), None)

    # Cottage selection and availability check
    cottages = load_data("SELECT cottage_id, cottage_name, cottage_price FROM Cottage WHERE cottage_status = 'available'")
    cottage_name = st.selectbox("Cottage", [c['cottage_name'] for c in cottages])
    cottage = next((c for c in cottages if c['cottage_name'] == cottage_name), None)

    check_in = st.date_input("Check-in Date")
    check_out = st.date_input("Check-out Date")

    if st.button("Reserve"):
        if cottage and customer:
            total_price = calculate_total_price(cottage['cottage_price'], check_in, check_out)
            if total_price > 0:  # Ensure total price is valid
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
                    "person_check_in": 1,  # Defaulting to 1 for simplicity
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

def view_bookings():
    st.header("View Your Bookings")
    customer_email = st.selectbox("Select Your Email", [c['cust_email'] for c in load_data("SELECT cust_email FROM Customer")])
    customer = load_data("SELECT cust_id FROM Customer WHERE cust_email = :email", {"email": customer_email})
    
    if customer:
        reservations = load_data("""
            SELECT r.reserve_id, c.cottage_name, r.check_in_date, r.check_out_date, r.total_price
            FROM Reservation r
            JOIN Cottage c ON r.cottage_id = c.cottage_id
            WHERE r.cust_id = :cust_id
        """, {"cust_id": customer[0]['cust_id']})

        if reservations:
            for reservation in reservations:
                st.write(f"Reservation ID: {reservation['reserve_id']}, Cottage: {reservation['cottage_name']}, Check-in: {reservation['check_in_date']}, Check-out: {reservation['check_out_date']}, Total Price: {reservation['total_price']}")
        else:
            st.write("No bookings found.")

def notify_booking_confirmation():
    st.header("Booking Confirmation Notification")
    st.write("Implement notification logic here.")
    # This could involve sending emails or other forms of communication.

def review_past_orders():
    st.header("Review Past Orders")
    st.write("Implement logic to fetch and display past orders for the customer.")

def main():
    reservation_section()
    view_bookings()
    notify_booking_confirmation()
    review_past_orders()

if __name__ == "__main__":
    main()
