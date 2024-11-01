def confirm_payment(book_id, staff_id, cottage_id):
    """Confirm payment for a booking, update booking and cottage status."""
    try:
        book_id = int(book_id)
        staff_id = int(staff_id)
        cottage_id = int(cottage_id)

        # Insert a new record into PAYMENT_CONFIRMATION
        payment_query = """
            INSERT INTO PAYMENT_CONFIRMATION (book_id, staff_id)
            VALUES (%s, %s)
        """
        execute_query(payment_query, (book_id, staff_id))

        # Delete related entries in PAYMENT_CONFIRMATION for non-confirmed bookings
        delete_payment_confirmations_query = """
            DELETE FROM PAYMENT_CONFIRMATION 
            WHERE book_id IN (
                SELECT book_id FROM BOOKING WHERE cot_id = %s AND book_id != %s
            )
        """
        execute_query(delete_payment_confirmations_query, (cottage_id, book_id))

        # Now delete all related bookings with the same cot_id, except the confirmed booking
        delete_bookings_query = """
            DELETE FROM BOOKING WHERE cot_id = %s AND book_id != %s
        """
        execute_query(delete_bookings_query, (cottage_id, book_id))

        # Update ct_id_stat to 3 in COTTAGE_ATTRIBUTES_RELATION for the confirmed booking's cot_id
        update_cottage_status_query = """
            UPDATE COTTAGE_ATTRIBUTES_RELATION 
            SET ct_id_stat = 3 
            WHERE cot_id = %s
        """
        execute_query(update_cottage_status_query, (cottage_id,))
        
        st.success("Payment confirmed, related bookings deleted, and cottage status updated.")

    except Error as e:
        st.error(f"Error confirming payment: {e}")
