import logging
from sql_connection import get_db_connection  

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_user_role(email):
    """
    Fetch the role of a user based on their email address from the database.

    Args:
        email (str): The email address of the user.

    Returns:
        str or None: The role of the user if found, otherwise None.
    """
    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Log the query execution
        logging.debug(f"Fetching role for email: {email}")

        # Query to fetch the role based on email
        query = "SELECT Role FROM CW2.Users WHERE Email_address = ?"
        cursor.execute(query, (email,))
        role = cursor.fetchone()

        # Log the retrieved role
        logging.debug(f"Role found: {role[0] if role else 'None'}")

        # Return the role or None if not found
        return role[0].lower() if role else None
    except Exception as e:
        # Log any errors during execution
        logging.error(f"Error fetching role for email {email}: {e}")
        return None
    finally:
        # Ensure the connection is always closed
        if conn:
            conn.close()
