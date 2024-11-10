import os
import streamlit as st
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text

# Set the path to the service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pro10-439001-dc966978b9d3.json"

# Define your instance connection details and database credentials
INSTANCE_CONNECTION_NAME = "pro10-439001:us-central1:sql12741294"
DB_USER = "group2"
DB_PASSWORD = "group2@2024"
DB_NAME = "12741294g10"

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

# Streamlit app
def main():
    st.title("Database Table Viewer")
    st.write("This app connects to the Google Cloud SQL database and lists all tables.")

    # Connect to the database and retrieve all tables
    try:
        with engine.connect() as connection:
            # Query to get all tables in the database
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]

            # Display tables in the Streamlit app
            if tables:
                st.write("Tables in the database:")
                for table in tables:
                    st.write(f"- {table}")
            else:
                st.write("No tables found in the database.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
