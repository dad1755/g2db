import streamlit as st

def show_booking():
    st.subheader("Booking")
    st.write("This is the Booking section where you can manage your cottage bookings.")
    
    # Add booking form example
    with st.form(key='booking_form'):
        name = st.text_input("Name")
        date = st.date_input("Check-in Date")
        nights = st.number_input("Number of Nights", min_value=1)
        submit_button = st.form_submit_button("Book Now")
        
        if submit_button:
            st.success(f"Booking confirmed for {name} from {date} for {nights} night(s).")
