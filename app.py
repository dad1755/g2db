import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Database connection details
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def add_payment_type(pt_id, pt_details):
    """Insert a new payment type into the database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            query = "INSERT INTO PAYMENT_TYPES (pt_id, pt_details) VALUES (%s, %s)"
            cursor.execute(query, (pt_id, pt_details))
            connection.commit()
            st.success("Payment type added successfully!")
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def view_payment_types():
    """Retrieve payment types from the database and return them as a DataFrame."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            query = "SELECT * FROM PAYMENT_TYPES"
            df = pd.read_sql(query, connection)
            return df
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
    return pd.DataFrame()  # Return an empty DataFrame if there's an error

def delete_payment_type(pt_id):
    """Delete a payment type from the database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            query = "DELETE FROM PAYMENT_TYPES WHERE pt_id = %s"
            cursor.execute(query, (pt_id,))
            connection.commit()
            st.success("Payment type deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    st.title("Payment Types Management")

    # Add Payment Type section
    st.subheader("Add Payment Type")
    pt_id = st.text_input("Payment Type ID (pt_id)", max_chars=10)
    pt_details = st.text_input("Payment Type Details (pt_details)", max_chars=50)

    if st.button("Add Payment Type"):
        if pt_id and pt_details:
            add_payment_type(pt_id, pt_details)
        else:
            st.warning("Please fill in both fields.")

    # View Payment Types section
    st.subheader("View Payment Types")
    payment_types_df = view_payment_types()
    if not payment_types_df.empty:
        st.dataframe(payment_types_df)

        # Delete Payment Type section
        st.subheader("Delete Payment Type")
        delete_id = st.selectbox("Select Payment Type ID to delete", payment_types_df['pt_id'].tolist())
        
        if st.button("Delete Payment Type"):
            delete_payment_type(delete_id)
            st.rerun()  # Refresh the app to update the data

    else:
        st.info("No payment types found.")

if __name__ == "__main__":
    main()
