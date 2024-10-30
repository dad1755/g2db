# management.py
import streamlit as st
from staff import show_staff_management


def show_management():
    """Display the management section with tabs for different functionalities."""
    st.subheader("Management")
    st.write("This is the Management section where you can manage overall operations.")

    # Create tabs for different management functionalities
    tabs = st.tabs(["Payment", "Discount", "Cottage", "Staff"])

    # Load each management function in the corresponding tab
    with tabs[0]:  # Payment Tab

    with tabs[1]:  # Discount Tab

    with tabs[2]:  # Cottage Tab

    with tabs[3]:  # Staff Tab
        show_staff_management()
