import logging
import connexion
from flask_cors import CORS
from flask import request, g
from middleware import authorize_user

# Configure logging
logging.basicConfig(level=logging.DEBUG)
print("Flask app is starting...")

# Create Connexion app instance
app = connexion.App(__name__, specification_dir="./")

# Enable CORS
CORS(app.app)

# Add the API
app.add_api(
    "swagger.yml",
    arguments={"title": "TrailService Flask REST API"},
    options={"swagger_ui": True}
)

# Add middleware for authentication and authorization
@app.app.before_request  # Use app.app to access the Flask instance
def check_auth():
    """
    Middleware to handle authentication.
    Ensures that Email and Password are present in the request headers.
    Verifies credentials and stores the email in Flask's global context.
    """
    logging.debug(f"check_auth triggered for path: {request.path}")
    logging.debug(f"All headers: {dict(request.headers)}")

    email = request.headers.get('Email')
    password = request.headers.get('Password')

    # Log the received credentials for debugging (avoid logging sensitive data in production)
    logging.debug(f"Received Email: {email}, Password: {password}")

    if not email or not password:
        logging.error("Missing authentication headers")
        return {"error": "Missing authentication headers"}, 401

    from auth import verify_credentials
    if not verify_credentials(email, password):
        logging.error("Invalid credentials provided")
        return {"error": "Invalid credentials"}, 401

    # Store the authenticated user's email in Flask's global context
    g.user_email = email
    logging.debug(f"User authenticated and g.user_email set: {g.user_email}")

# Log all registered routes
for rule in app.app.url_map.iter_rules():
    logging.debug(f"Route: {rule.rule}, Endpoint: {rule.endpoint}, Methods: {rule.methods}")

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
