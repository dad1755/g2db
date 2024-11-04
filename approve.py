import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

# Function to connect to the database and execute queries
def get_database_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Fetch all booking data from the database
def fetch_booking_data():
    connection = get_database_connection()
    if connection:
        try:
            query = "SELECT * FROM BOOKING"  # Fetch all bookings without filter
            booking_data = pd.read_sql(query, connection)
            return booking_data
        except Error as e:
            st.error(f"Error fetching data: {e}")
            return pd.DataFrame()
        finally:
            connection.close()
    return pd.DataFrame()

# Function to update payment_status for a specific booking and delete conflicting entries
def update_payment_status(book_id):
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Update payment_status to 2 for the selected booking
            update_query = "UPDATE BOOKING SET payment_status = 2 WHERE book_id = %s"
            cursor.execute(update_query, (book_id,))
            connection.commit()

            # Get cot_id for the confirmed booking
            cot_query = "SELECT cot_id FROM BOOKING WHERE book_id = %s"
            cursor.execute(cot_query, (book_id,))
            cot_id = cursor.fetchone()[0]  # Fetch cot_id of the current booking

            # Delete other bookings with the same cot_id and payment_status = 1
            delete_query = "DELETE FROM BOOKING WHERE cot_id = %s AND payment_status = 1 AND book_id != %s"
            cursor.execute(delete_query, (cot_id, book_id))
            connection.commit()

            st.success(f"Booking ID {book_id} has been confirmed! Other pending bookings with the same cot_id have been removed.")
            st.rerun()  # Use experimental_rerun to refresh the app

        except Error as e:
            st.error(f"Error updating booking: {e}")
        finally:
            cursor.close()
            connection.close()

# Streamlit UI for displaying and managing booking confirmation
def show_approve_management():
    st.subheader("Booking Management")
    st.write("All Bookings (Pending and Confirmed)")

    # Fetch and display booking data
    booking_data = fetch_booking_data()
    if not booking_data.empty:
        # Optionally, display the data in a table/grid with better formatting
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
                # Confirm button
                if st.button("CONFIRM"):
                    update_payment_status(selected_book_id)
    else:
        st.write("No bookings available.")

# Run this function only if this script is executed directly
if __name__ == "__main__":
    show_approve_management()
