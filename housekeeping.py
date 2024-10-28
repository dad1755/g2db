import streamlit as st
from sqlalchemy import create_engine, text

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

# Housekeeping Section
def housekeeping_section():
    st.header("Housekeeping Management")
    
    # View housekeeping requests
    housekeeping_requests = load_data("SELECT hk_id, cottage_id, status FROM Housekeeping")
    for request in housekeeping_requests:
        st.write(f"Housekeeping ID: {request['hk_id']}, Cottage ID: {request['cottage_id']}, Status: {request['status']}")

    # Manual update of status
    cottage_id = st.selectbox("Select Cottage ID for Housekeeping", [request['cottage_id'] for request in housekeeping_requests])
    staff_id = st.text_input("Enter Staff ID")
    if st.button("Mark as Available"):
        update_status_query = "UPDATE Housekeeping SET status = 'available' WHERE cottage_id = :cottage_id AND staff_id = :staff_id"
        save_data(update_status_query, {"cottage_id": cottage_id, "staff_id": staff_id})
        st.success("Cottage status updated to available.")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Housekeeping"])

if page == "Housekeeping":
    housekeeping_section()
