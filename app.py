import streamlit as st
import os
import pymysql
from google.cloud.sql.connector import Connector
from google.auth import default

# Database configuration
DB_CONFIG = {
    'instance_connection_name': 'pro10-439001:us-central1:sql12741294',  # Google Cloud SQL instance connection name
    'database': '12741294g10',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
}

# Function to get a connection to Google Cloud SQL
def get_db_connection():
    connector = Connector()

    # Use the default credentials (this will automatically use the Google Cloud SDK credentials)
    _, project_id = default()

    # Use the connector to establish a connection to the Cloud SQL instance
    connection = connector.connect(
        DB_CONFIG['instance_connection_name'],
        "pymysql",
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

    return connection

# Function to test database connection
def test_db_connection():
    try:
        # Get the database connection
        connection = get_db_connection()

        # If the connection is successful, return a success message
        if connection:
            return "Connection Successful!"
        else:
            return "Connection Failed!"
    except Exception as e:
        return f"Error: {e}"
    finally:
        # Make sure the connection is closed after the operation
        if connection:
            connection.close()

# Streamlit app layout
st.title("Google Cloud SQL Database Connection Test")

# Run the connection test
status = test_db_connection()

# Display the status of the connection
st.write(status)
