import streamlit as st
from sqlalchemy import create_engine, text
import booking  # Import booking module for reservation functionality
import finance  # Import finance module
import housekeeping  # Import housekeeping module

# Database connection setup
DATABASE_URL = "mysql+mysqlconnector://sql12741294:Lvu9cg9kGm@sql12.freemysqlhosting.net:3306/sql12741294"
engine = create_engine(DATABASE_URL)

# Load data from MySQL
def load_data(query, parameters=None):
    with engine.connect() as connection:
        result = connection.execute(text(query), parameters or {})
        return [dict(row) for row in result]

def save_data(query, parameters=None):
    with engine.connect() as connection:
        connection.execute(text(query), parameters or {})

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Reservation", "Housekeeping", "Finance"])

# Call sections based on sidebar selection
if page == "Reservation":
    booking.main()  # Call the main function from booking.py
elif page == "Housekeeping":
    housekeeping.housekeeping_section()  # Call housekeeping section
elif page == "Finance":
    finance.finance_section()  # Call finance section
