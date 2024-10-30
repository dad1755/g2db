import streamlit as st
from staff import show_staff_management
from payment import show_payment_management
from discount import show_discount_management
from cottage import show_cottage_management

def show_management():
    st.subheader("Management")
    st.write("This is the Management section where you can manage overall operations.")

    # Create tabs for different management functionalities
    tabs = st.tabs(["Payment", "Discount", "Cottage", "Staff"])

    with tabs[0]:  # Payment Tab
        show_payment_management()
    with tabs[1]:  # Discount Tab
        show_discount_management()
    with tabs[2]:  # Cottage Tab
        show_cottage_management()
    with tabs[3]:  # Staff Tab
        show_staff_management()
