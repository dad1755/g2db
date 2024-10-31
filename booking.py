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
        cursor.execute("SELECT cot_name FROM COTTAGE")
        cottages = [row[0] for row in cursor.fetchall()]  # Extract cottage names from result
        cursor.close()
        connection.close()
    return cottages

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

    # Booking Details section
    with st.container():
        st.write("### Booking Details")
        cottage = st.selectbox("Cottage", options=cottage_options)  # Dynamic cottage options
        check_in_date = st.date_input("Check-in Date")
        nights = st.number_input("Number of Nights", min_value=1)
        
        # Calculate check-out date
        check_out_date = check_in_date + timedelta(days=nights)
        st.write(f"Check-out Date: {check_out_date}")

    # Booking form submission
    with st.form(key='booking_form'):
        submit_button = st.form_submit_button("Book Now")

        if submit_button:
            cust_id = insert_customer(name, email, phone)  # Insert customer and retrieve ID
            
            # Confirm customer record creation
            if cust_id:
                st.success(f"Customer '{name}' added with ID: {cust_id}")
                st.success(f"Booking confirmed for {name} in {cottage} from {check_in_date} to {check_out_date} for {nights} night(s).")
            else:
                st.error("Error adding customer details. Please try again.")

# Run the function to display booking form on Streamlit app
show_booking()
