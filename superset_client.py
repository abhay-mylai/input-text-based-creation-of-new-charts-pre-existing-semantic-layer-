import requests
import jwt
import json
from config import SUPERSET_URL, USERNAME, PASSWORD, SECRET_KEY

def get_superset_token():
    auth_url = f"{SUPERSET_URL}/api/v1/security/login"
    response = requests.post(auth_url, json={"username": USERNAME, "password": PASSWORD, "provider": "db"})

    if response.status_code == 200:
        token = response.json().get("access_token")
        if not token:
            raise Exception("❌ No access token received from Superset.")

        # Decode token for debugging
        decoded_token = jwt.decode(token, options={"verify_signature": False})

        # Convert 'sub' to string if necessary
        if "sub" in decoded_token and not isinstance(decoded_token["sub"], str):
            decoded_token["sub"] = str(decoded_token["sub"])  # Convert it to a string
            token = jwt.encode(decoded_token, key=SECRET_KEY, algorithm="HS256")  # Re-encode token

        return token
    else:
        raise Exception(f"❌ Authentication Failed: {response.status_code} - {response.text}")

def get_csrf_token():
    """Fetch the CSRF token from Superset using authentication."""
    token = get_superset_token()
    if not token:
        print("❌ Cannot fetch CSRF token without authentication.")
        return None, None  # Return both CSRF token and cookies

    csrf_url = f"{SUPERSET_URL}/api/v1/security/csrf_token/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Referer": SUPERSET_URL,  # ✅ Ensure Referer is included
    }

    try:
        session = requests.Session()
        response = session.get(csrf_url, headers=headers)
        response.raise_for_status()

        csrf_token = response.json().get("result")
        if not csrf_token:
            print("❌ CSRF token retrieval failed. No token received.")
            return None, None

        # print(f"✅ CSRF Token retrieved successfully: {csrf_token}")
        return csrf_token, session.cookies  # ✅ Return CSRF token & cookies

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get CSRF token: {response.status_code} - {response.text}")
        return None, None


def get_superset_datasets():
    """Fetches the list of datasets from Superset."""
    token = get_superset_token()
    csrf_token, cookies = get_csrf_token()  # ✅ Get cookies separately

    if not token or not csrf_token:
        print("❌ Cannot fetch datasets without authentication.")
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "X-CSRFToken": csrf_token,  # ✅ Extract string, not tuple
        "Referer": SUPERSET_URL,
        "Accept": "application/json",
    }

    session = requests.Session()
    session.cookies.update(cookies)  # ✅ Set cookies

    datasets_url = f"{SUPERSET_URL}/api/v1/dataset/"

    try:
        response = session.get(datasets_url, headers=headers)
        response.raise_for_status()  # ✅ Raise error for HTTP failures
        return response.json()["result"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch datasets: {e}")
        return None  # ✅ Prevents 'response' being unassigned
