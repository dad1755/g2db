import streamlit as st
from datetime import datetime
from db import load_data, save_data  # Import DB functions from a central location

def calculate_total_price(cottage_price, check_in, check_out):
    nights = (check_out - check_in).days
    return cottage_price * nights if nights > 0 else 0

def reservation_section():
    st.header("Cottage Reservation")

    # Load customers with names, emails, and phone numbers
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

def view_bookings():
    st.header("View Your Bookings")
    customer_email = st.selectbox("Select Your Email", [c['cust_email'] for c in load_data("SELECT cust_email FROM Customer")])
    customer = load_data("SELECT cust_id FROM Customer WHERE cust_email = :email", {"email": customer_email})

    if customer:
        reservations = load_data("""
            SELECT r.reserve_id, c.cottage_name, r.check_in_date, r.check_out_date, r.total_price, r.payment_status, r.reserve_date
            FROM Reservation r
            JOIN Cottage c ON r.cottage_id = c.cottage_id
            WHERE r.cust_id = :cust_id
        """, {"cust_id": customer[0]['cust_id']})

        if reservations:
            for reservation in reservations:
                st.write(f"Reservation ID: {reservation['reserve_id']}, Cottage: {reservation['cottage_name']}, "
                         f"Check-in: {reservation['check_in_date']}, Check-out: {reservation['check_out_date']}, "
                         f"Total Price: {reservation['total_price']}, Payment Status: {reservation['payment_status']}, "
                         f"Reservation Date: {reservation['reserve_date']}")
        else:
            st.write("No bookings found.")

def main():
    reservation_section()
    view_bookings()

if __name__ == "__main__":
    main()
