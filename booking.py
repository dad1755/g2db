import os
import streamlit as st
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text
from datetime import timedelta

# Retrieve the service account JSON from st.secrets
service_account_info = st.secrets["google_cloud"]["credentials"]

# Write the JSON to a file
with open("service_account.json", "w") as f:
    f.write(service_account_info)

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

# Retrieve database credentials from st.secrets
INSTANCE_CONNECTION_NAME = st.secrets["database"]["instance_connection_name"]
DB_USER = st.secrets["database"]["db_user"]
DB_PASSWORD = st.secrets["database"]["db_password"]
DB_NAME = st.secrets["database"]["db_name"]

# Initialize Connector object
connector = Connector()

# Function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )
    return conn

# SQLAlchemy engine for creating database connection
engine = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Function to fetch cottages from the database
def fetch_cottages():
    cottages = []
    with engine.connect() as connection:
        query = """
            SELECT c.cot_id, c.cot_name, c.cot_price 
            FROM COTTAGE c
            JOIN COTTAGE_ATTRIBUTES_RELATION car ON c.cot_id = car.cot_id
            WHERE car.ct_id_stat = 2  -- Filter for available cottages
        """
        result = connection.execute(text(query))
        cottages = result.fetchall()
    return cottages

# Function to fetch payment types from the database
def fetch_payment_types():
    payment_types = []
    with engine.connect() as connection:
        query = "SELECT pt_id, pt_details FROM PAYMENT_TYPES"
        result = connection.execute(text(query))
        payment_types = result.fetchall()
    return payment_types

# Function to insert customer into the database
def insert_customer(name, email, phone):
    cust_id = None
    with engine.connect() as connection:
        insert_query = "INSERT INTO CUSTOMER (cust_name, cust_phone) VALUES (:name, :phone)"
        connection.execute(text(insert_query), {"name": name, "phone": phone})
        # Retrieve the customer ID
        result = connection.execute("SELECT LAST_INSERT_ID()")
        cust_id = result.scalar()
    return cust_id

# Function to fetch discounts for a specific cottage
def fetch_discounts(cottage_id):
    discounts = []
    with engine.connect() as connection:
        query = "SELECT dis_id, dis_amount FROM DISCOUNT WHERE cot_id = :cottage_id"
        result = connection.execute(text(query), {"cottage_id": cottage_id})
        discounts = result.fetchall()
    return discounts

# Function to fetch the price of a specific cottage
def fetch_cottage_price(cottage_id):
    price = None
    with engine.connect() as connection:
        query = "SELECT cot_price FROM COTTAGE WHERE cot_id = :cottage_id"
        result = connection.execute(text(query), {"cottage_id": cottage_id})
        price = result.fetchone()
    return price[0] if price else None

# Function to insert booking into the database
def insert_booking(cust_id, cottage_id, check_in, check_out, payment_type_id):
    with engine.connect() as connection:
        insert_query = """
            INSERT INTO BOOKING (cust_id, cot_id, check_in_date, check_out_date, payment_types, payment_status)
            VALUES (:cust_id, :cottage_id, :check_in, :check_out, :payment_type_id, 1)
        """
        connection.execute(text(insert_query), {
            "cust_id": cust_id,
            "cottage_id": cottage_id,
            "check_in": check_in,
            "check_out": check_out,
            "payment_type_id": payment_type_id
        })

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
        st.error("No cottages available. Please check again later.")
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
                total_price -= float(dis_amount)  # Convert Decimal to float

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
