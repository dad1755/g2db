import os
import streamlit as st
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
