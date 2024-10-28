import streamlit as st
from db import load_data, save_data

def cottage_section():
    st.header("Manage Cottages")

    cottages = load_data("SELECT * FROM Cottage")

    new_cottage_name = st.text_input("New Cottage Name")
    new_cottage_description = st.text_area("New Cottage Description")
    new_cottage_price = st.number_input("New Cottage Price", min_value=0.0, format="%.2f")
    new_cottage_status = st.selectbox("New Cottage Status", ["available", "occupied"])

    if st.button("Add Cottage"):
        if new_cottage_name and new_cottage_price:
            save_data("""
                INSERT INTO Cottage (cottage_name, cottage_description, cottage_price, cottage_status)
                VALUES (:name, :description, :price, :status)
            """, {
                "name": new_cottage_name, 
                "description": new_cottage_description, 
                "price": new_cottage_price, 
                "status": new_cottage_status
            })
            st.success("Cottage added successfully.")

    for cottage in cottages:
        st.write(f"Cottage ID: {cottage['cottage_id']}, Name: {cottage['cottage_name']}, Status: {cottage['cottage_status']}")
        
        new_name = st.text_input(f"Edit Name for Cottage {cottage['cottage_id']}", cottage['cottage_name'])
        new_description = st.text_area(f"Edit Description for Cottage {cottage['cottage_id']}", cottage['cottage_description'])
        new_price = st.number_input(f"Edit Price for Cottage {cottage['cottage_id']}", value=float(cottage['cottage_price']), format="%.2f")
        new_status = st.selectbox(f"Edit Status for Cottage {cottage['cottage_id']}", ["available", "occupied"], 
                                  index=0 if cottage['cottage_status'] == "available" else 1)
        
        if st.button("Update", key=f"update_cottage_{cottage['cottage_id']}"):
            save_data("""
                UPDATE Cottage SET cottage_name = :name, cottage_description = :description, 
                cottage_price = :price, cottage_status = :status WHERE cottage_id = :cottage_id
            """, {
                "name": new_name, 
                "description": new_description, 
                "price": new_price, 
                "status": new_status, 
                "cottage_id": cottage['cottage_id']
            })
            st.success("Cottage updated.")
        
        if st.button("Delete", key=f"delete_cottage_{cottage['cottage_id']}"):
            save_data("DELETE FROM Cottage WHERE cottage_id = :cottage_id", {"cottage_id": cottage['cottage_id']})
            st.success("Cottage deleted.")
