import streamlit as st
from staff import show_staff_management
from cottage import show_cottage_management  # Importing cottage management function
from discount import show_discount_management
from facilities import show_facilities_management
from payment import show_payment_management

def show_management():
    """Display the management section with tabs for different functionalities."""
    st.subheader("Management")
    st.write("This is the Management section where you can manage overall operations.")

    # Create tabs for different management functionalities
    tabs = st.tabs(["Payment", "Discount", "Cottage", "Cottage Details", "Staff"])  # Added comma

    with tabs[0]:  # Payment Tab
        show_payment_management()

    with tabs[1]:  # Discount Tab
        show_discount_management()
       
    with tabs[2]:  # Cottage Tab
        show_cottage_management()  # Call the cottage management function
    
    with tabs[3]:  # Cottage Details
        show_facilities_management()

    with tabs[4]:  # Staff Tab
        show_staff_management()  # Call the staff management function

# Call the management function to display the UI
if __name__ == "__main__":
    show_management()
