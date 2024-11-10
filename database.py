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

def connect_to_database():
    """Establish a connection to the database."""
    try:
        conn = engine.connect()
        return conn
    except Exception as e:
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

def delete_record(table_name, record_id):
    """Delete a record from the specified table by ID."""
    conn = connect_to_database()
    if conn:
        try:
            # Use correct primary key based on table name
            if table_name == "HOUSEKEEPING":
                query = f"DELETE FROM {table_name} WHERE housekeep_id = %s"
            elif table_name == "BOOKING":
                query = f"DELETE FROM {table_name} WHERE book_id = %s"
            elif table_name == "COTTAGE_ATTRIBUTES_RELATION":
                query = f"DELETE FROM {table_name} WHERE id = %s"
            else:
                st.error("Unknown table for deletion.")
                return
            
            cursor = conn.cursor()
            cursor.execute(query, (record_id,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Record with ID {record_id} deleted successfully from {table_name}.")
                # Update the session state after deletion
                st.session_state.data[table_name] = fetch_table_data(table_name)  # Refresh data
            else:
                st.warning(f"No record found with ID {record_id} in {table_name}.")
        except Exception as e:
            st.error(f"Error deleting record from {table_name}: {e}")
        finally:
            cursor.close()
            conn.close()

def show_database_management():
    """Display the database management section with grids for all tables."""
    st.subheader("Database Management")
    st.write("View records from various tables in the database.")

    # Define tables to display
    tables = ["COTTAGE_ATTRIBUTES_RELATION", "HOUSEKEEPING", "BOOKING", "PAYMENT_CONFIRMATION"]

    # Initialize session state for data if not already done
    if 'data' not in st.session_state:
        st.session_state.data = {table: fetch_table_data(table) for table in tables}

    # Add a button to refresh data manually
    if st.button("Refresh Data"):
        st.session_state.data = {table: fetch_table_data(table) for table in tables}

    # Loop through each table and display data
    for table_name in tables:
        data = st.session_state.data.get(table_name)  # Get data from session state
        if data is not None:
            st.write(f"Showing records from **{table_name}**:")
            st.dataframe(data)  # Display in a grid format
            
            # Add delete functionality for each table
            if not data.empty:
                record_id = st.text_input(f"Enter ID to delete from {table_name}:", "")
                if st.button(f"Delete Record from {table_name}"):
                    if record_id:  # Check if input is not empty
                        delete_record(table_name, record_id)
                        # Refresh the data after deletion
                        st.session_state.data[table_name] = fetch_table_data(table_name)
                    else:
                        st.warning("Please enter a valid ID to delete.")
        else:
            st.write(f"No data available or unable to fetch data for **{table_name}**.")


# Run this function only if this script is executed directly
if __name__ == "__main__":
    show_database_management()
