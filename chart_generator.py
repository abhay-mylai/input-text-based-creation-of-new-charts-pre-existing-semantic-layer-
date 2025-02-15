import requests
from config import SUPERSET_URL
from superset_client import get_superset_token

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

def generate_chart_config(dataset_name, chart_type):
    """Generates a valid chart configuration."""
    dataset_id = get_dataset_id(dataset_name)
    if not dataset_id:
        return None

    chart_config = {
        "slice_name": f"{dataset_name} Chart",
        "datasource_id": dataset_id,  # ✅ Use numeric ID
        "datasource_type": "table",   # ✅ Must specify table
        "viz_type": chart_type.replace(" ", "_"),  
        # "groupby": ["country"],  # ✅ Use valid column names
        # "metrics": ["count"],  # ✅ Basic metric (modify if needed)
        # "row_limit": 1000 
    }
    return chart_config
