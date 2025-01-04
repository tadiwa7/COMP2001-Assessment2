from flask import g, jsonify
from functools import wraps
from roles import get_user_role
import logging

logging.basicConfig(level=logging.DEBUG)

def authorize_user(*allowed_roles):  # Accept multiple roles
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Fetch email from g.user_email
            email = getattr(g, 'user_email', None)
            if not email:
                logging.warning("Missing authenticated user email in context.")
                return jsonify({"error": "Authentication required"}), 401

            # Fetch the user's role
            logging.debug(f"Fetching role for email: {email}")
            user_role = get_user_role(email)
            if not user_role:
                logging.warning(f"No role found for email: {email}")
                return jsonify({"error": "User role not found"}), 403

            # Log the user role and allowed roles
            logging.debug(f"Role found: {user_role}")
            logging.debug(f"User Role: {user_role.lower()}, Allowed Roles: {[role.lower() for role in allowed_roles]}")

            # Check if the user has one of the allowed roles
            if user_role.lower() not in [role.lower() for role in allowed_roles]:
                logging.warning(f"Access denied for user: {email}")
                return jsonify({"error": "Access denied"}), 403

            # Proceed with the function
            return func(*args, **kwargs)
        return wrapper
    return decorator
