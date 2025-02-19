from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_chart_info(user_input):
    labels = ["bar chart", "line chart", "scatter plot", "pie chart"]
    result = classifier(user_input, labels)
    return result['labels'][0]

