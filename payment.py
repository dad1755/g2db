import streamlit as st
from utils.db_utils import execute_query, fetch_data

def create_payment_table():
    query = """
    CREATE TABLE IF NOT EXISTS PAYMENT (
        payment_id INT AUTO_INCREMENT PRIMARY KEY,
        amount DECIMAL(10, 2) NOT NULL,
        payment_date DATE NOT NULL
    )
    """
    execute_query(query)

def add_payment(amount, payment_date):
    query = "INSERT INTO PAYMENT (amount, payment_date) VALUES (%s, %s)"
    result = execute_query(query, (amount, payment_date))
    if isinstance(result, Error):
        st.error(f"Error while adding payment: {result}")
    else:
        st.success(f"Added payment of ${amount} on {payment_date}")

def delete_payment(payment_id):
    query = "DELETE FROM PAYMENT WHERE payment_id = %s"
    result = execute_query(query, (payment_id,))
    if isinstance(result, Error):
        st.error(f"Error while deleting payment: {result}")
    elif result.rowcount > 0:
        st.success(f"Deleted payment record with ID: {payment_id}")
    else:
        st.warning(f"No payment record found with ID: {payment_id}")

def get_payments():
    query = "SELECT * FROM PAYMENT"
    return fetch_data(query)

def show_payment_management():
    st.subheader("Payment Management")
    create_payment_table()

    # Add Payment
    st.write("### Add Payment")
    amount = st.number_input("Amount", min_value=0.0)
    payment_date = st.date_input("Payment Date")
    if st.button("Add Payment"):
        if amount and payment_date:
            add_payment(amount, payment_date)
        else:
            st.warning("Please provide both amount and date.")

    # View Payments
    st.write("### Payment Records")
    payments_data = get_payments()
    if not payments_data.empty:
        st.dataframe(payments_data)

        # Delete Payment
        st.write("### Delete Payment Record")
        payment_id_to_delete = st.number_input("Enter Payment ID to delete", min_value=1)
        if st.button("Delete Payment"):
            if payment_id_to_delete:
                delete_payment(payment_id_to_delete)
            else:
                st.warning("Please enter a Payment ID to delete.")
    else:
        st.warning("No payment records found.")
