import os
import streamlit as st
import pandas as pd
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text

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

# Function to fetch booking data from the database
def fetch_booking_data():
    try:
        with engine.connect() as conn:
            query = "SELECT * FROM BOOKING"  # Fetch all bookings without filter
            booking_data = pd.read_sql(query, conn)
            return booking_data
    except Exception as e:
        st.error(f"Error fetching booking data: {e}")
        return pd.DataFrame()

# Fetch all staff data from the STAFF table
def fetch_staff_data():
    try:
        with engine.connect() as conn:
            query = "SELECT staff_id, staff_name FROM STAFF"
            staff_data = pd.read_sql(query, conn)
            return staff_data
    except Exception as e:
        st.error(f"Error fetching staff data: {e}")
        return pd.DataFrame()

# Function to update payment_status and assign staff_id for a specific booking
def confirm_booking(book_id, staff_id):
    try:
        with engine.connect() as conn:
            # Update payment_status to 2 and assign staff_id for the selected booking
            update_query = """
                UPDATE BOOKING 
                SET payment_status = 2, staff_id = :staff_id 
                WHERE book_id = :book_id
            """
            conn.execute(text(update_query), {"staff_id": staff_id, "book_id": book_id})

            # Get cot_id for the confirmed booking
            cot_query = "SELECT cot_id FROM BOOKING WHERE book_id = :book_id"
            result = conn.execute(text(cot_query), {"book_id": book_id})
            cot_id = result.fetchone()[0]  # Fetch cot_id of the current booking

            # Delete other bookings with the same cot_id and payment_status = 1
            delete_query = "DELETE FROM BOOKING WHERE cot_id = :cot_id AND payment_status = 1 AND book_id != :book_id"
            conn.execute(text(delete_query), {"cot_id": cot_id, "book_id": book_id})

            # Update ct_id_stat to 3 in COTTAGE_ATTRIBUTES_RELATION
            update_cottage_query = "UPDATE COTTAGE_ATTRIBUTES_RELATION SET ct_id_stat = 3 WHERE cot_id = :cot_id"
            conn.execute(text(update_cottage_query), {"cot_id": cot_id})

            st.success(f"Booking ID {book_id} has been confirmed! Staff ID {staff_id} has been assigned.")
            st.rerun()  # Refresh the app

    except Exception as e:
        st.error(f"Error updating booking: {e}")

# Streamlit UI for displaying and managing booking confirmation
def show_approve_management():
    st.subheader("Booking Management")
    st.write("All Bookings (Pending and Confirmed)")

    # Fetch and display booking data
    booking_data = fetch_booking_data()
    if not booking_data.empty:
        # Display booking data in a table
        st.dataframe(booking_data)

        # Dropdown to select a booking ID
        book_id_list = booking_data['book_id'].tolist()
        selected_book_id = st.selectbox("Select Booking ID to Confirm", book_id_list)

        # Fetch the selected booking's current status
        selected_booking = booking_data[booking_data['book_id'] == selected_book_id]
        if not selected_booking.empty:
            current_status = selected_booking.iloc[0]['payment_status']
            if current_status == 2:
                st.info(f"Booking ID {selected_book_id} is already confirmed.")
            else:
                # Fetch staff data and create dropdown for staff selection
                staff_data = fetch_staff_data()
                if not staff_data.empty:
                    staff_options = staff_data['staff_name'] + " (ID: " + staff_data['staff_id'].astype(str) + ")"
                    selected_staff = st.selectbox("Select Staff to Confirm Booking", staff_options)
                    selected_staff_id = int(selected_staff.split(" (ID: ")[1][:-1])  # Extract staff_id from the selected option

                    # Confirm button
                    if st.button("CONFIRM"):
                        confirm_booking(selected_book_id, selected_staff_id)
                else:
                    st.write("No staff available for assignment.")
    else:
        st.write("No bookings available.")

# Run this function only if this script is executed directly
if __name__ == "__main__":
    show_approve_management()
