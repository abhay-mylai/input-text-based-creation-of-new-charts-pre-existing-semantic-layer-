import time
from superset_client import get_superset_datasets
from vector_store import store_dataset_embeddings

UPDATE_INTERVAL = 120  # Check every 10 minutes

def update_datasets():
    """Fetch datasets from Superset and update vector embeddings."""
    
    while True:
        print("🔄 Checking for new/updated datasets...")

        datasets = get_superset_datasets()

        if not datasets:
            print("❌ No datasets found.")
            return

        print(f"✅ Retrieved {len(datasets)} datasets.")

        for dataset in datasets:
            if not isinstance(dataset, dict):  # Ensure dataset is a dictionary
                print(f"❌ Invalid dataset format: {dataset}")
                continue
            
            dataset_name = dataset.get("table_name", "unknown")
            description = dataset.get("description", dataset_name)

            print(f"📂 Processing dataset: {dataset_name}")

            store_dataset_embeddings(dataset_name, description)

        print("✅ Dataset update complete.")

        print(f"⏳ Waiting {UPDATE_INTERVAL / 60} minutes before next update...\n")
        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    update_datasets()
