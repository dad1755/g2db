import streamlit as st

def show_management():
    st.subheader("Management")
    st.write("This is the Management section where you can manage overall operations.")
    
    # Example: Management statistics
    total_bookings = 120
    available_cottages = 15
    
    st.write(f"### Total Bookings: {total_bookings}")
    st.write(f"### Available Cottages: {available_cottages}")

    # Add more management functionality here (charts, tables, etc.)
