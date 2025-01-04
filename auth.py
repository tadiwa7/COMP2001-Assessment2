import requests

def verify_credentials(email, password):
    auth_api_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
    payload = {"email": email,"password": password}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(auth_api_url, json=payload)

    if response.status_code == 200:
        return response.json() == ["Verified", "True"]
    return False
