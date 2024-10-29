import streamlit as st

def show_management():
    st.subheader("Management2")
    st.write("This is the Management section where you can manage overall operations.")

    # Create tabs for different management functionalities
    tabs = st.tabs(["Payment", "Discount", "Cottage", "Staff"])

    with tabs[0]:  # Payment Tab
        st.subheader("Payment")
        st.write("Manage payment transactions here.")
        # Example content
        payment_method = st.selectbox("Select Payment Method", ["Credit Card", "Debit Card", "PayPal"])
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        if st.button("Process Payment"):
            st.success(f"Processed {payment_method} payment of ${amount:.2f}.")

    with tabs[1]:  # Discount Tab
        st.subheader("Discount")
        st.write("Manage discounts and promotions here.")
        # Example content
        discount_code = st.text_input("Discount Code")
        discount_amount = st.number_input("Discount Amount", min_value=0.0, format="%.2f")
        if st.button("Apply Discount"):
            st.success(f"Discount code '{discount_code}' applied: -${discount_amount:.2f}.")

    with tabs[2]:  # Cottage Tab
        st.subheader("Cottage")
        st.write("Manage cottages and their details here.")
        # Example content
        cottage_name = st.text_input("Cottage Name")
        cottage_status = st.selectbox("Cottage Status", ["Available", "Occupied", "Under Maintenance"])
        if st.button("Update Cottage Status"):
            st.success(f"Updated '{cottage_name}' status to {cottage_status}.")

    with tabs[3]:  # Staff Tab
        st.subheader("Staff")
        st.write("Manage staff information here.")
        # Example content
        staff_name = st.text_input("Staff Name")
        staff_role = st.selectbox("Role", ["Manager", "Housekeeping", "Maintenance"])
        if st.button("Add Staff"):
            st.success(f"Added staff member '{staff_name}' as {staff_role}.")

