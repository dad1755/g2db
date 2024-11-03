import mysql.connector
import pandas as pd
import streamlit as st
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def fetch_booking_data():
    """Fetch book_id, cot_id, and check_out_date from BOOKING table where payment_status is 2."""
    query = """
        SELECT book_id, cot_id, check_out_date
        FROM BOOKING
        WHERE payment_status = 2
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convert the result to a DataFrame for easy viewing in Streamlit
        df = pd.DataFrame(rows)
        return df
    except Error as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there's an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def show_housekeeping():
    """Display housekeeping booking data with payment_status = 2 in Streamlit."""
    st.subheader("Booking On Going")
    booking_data = fetch_booking_data()
    if not booking_data.empty:
        st.dataframe(booking_data)
    else:
        st.warning("No booking data found with payment_status = 2.")
