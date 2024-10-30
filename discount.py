import streamlit as st
from db_utils import execute_query, fetch_data

def create_discount_table():
    query = """
    CREATE TABLE IF NOT EXISTS DISCOUNT (
        discount_id INT AUTO_INCREMENT PRIMARY KEY,
        discount_code VARCHAR(20) NOT NULL,
        discount_amount DECIMAL(5, 2) NOT NULL
    )
    """
    execute_query(query)

def add_discount(discount_code, discount_amount):
    query = "INSERT INTO DISCOUNT (discount_code, discount_amount) VALUES (%s, %s)"
    result = execute_query(query, (discount_code, discount_amount))
    if isinstance(result, Error):
        st.error(f"Error while adding discount: {result}")
    else:
        st.success(f"Added discount {discount_code} of ${discount_amount}")

def delete_discount(discount_id):
    query = "DELETE FROM DISCOUNT WHERE discount_id = %s"
    result = execute_query(query, (discount_id,))
    if isinstance(result, Error):
        st.error(f"Error while deleting discount: {result}")
    elif result.rowcount > 0:
        st.success(f"Deleted discount with ID: {discount_id}")
    else:
        st.warning(f"No discount found with ID: {discount_id}")

def get_discounts():
    query = "SELECT * FROM DISCOUNT"
    return fetch_data(query)

def show_discount_management():
    st.subheader("Discount Management")
    create_discount_table()

    # Add Discount
    st.write("### Add Discount")
    discount_code = st.text_input("Discount Code")
    discount_amount = st.number_input("Discount Amount", min_value=0.0)
    if st.button("Add Discount"):
        if discount_code and discount_amount:
            add_discount(discount_code, discount_amount)
        else:
            st.warning("Please provide both code and amount.")

    # View Discounts
    st.write("### Available Discounts")
    discounts_data = get_discounts()
    if not discounts_data.empty:
        st.dataframe(discounts_data)

        # Delete Discount
        st.write("### Delete Discount")
        discount_id_to_delete = st.number_input("Enter Discount ID to delete", min_value=1)
        if st.button("Delete Discount"):
            if discount_id_to_delete:
                delete_discount(discount_id_to_delete)
            else:
                st.warning("Please enter a Discount ID to delete.")
    else:
        st.warning("No discounts found.")
