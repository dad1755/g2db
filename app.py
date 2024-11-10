import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to connect to Google Cloud SQL MySQL Database
def create_connection():
    try:
        connection = mysql.connector.connect(
            user='sql12741294',  # Change this to your username
            password='Lvu9cg9kGm',  # Change this to your password
            host='34.67.211.206',  # Replace with your Cloud SQL instance IP address
            database='12741294g10',  # Replace with your database name
            ssl_ca='./server-ca.pem',  # SSL certificate for the server
            ssl_cert='./client-cert.pem',  # Client certificate
            ssl_key='./client-key.pem'  # Client key

        )
        if connection.is_connected():
            st.success("Successfully connected to the database!")
            return connection
        else:
            st.error("Failed to connect to the database.")
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to query the database and fetch results
def fetch_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM STAFF LIMIT 10;")  # Change to your query
    rows = cursor.fetchall()
    st.write("Query Results:", rows)

# Streamlit User Interface
def main():
    st.title("Connect to Google SQL Database")
    
    # Button to establish a connection
    if st.button('Connect to Database'):
        connection = create_connection()
        if connection:
            fetch_data(connection)

    # Display info
    st.info("Ensure you have the necessary SSL certificates for the connection.")

if __name__ == '__main__':
    main()
