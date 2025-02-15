import requests
from config import SUPERSET_URL
from superset_client import get_superset_token, get_csrf_token

def create_chart(chart_config):
    """Creates a chart in Superset using the provided configuration."""
    token = get_superset_token()
    csrf_token, cookies = get_csrf_token()  # ✅ Get cookies along with CSRF token

    if not token or not csrf_token:
        print("❌ Cannot create chart without authentication.")
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,  # ✅ CSRF token in header
        "Referer": SUPERSET_URL,    # ✅ Ensure Superset recognizes the request
        "Accept": "application/json",
    }

    print(f"DEBUG: CSRF Token in Header: {csrf_token}")  # ✅ Debugging output

    session = requests.Session()
    session.cookies.update(cookies)  # ✅ Set cookies

    response = session.post(f"{SUPERSET_URL}/api/v1/chart", json=chart_config, headers=headers)

    if response.status_code == 201:
        chart_id = response.json()["id"]
        print(f"✅ Chart created successfully! View it here: {SUPERSET_URL}/superset/explore/?slice_id={chart_id}")
        return f"{SUPERSET_URL}/superset/explore/?slice_id={chart_id}"
    else:
        print(f"❌ Chart creation failed: {response.status_code}, Response: {response.text}")
        return None
