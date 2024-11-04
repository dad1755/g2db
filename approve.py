def confirm_payment(book_id, staff_id, cottage_id):
    """Confirm payment and update the database accordingly."""
    try:
        # Convert parameters to standard Python int
        book_id = int(book_id)
        staff_id = int(staff_id)
        cottage_id = int(cottage_id)

        # 1. Update the payment status to 2
        update_query = """
            UPDATE BOOKING 
            SET payment_status = 2 
            WHERE book_id = %s
        """
        execute_query(update_query, (book_id,))

        # 2. Check how many bookings exist for the same cottage
        count_query = """
            SELECT COUNT(*) AS booking_count 
            FROM BOOKING 
            WHERE cot_id = %s
        """
        count_result = fetch_data(count_query, (cottage_id,))
        booking_count = count_result[0]['booking_count'] if count_result else 0

        # 3. Proceed with deletion if there are multiple bookings
        if booking_count > 1:
            # Deleting other bookings for the same cottage except the confirmed one
            delete_query = """
                DELETE FROM BOOKING 
                WHERE cot_id = %s AND book_id != %s
            """
            execute_query(delete_query, (cottage_id, book_id))
            st.success("Other bookings deleted successfully.")
        else:
            st.info("Only one booking exists for this cottage. No deletions required.")

        # 4. Insert a new record into PAYMENT_CONFIRMATION
        insert_query = """
            INSERT INTO PAYMENT_CONFIRMATION (book_id, staff_id) 
            VALUES (%s, %s)
        """
        execute_query(insert_query, (book_id, staff_id))

        # Success message
        st.success("Payment confirmed successfully.")
        
    except Exception as e:
        st.error(f"An error occurred while confirming payment: {e}")
