import streamlit as st
from booking import reservation_section
from housekeeping import management_section
from finance import payment_section

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Reservation", "Payment", "Management"])

if page == "Reservation":
    reservation_section()
elif page == "Payment":
    payment_section()
elif page == "Management":
    management_section()
