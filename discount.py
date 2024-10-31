import streamlit as st
import mysql.connector
from mysql.connector import Error
from decimal import Decimal

# Hardcoded database configuration (make sure to secure your credentials)
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def execute_query(query, params=None):
    """Execute a query with optional parameters."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)  # Using parameterized queries is good for safety
        else:
            cursor.execute(query)
        connection.commit()
        return cursor  # Return cursor for further processing
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_data(query):
    """Fetch data from the database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows  # Return fetched rows
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Discount Management Functions
def create_discount(cot_id, dis_amount, staff_id):
    """Create a new discount."""
    query = "INSERT INTO DISCOUNT (cot_id, dis_amount, staff_id) VALUES (%s, %s, %s)"
    execute_query(query, (cot_id, dis_amount, staff_id))

def get_discounts():
    """Fetch all discounts."""
    query = """
    SELECT d.dis_id, c.cot_name, d.dis_amount, s.staff_name 
    FROM DISCOUNT d
    JOIN COTTAGE c ON d.cot_id = c.cot_id
    JOIN STAFF s ON d.staff_id = s.staff_id
    """
    data = fetch_data(query)
    if data is None:
        return []  # Return an empty list instead of None to avoid errors in UI
    # Convert Decimal amounts to float
    for row in data:
        row['dis_amount'] = float(row['dis_amount']) if isinstance(row['dis_amount'], Decimal) else row['dis_amount']
    return data

def delete_discount(discount_id):
    """Delete a discount by ID."""
    query = "DELETE FROM DISCOUNT WHERE dis_id = %s"
    execute_query(query, (discount_id,))

def edit_discount(dis_id, new_cot_id, new_dis_amount, new_staff_id):
    """Edit an existing discount."""
    query = "UPDATE DISCOUNT SET cot_id = %s, dis_amount = %s, staff_id = %s WHERE dis_id = %s"
    execute_query(query, (new_cot_id, new_dis_amount, new_staff_id, dis_id))

def get_cottages():
    """Fetch all cottages."""
    query = "SELECT * FROM COTTAGE"
    return fetch_data(query) or []

def get_staff():
    """Fetch all staff members."""
    query = "SELECT * FROM STAFF"
    return fetch_data(query) or []

def show_discount_management():
    """Streamlit UI for Discount Management."""
    st.subheader("Discount Management")

    # Add Discount
    st.write("### Add Discount")
    cottages = get_cottages()
    staff = get_staff()

    if cottages and staff:
        cot_names = [f"{c['cot_id']} - {c['cot_name']}" for c in cottages]
        staff_names = [f"{s['staff_id']} - {s['staff_name']}" for s in staff]

        selected_cot = st.selectbox("Select Cottage", options=cot_names)
        selected_staff = st.selectbox("Select Staff", options=staff_names)
        discount_amount = st.number_input("Discount Amount", min_value=0.0, max_value=100.0, step=0.1)

        if st.button("Add Discount"):
            if selected_cot and selected_staff:
                cot_id = int(selected_cot.split(" - ")[0])
                staff_id = int(selected_staff.split(" - ")[0])
                create_discount(cot_id, discount_amount, staff_id)
                st.success(f"Added Discount: {discount_amount} for {selected_cot} by {selected_staff}")
            else:
                st.warning("Please select a Cottage and Staff.")

    # View Discounts
    st.write("### Discount List")
    discount_data = get_discounts()
    if discount_data:
        st.dataframe(discount_data)

        # Prepare to delete a discount
        st.write("### Delete Discount")
        discount_ids = [discount['dis_id'] for discount in discount_data]
        discount_ids_to_delete = st.selectbox("Select Discount to Delete", options=discount_ids)

        if st.button("Delete Discount"):
            if discount_ids_to_delete:
                delete_discount(discount_ids_to_delete)
                st.success(f"Deleted Discount ID: {discount_ids_to_delete}")
            else:
                st.warning("Please select a Discount to delete.")

        # Prepare to edit a discount
        st.write("### Edit Discount")
        discount_to_edit = st.selectbox("Select Discount to Edit", options=discount_ids)
        if discount_to_edit:
            # Get the current details of the selected discount
            current_discount = next(d for d in discount_data if d['dis_id'] == discount_to_edit)
            current_cot_name = current_discount['cot_name']
            current_dis_amount = current_discount['dis_amount']
            current_staff_name = current_discount['staff_name']

            # Display current details
            st.write(f"Current Cottage: {current_cot_name}")
            st.write(f"Current Discount Amount: {current_dis_amount}")
            st.write(f"Current Staff: {current_staff_name}")

            # New values for edit
            new_selected_cot = st.selectbox("New Cottage", options=cot_names)
            new_selected_staff = st.selectbox("New Staff", options=staff_names)
            new_discount_amount = st.number_input("New Discount Amount", min_value=0.0, max_value=100.0, step=0.1, value=current_dis_amount)

            if st.button("Update Discount"):
                if new_selected_cot and new_selected_staff:
                    new_cot_id = int(new_selected_cot.split(" - ")[0])
                    new_staff_id = int(new_selected_staff.split(" - ")[0])
                    edit_discount(discount_to_edit, new_cot_id, new_discount_amount, new_staff_id)
                    st.success(f"Updated Discount ID: {discount_to_edit}")
                else:
                    st.warning("Please select a new Cottage and Staff.")
    else:
        st.warning("No discounts found.")

# Call the show_discount_management function to display the UI
if __name__ == "__main__":
    show_discount_management()
