import requests
from config import SUPERSET_URL
from superset_client import get_superset_token, get_csrf_token
import json

def get_dataset_id(dataset_name):
    """Fetches the dataset ID from Superset."""
    token = get_superset_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{SUPERSET_URL}/api/v1/dataset/", headers=headers)
    
    if response.status_code == 200:
        datasets = response.json()["result"]
        for dataset in datasets:
            if dataset["table_name"] == dataset_name:
                return dataset["id"]  # ✅ Return the correct dataset ID
    
    print(f"❌ Dataset '{dataset_name}' not found in Superset.")
    return None

def get_dataset_columns(dataset_id):
    token = get_superset_token()
    csrf_token, cookies = get_csrf_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "X-CSRFToken": csrf_token,
        "Referer": SUPERSET_URL,
        "Accept": "application/json",
    }
    response = requests.get(f"{SUPERSET_URL}/api/v1/dataset/{dataset_id}", headers=headers)
    
    if response.status_code == 200:
        dataset_info = response.json()["result"]
        
        # ✅ Extract columns
        columns = [col["column_name"] for col in dataset_info.get("columns", [])]
        
        # ✅ Extract available metrics
        metrics = [metric["metric_name"] for metric in dataset_info.get("metrics", [])]
        
        print("✅ Available columns:", columns)
        print("✅ Available metrics:", metrics)

        return columns, metrics
    else:
        print(f"❌ Failed to fetch dataset info: {response.text}")
        return [], []


def generate_chart_config(dataset_name, chart_type, groupby=None, metrics=None, row_limit=1000, order_by=None, x_axis=None, y_axis=None):
    """Generates a flexible chart configuration for any dataset and query."""

    dataset_id = get_dataset_id(dataset_name)
    if not dataset_id:
        return None

    # ✅ Fetch dataset columns and available metrics
    _, available_metrics = get_dataset_columns(dataset_id)

    # ✅ Use available metrics or default to COUNT(*)
    if not metrics:
        metrics = ["COUNT(*)"] if "COUNT(*)" in available_metrics else available_metrics[:1]  # Fallback to first metric
    
    if not metrics:
        print("❌ No valid metrics found for the dataset. Cannot create chart.")
        return None
    
    # ✅ Map chart types correctly
    chart_type_map = {
        "scatter plot": "scatter",
        "line chart": "line",
        "bar chart": "bar",
        "pie chart": "pie"
    }
    
    viz_type = chart_type_map.get(chart_type.lower(), chart_type.lower().replace(" ", "_"))

    chart_config = {
        "slice_name": f"{dataset_name} Chart",
        "datasource_id": dataset_id,
        "datasource_type": "table",
        "viz_type": viz_type,
        "params": json.dumps({
            "datasource": f"{dataset_id}__table",
            "viz_type": viz_type,
            "metrics": metrics,  # ✅ Ensure valid metrics
            "groupby": groupby if groupby else [],
            "row_limit": row_limit,
            "orderby": order_by if order_by else [],
            "time_range": "No filter",
            "x_axis": x_axis,
            "y_axis": y_axis
        })
    }
    return chart_config