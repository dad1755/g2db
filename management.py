import streamlit as st
from staff import show_staff_management
from payment import show_payment_management
from discount import show_discount_management
from cottage import show_cottage_management

def show_management():
    """Display the management section with tabs for different functionalities."""
    st.subheader("Management")
    st.write("This is the Management section where you can manage overall operations.")

    # Create tabs for different management functionalities
    tabs = st.tabs(["Payment", "Discount", "Cottage", "Staff"])

    # Load each management function in the corresponding tab
    with tabs[0]:  # Payment Tab
        try:
            show_payment_management()
        except Exception as e:
            st.error(f"Error loading payment management: {e}")

    with tabs[1]:  # Discount Tab
        try:
            show_discount_management()
        except Exception as e:
            st.error(f"Error loading discount management: {e}")

    with tabs[2]:  # Cottage Tab
        try:
            show_cottage_management()
        except Exception as e:
            st.error(f"Error loading cottage management: {e}")

    with tabs[3]:  # Staff Tab
        try:
            show_staff_management()
        except Exception as e:
            st.error(f"Error loading staff management: {e}")

# This is typically how you would call the function in your main app file (app.py):
# if __name__ == "__main__":
#     show_management()
