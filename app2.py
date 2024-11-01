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

def add_payment_type(pt_details):
    """Insert a new payment type into the database without needing pt_id."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            query = "INSERT INTO PAYMENT_TYPES (pt_details) VALUES (%s)"
            cursor.execute(query, (pt_details,))
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

    # Create tabs
    tabs = st.tabs(["Add Payment Type", "View Payment Types", "Delete Payment Type"])

    # Add Payment Type tab
    with tabs[0]:
        pt_details = st.text_input("Payment Type Details (pt_details)", max_chars=50)
        if st.button("Add Payment Type"):
            if pt_details:
                add_payment_type(pt_details)
                st.experimental_rerun()  # Refresh the app to show the new payment type
            else:
                st.warning("Please fill in the payment type details.")

    # View Payment Types tab
    with tabs[1]:
        payment_types_df = view_payment_types()
        if not payment_types_df.empty:
            st.dataframe(payment_types_df)
        else:
            st.info("No payment types found.")

    # Delete Payment Type tab
    with tabs[2]:
        payment_types_df = view_payment_types()
        if not payment_types_df.empty:
            delete_options = [(row['pt_id'], row['pt_details']) for index, row in payment_types_df.iterrows()]
            formatted_options = [f"{pt_id}: {pt_details}" for pt_id, pt_details in delete_options]
            delete_id = st.selectbox("Select Payment Type to delete", formatted_options)

            if st.button("Delete Payment Type"):
                selected_pt_id = delete_id.split(":")[0]  # Get the pt_id from the formatted string
                delete_payment_type(selected_pt_id)
                st.experimental_rerun()  # Refresh the app to update the data
        else:
            st.info("No payment types found to delete.")

if __name__ == "__main__":
    main()
