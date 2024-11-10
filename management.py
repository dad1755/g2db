import streamlit as st
from staff import show_staff_management
from cottage import show_cottage_management  # Importing cottage management function
from discount import show_discount_management
from facilities import show_facilities_management
from payment import show_payment_management
from approve import show_approve_management
from database import show_database_management
from staff_role import show_role_management  # Import the role management function

def show_management():
    """Display the management section with tabs for different functionalities."""
    st.subheader("Management")
    st.write("This is the Management section where you can manage overall operations.")

    # Create tabs for different management functionalities
    tabs = st.tabs(["Approve", "Payment", "Discount", "Cottage", "Cottage Details", "Staff", "Roles", "Database"])  # Added "Roles" tab
    with tabs[0]:
        show_approve_management()
    
    with tabs[1]:  # Payment Tab
        show_payment_management()

    with tabs[2]:  # Discount Tab
        show_discount_management()
       
    with tabs[3]:  # Cottage Tab
        show_cottage_management()  # Call the cottage management function
    
    with tabs[4]:  # Cottage Details
        show_facilities_management()

    with tabs[5]:  # Staff Tab
        show_staff_management()  # Call the staff management function

    with tabs[6]:  # Roles Tab
        show_role_management()  # Call the role management function
    
    with tabs[7]:  # Show Database Tab
        show_database_management()

# Call the management function to display the UI
if __name__ == "__main__":
    show_management()
