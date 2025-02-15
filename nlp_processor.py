from transformers import pipeline
from chart_generator import get_dataset_id

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_chart_info(user_input):
    labels = ["bar chart", "line chart", "scatter plot", "pie chart"]
    result = classifier(user_input, labels)
    return result['labels'][0]

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
        "groupby": ["country"],  # ✅ Use valid column names
        "metrics": [{"metric_name": "count"}],  # ✅ Correct format
        "row_limit": 1000
    }
    return chart_config
