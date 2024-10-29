import streamlit as st

# Set the title of the app
st.title("Cottage Booking System")

# Create a sidebar with three options
st.sidebar.title("Menu")
option = st.sidebar.radio("Select an option:", ("Booking", "House Keeping", "Management"))

# Display content based on the selected option
if option == "Booking":
    st.subheader("Booking")
    st.write("This is the Booking section where you can manage your cottage bookings.")
    # Add more components related to Booking here

elif option == "House Keeping":
    st.subheader("House Keeping")
    st.write("This is the House Keeping section where you can manage housekeeping tasks.")
    # Add more components related to House Keeping here

elif option == "Management":
    st.subheader("Management")
    st.write("This is the Management section where you can manage the overall operations.")
    # Add more components related to Management here

# Optional: Add a footer or other components
st.sidebar.info("This is a simple cottage booking management application.")
