import os
import streamlit as st
import pandas as pd
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text

# Retrieve the service account JSON from st.secrets
service_account_info = st.secrets["google_cloud"]["credentials"]

# Write the JSON to a file
with open("service_account.json", "w") as f:
    f.write(service_account_info)

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

# Retrieve database credentials from st.secrets
INSTANCE_CONNECTION_NAME = st.secrets["database"]["instance_connection_name"]
DB_USER = st.secrets["database"]["db_user"]
DB_PASSWORD = st.secrets["database"]["db_password"]
DB_NAME = st.secrets["database"]["db_name"]

# Initialize Connector object
connector = Connector()

# Function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )
    return conn

# SQLAlchemy engine for creating database connection
engine = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Fetch housekeeping data function with the new connection method
def fetch_housekeeping_data():
    """Fetch housekeeping booking data."""
    try:
        with engine.connect() as connection:
            query = """
            SELECT b.book_id, b.cot_id, b.check_out_date, s.staff_id, s.staff_name
            FROM BOOKING b
            JOIN COTTAGE_ATTRIBUTES_RELATION c ON b.cot_id = c.cot_id
            JOIN STAFF s ON b.staff_id = s.staff_id
            WHERE c.ct_id_stat = 3 AND b.payment_status = 2
            """
            df = pd.read_sql(query, connection)
            return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")

# Show housekeeping function for displaying data in Streamlit
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
                with engine.connect() as connection:
                    update_query = text("""
                    UPDATE BOOKING SET staff_id = :staff_id WHERE book_id = :book_id
                    """)
                    connection.execute(update_query, {'staff_id': selected_staff_id, 'book_id': selected_book_id})
                    st.success(f"Staff {staff_dropdown} assigned to booking {selected_book_id}.")
            except Exception as e:
                st.error(f"Error updating booking: {e}")
    else:
        st.warning("No bookings available for display.")

# Run the app
if __name__ == "__main__":
    st.title("Housekeeping Management")
    show_housekeeping()
