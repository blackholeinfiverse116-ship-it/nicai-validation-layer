import json

# -----------------------------
# 🔹 LOAD DATASETS SAFE
# -----------------------------
def load_datasets():
    try:
        with open("datasets.json", "r") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return []

        return data

    except FileNotFoundError:
        print("ERROR: datasets.json file not found")
        return []

    except json.JSONDecodeError:
        print("ERROR: datasets.json is invalid JSON")
        return []


# -----------------------------
# 🔹 GET DATASET (SAFE LOOKUP)
# -----------------------------
def get_dataset(dataset_id):

    if not dataset_id:
        return None

    datasets = load_datasets()

    for dataset in datasets:
        if isinstance(dataset, dict) and dataset.get("dataset_id") == dataset_id:
            return dataset

    return None
