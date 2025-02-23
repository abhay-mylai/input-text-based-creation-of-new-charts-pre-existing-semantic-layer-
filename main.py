from nlp_processor import extract_chart_info
from vector_store import find_best_matching_dataset
from chart_generator import generate_chart_config
from create_chart import create_chart
from superset_client import get_superset_datasets

def main():
    print("🔵 Welcome to the AI Chart Creator!")

    while True:
        user_query = input("Enter your chart request: ").strip().lower()

        # Step 1: Extract chart type
        

        # Step 2: Find best dataset
        dataset_name = find_best_matching_dataset(user_query)
        print(f"🗃 Matching Dataset: {dataset_name}")

        if(dataset_name == None):
            print("Enter a valid dataset name")
            print("Available datasets:")
            datasets = get_superset_datasets()
            i = 1
            for dataset in datasets:
                print(f"{i}. {dataset.get('table_name', 'unknown')}")
                i += 1
            dataset_name = input("Enter the dataset name: ").strip().lower()

        else:
            print("Are you satisfied with this dataset? (y/n): ")
            cont = input().strip().lower()
            if cont == 'n':
                print("Available datasets:")
                datasets = get_superset_datasets()
                i = 1
                for dataset in datasets:
                    if not isinstance(dataset, dict):
                        print(f"❌ Invalid dataset format: {dataset}")
                        continue
                    
                    dataset_name = dataset.get("table_name", "unknown")
                    print(f"Dataset {i}: {dataset_name}")
                    i += 1

                print("🔵 Please specify the dataset you want to use.")
                dataset_name = input("Enter the dataset name: ").strip().lower()

        if not dataset_name:
            print("❌ No relevant dataset found. Try rewording your query.")
            continue

        chart_type = extract_chart_info(user_query)
        print(f"📊 Suggested Chart Type: {chart_type}")
        print("Are you satisfied with this chart type? (y/n)")
        cont = input().strip().lower()
        if cont == 'n':
            print("Available chart types:")
            chart_types = [
                "bar chart", "line chart", "scatter plot", "pie chart", 
                "area chart", "heatmap", "box plot", "histogram", 
                "treemap", "word cloud", "radar chart", "bubble chart"
            ]
            for chart_type in chart_types:
                print(f"- {chart_type}")
            print("\n🔵 Please specify the chart type you want to create.")
            chart_type = input("Enter the chart type: ").strip().lower()

        

        # Step 3: Ask user for chart name
        chart_name = input("Enter a name for your chart: ").strip()
        if not chart_name:
            chart_name = f"{dataset_name} {chart_type} Chart"

       

        # Step 5: Generate chart configuration
        chart_config = generate_chart_config(dataset_name, chart_type)
        chart_config["slice_name"] = chart_name  # Set chart name

        # Step 6: Create chart and add to dashboard
        chart_url = create_chart(chart_config)

        if chart_url:
            print(f"✅ Chart Created Successfully! View it here: {chart_url}")
        else:
            print("❌ Chart creation failed.")

        cont = input("\nDo you want to create another chart? (y/n): ").strip().lower()
        if cont != 'y':
            break

if __name__ == "__main__":
    main()