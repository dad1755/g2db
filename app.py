import streamlit as st
import mysql.connector

# Hard-coded database configuration
DB_HOST = "34.67.211.206"         # e.g., "34.123.45.67" or a private IP if configured
DB_USER = "sql12741294"         # e.g., "root"
DB_PASSWORD = "Lvu9cg9kGm" # e.g., "yourpassword"
DB_NAME = "12741294g10"         # e.g., "my_database"

# Function to create a connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Function to run a query
def run_query(query):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    else:
        return None

# Streamlit app
st.title("My Streamlit App with Google Cloud MySQL (Hardcoded)")

# Example query to fetch data
query = "SELECT * FROM your_table LIMIT 5"  # Replace "your_table" with your actual table name
data = run_query(query)

# Display data
if data:
    st.write(data)
else:
    st.write("No data available or an error occurred.")
