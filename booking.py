import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import timedelta

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

# Function to establish database connection
def create_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Function to fetch cottages from the database
def fetch_cottages():
    connection = create_connection()
    cottages = []
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT cot_id, cot_name, cot_price FROM COTTAGE")  # Fetching cot_id and cot_price as well
        cottages = cursor.fetchall()  # Fetch all results
        cursor.close()
        connection.close()
    return cottages

# Function to fetch payment types from the database
def fetch_payment_types():
    connection = create_connection()
    payment_types = []
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT pt_id, pt_details FROM PAYMENT_TYPES")  # Fetching pt_id as well
        payment_types = cursor.fetchall()  # Fetch all results
        cursor.close()
        connection.close()
    return payment_types

# Function to insert customer into the database
def insert_customer(name, email, phone):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        insert_query = "INSERT INTO CUSTOMER (cust_name, cust_phone) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, phone))
        connection.commit()
        cust_id = cursor.lastrowid  # Get the newly inserted customer ID
        cursor.close()
        connection.close()
        return cust_id
    return None

# Function to fetch discounts for a specific cottage
def fetch_discounts(cottage_id):
    connection = create_connection()
    discounts = []
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT dis_id, dis_amount FROM DISCOUNT WHERE cot_id = %s", (cottage_id,))
        discounts = cursor.fetchall()  # Fetch all results
        cursor.close()
        connection.close()
    return discounts

# Function to fetch the price of a specific cottage
def fetch_cottage_price(cottage_id):
    connection = create_connection()
    price = None
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT cot_price FROM COTTAGE WHERE cot_id = %s", (cottage_id,))
        price = cursor.fetchone()  # Fetch the price
        cursor.close()
        connection.close()
    return price[0] if price else None

# Function to insert booking into the database
def insert_booking(cust_id, cottage_id, check_in, check_out, payment_type_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO BOOKING (cust_id, cot_id, check_in_date, check_out_date, payment_types, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (cust_id, cottage_id, check_in, check_out, payment_type_id, 1))  # Assuming 1 for "pending"
        connection.commit()
        cursor.close()
        connection.close()

# Main booking function
def show_booking():
    st.subheader("Booking")
    st.write("This is the Booking section where you can manage your cottage bookings.")

    # Customer Details section
    with st.container():
        st.write("### Customer Details")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")

    # Fetch cottage options from database
    cottage_options = fetch_cottages()
    if not cottage_options:
        st.error("No cottages available. Please check your database.")
        return

    # Fetch payment options from database
    payment_options = fetch_payment_types()
    if not payment_options:
        st.error("No payment types available. Please check your database.")
        return

    # Booking Details section
    with st.container():
        st.write("### Booking Details")
        
        # Cottage selection with ID extraction
        cottage_options_dict = {f"{name} (ID: {id}, Price: ${price})": id for id, name, price in cottage_options}
        cottage = st.selectbox("Cottage", options=list(cottage_options_dict.keys()))  # Display cottage names with IDs
        cottage_id = cottage_options_dict[cottage]  # Directly get cot_id from the dictionary

        check_in_date = st.date_input("Check-in Date")
        nights = st.number_input("Number of Nights", min_value=1)

        # Calculate check-out date
        check_out_date = check_in_date + timedelta(days=nights)
        st.write(f"Check-out Date: {check_out_date}")

        # Payment Type selection with ID extraction
        payment_options_dict = {f"{details} (ID: {id})": id for id, details in payment_options}  # Dictionary for payment types
        payment_type = st.selectbox("Payment Type", options=list(payment_options_dict.keys()))  # Display payment details with IDs
        payment_type_id = payment_options_dict[payment_type]  # Directly get pt_id from the dictionary

        # Fetch cottage price
        cottage_price = fetch_cottage_price(cottage_id)
        total_price = cottage_price * nights if cottage_price is not None else 0
        st.write(f"Total Price (without discount): ${total_price:.2f}")

        # Fetch and display discounts for the selected cottage
        discounts = fetch_discounts(cottage_id)
        if discounts:
            st.write("### Available Discounts")
            for dis_id, dis_amount in discounts:
                st.write(f"Discount ID: {dis_id}, Amount: ${dis_amount:.2f}")
                total_price -= dis_amount  # Apply the discount to total price

        # Display the final price after discount
        st.write(f"Total Price after discount: ${total_price:.2f}")

    # Booking form submission
    with st.form(key='booking_form'):
        submit_button = st.form_submit_button("Book Now")

        if submit_button:
            cust_id = insert_customer(name, email, phone)  # Insert customer and retrieve ID
            
            # Confirm customer record creation
            if cust_id:
                insert_booking(cust_id, cottage_id, check_in_date, check_out_date, payment_type_id)  # Insert booking
                st.success(f"Customer '{name}' added with ID: {cust_id}")
                st.success(f"Booking confirmed for {name} in {cottage.split(' (ID: ')[0]} from {check_in_date} to {check_out_date} for {nights} night(s).")
                st.success(f"Payment Type: {payment_type.split(' (ID: ')[0]}")
                st.success(f"Final Price after discount: ${total_price:.2f}")  # Show final price
            else:
                st.error("Error adding customer details. Please try again.")

# Run the function to display booking form on Streamlit app
if __name__ == "__main__":
    show_booking()
