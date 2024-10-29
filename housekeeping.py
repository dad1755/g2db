import streamlit as st

def show_housekeeping():
    st.subheader("House Keeping")
    st.write("This is the House Keeping section where you can manage housekeeping tasks.")
    
    # Example: Listing housekeeping tasks
    tasks = ["Clean cottage", "Change linens", "Restock supplies"]
    
    st.write("### Current Tasks:")
    for task in tasks:
        st.write(f"- {task}")

    # Add a button to mark a task as complete
    if st.button("Mark Task Complete"):
        st.success("Task marked as complete!")
