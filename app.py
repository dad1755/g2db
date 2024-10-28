import streamlit as st
import finance
import staff_role
import cottage
import housekeeping
import booking

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Approve Payment", "Manage Staff and Roles", "Manage Cottages", "Housekeeping", "Booking"])

# Load respective sections based on sidebar selection
if page == "Approve Payment":
    finance.approve_payment_section()
elif page == "Manage Staff and Roles":
    staff_role.staff_role_section()
elif page == "Manage Cottages":
    cottage.cottage_section()
elif page == "Housekeeping":
    housekeeping.housekeeping_section()
elif page == "Booking":
    booking.booking_section()
