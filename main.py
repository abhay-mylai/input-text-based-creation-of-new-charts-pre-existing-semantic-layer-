from nlp_processor import extract_chart_info
from vector_store import find_best_matching_dataset
from chart_generator import generate_chart_config
from create_chart import create_chart

def main():
    print("🔵 Welcome to the AI Chart Creator!")

    while True:
        user_query = input("Enter your chart request: ").strip().lower()

        # Step 1: Extract chart type
        chart_type = extract_chart_info(user_query)
        print(f"📊 Suggested Chart Type: {chart_type}")

        # Step 2: Find best dataset
        dataset_name = find_best_matching_dataset(user_query)
        if not dataset_name:
            print("❌ No relevant dataset found. Try rewording your query.")
            continue

        print(f"🗃 Matching Dataset: {dataset_name}")

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
