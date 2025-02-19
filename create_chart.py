import requests
from config import SUPERSET_URL
from superset_client import get_superset_token, get_csrf_token
import json

def create_chart(chart_config, dashboard_name=None):
    """Creates a chart in Superset and adds it to an existing dashboard if specified."""
    token = get_superset_token()
    csrf_token, cookies = get_csrf_token()

    if not token or not csrf_token:
        print("❌ Cannot create chart without authentication.")
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
        "Referer": SUPERSET_URL,
        "Accept": "application/json",
    }

    session = requests.Session()
    session.cookies.update(cookies)

    # ✅ Step 1: Create the chart
    response = session.post(f"{SUPERSET_URL}/api/v1/chart", json=chart_config, headers=headers)

    if response.status_code == 201:
        chart_id = response.json()["id"]
        chart_url = f"{SUPERSET_URL}/superset/explore/?slice_id={chart_id}"
        print(f"✅ Chart created successfully with ID: {chart_id}")


        return chart_url
    else:
        print(f"❌ Chart creation failed: {response.status_code}, Response: {response.text}")
        return None


def get_dashboard_id(dashboard_name):
    """Fetches the dashboard ID by name."""
    token = get_superset_token()
    csrf_token, cookies = get_csrf_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "X-CSRFToken": csrf_token,
        "Referer": SUPERSET_URL
    }

    session = requests.Session()
    session.cookies.update(cookies)

    response = session.get(f"{SUPERSET_URL}/api/v1/dashboard/", headers=headers)
    
    if response.status_code == 200:
        dashboards = response.json()["result"]
        for dashboard in dashboards:
            if dashboard["dashboard_title"].lower() == dashboard_name.lower():
                return dashboard["id"]
    print(f"❌ Dashboard '{dashboard_name}' not found.")
    return None


