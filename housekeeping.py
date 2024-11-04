import mysql.connector
import pandas as pd
import streamlit as st
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def fetch_housekeeping_data():
    """Fetch housekeeping booking data."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            query = """
            SELECT b.book_id, b.cot_id, b.check_out_date, s.staff_id, s.staff_name
            FROM BOOKING b
            JOIN COTTAGE_ATTRIBUTES_RELATION c ON b.cot_id = c.cot_id
            JOIN STAFF s ON b.staff_id = s.staff_id
            WHERE c.ct_id_stat = 3 AND b.payment_status = 2
            """
            df = pd.read_sql(query, connection)
            return df
    except Error as e:
        st.error(f"Error fetching data: {e}")
    finally:
        if connection.is_connected():
            connection.close()

def show_housekeeping():
    """Display housekeeping booking data with payment_status = 2 in Streamlit."""
    df = fetch_housekeeping_data()
    
    if df is not None and not df.empty:
        st.subheader("Housekeeping Bookings")
        st.dataframe(df[['book_id', 'cot_id', 'check_out_date']])

        # Dropdown for staff selection
        staff_list = df[['staff_id', 'staff_name']].drop_duplicates()
        staff_dropdown = st.selectbox("Select Staff", staff_list['staff_name'].tolist())

        # Get the selected staff_id
        selected_staff_id = staff_list.loc[staff_list['staff_name'] == staff_dropdown, 'staff_id'].values[0]

        # Assign staff button
        if st.button("Assign Staff"):
            selected_book_id = st.selectbox("Select Booking ID", df['book_id'].tolist())
            # Here you would implement the logic to assign the staff to the selected booking
            # For example, you could run an UPDATE statement to set the staff_id for the booking
            
            # Placeholder logic for assigning staff
            try:
                connection = mysql.connector.connect(**DB_CONFIG)
                if connection.is_connected():
                    cursor = connection.cursor()
                    update_query = f"""
                    UPDATE BOOKING SET staff_id = %s WHERE book_id = %s
                    """
                    cursor.execute(update_query, (selected_staff_id, selected_book_id))
                    connection.commit()
                    st.success(f"Staff {staff_dropdown} assigned to booking {selected_book_id}.")
            except Error as e:
                st.error(f"Error updating booking: {e}")
            finally:
                if connection.is_connected():
                    connection.close()
    else:
        st.warning("No bookings available for display.")

# Run the app
if __name__ == "__main__":
    st.title("Housekeeping Management")
    show_housekeeping()
