import streamlit as st
from google.cloud.sql.connector import Connector
import sqlalchemy
import pandas as pd

# Database connection parameters
INSTANCE_CONNECTION_NAME = "pro10-439001:us-central1:sql12741294"
DB_USER = "sql12741294"
DB_PASS = "Lvu9cg9kGm"
DB_NAME = "12741294g10"

# Initialize Connector object
connector = Connector()

# Function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# Create SQLAlchemy engine using the getconn function
engine = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Streamlit app title
st.title("Google Cloud SQL Database Connection")

# Text area for SQL query input
query = st.text_area("Enter SQL Query", "SELECT * FROM your_table LIMIT 10")

# Button to execute query
if st.button("Run Query"):
    try:
        # Connect and run query using SQLAlchemy engine
        with engine.connect() as connection:
            result = pd.read_sql(query, connection)
            st.write(result)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Close the Connector when the app stops
connector.close()
