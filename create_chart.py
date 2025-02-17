import requests
from config import SUPERSET_URL
from superset_client import get_superset_token, get_csrf_token
import re
import json

def create_chart(chart_config):
    """Creates a chart in Superset using the provided configuration."""
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

    response = session.post(f"{SUPERSET_URL}/api/v1/chart", json=chart_config, headers=headers)

    if response.status_code == 201:
        chart_id = response.json()["id"]
        chart_url = f"{SUPERSET_URL}/superset/explore/?slice_id={chart_id}"
        print(f"✅ Chart created successfully! View it here: {chart_url}")

        # ✅ Attach query context to avoid empty query issue
        # attach_query_context(chart_id)

        return chart_url
    else:
        print(f"❌ Chart creation failed: {response.status_code}, Response: {response.text}")
        return None
    

