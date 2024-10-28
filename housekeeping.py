import streamlit as st
from db import load_data, save_data

def management_section():
    st.header("Cottage Maintenance and Housekeeping")

    # Maintenance requests
    maintenance_requests = load_data("SELECT maintenance_id FROM Maintenance WHERE status = 'requested'")
    maintenance_request = st.selectbox("Maintenance", [m['maintenance_id'] for m in maintenance_requests])
    if st.button("Mark Maintenance as Completed"):
        update_maintenance_query = "UPDATE Maintenance SET status = 'completed' WHERE maintenance_id = :maintenance_id"
        save_data(update_maintenance_query, {"maintenance_id": maintenance_request})
        st.success("Maintenance completed.")

    # Housekeeping requests
    housekeeping_requests = load_data("SELECT hk_id FROM Housekeeping WHERE status = 'pending'")
    housekeeping_request = st.selectbox("Housekeeping", [h['hk_id'] for h in housekeeping_requests])
    if st.button("Mark Housekeeping as Completed"):
        update_housekeeping_query = "UPDATE Housekeeping SET status = 'completed' WHERE hk_id = :hk_id"
        save_data(update_housekeeping_query, {"hk_id": housekeeping_request})
        st.success("Housekeeping completed.")

