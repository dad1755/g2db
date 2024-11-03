import streamlit as st
import pandas as pd
import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def connect_to_database():
    """Establish a connection to the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

def fetch_table_data(table_name):
    """Fetch data from the specified table."""
    conn = connect_to_database()
    if conn:
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            st.error(f"Error fetching data from {table_name}: {e}")
            return None
        finally:
            conn.close()
    return None

def show_database_management():
    """Display the database management section with grids for all tables."""
    st.subheader("Database Management")
    st.write("View records from various tables in the database.")

    # Define tables to display
    tables = ["COTTAGE_ATTRIBUTES_RELATION", "HOUSEKEEPING", "BOOKING", "PAYMENT_CONFIRMATION"]

    # Loop through each table and display data
    for table_name in tables:
        data = fetch_table_data(table_name)
        if data is not None:
            st.write(f"Showing records from **{table_name}**:")
            st.dataframe(data)  # Display in a grid format
        else:
            st.write(f"No data available or unable to fetch data for **{table_name}**.")

# Run the database management display
show_database_management()
