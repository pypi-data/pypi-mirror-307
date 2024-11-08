import logging
import requests
import os
from huggingface_hub import HfApi, list_datasets
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


headers = {"Authorization": f"Bearer {os.environ.get('HF_API_KEY')}"} if os.environ.get('HF_API_KEY') else {}

API_URL = "https://huggingface.co/api/datasets/"

def croissant_dataset(dsid,use_api_key=True):
    """
    Retrieves the 'croissant' metadata file for a specified dataset from Hugging Face.

    Args:
        dsid (str): The unique identifier of the dataset from which to retrieve the 'croissant' metadata file.
        use_api_key (bool): A boolean determining if an API Key will be used to make the requests to Huggingface.

    Returns:
        dict: A JSON response containing metadata and details from the 'croissant' file for the specified dataset.
        
    """
    if use_api_key:
        response = requests.get(API_URL + dsid + "/croissant", headers=headers)
    else:
        response = requests.get(API_URL + dsid + "/croissant")
        
    return response.json()

def get_datasets(limit):
    """
    Retrieves a list of datasets hosted on Hugging Face, up to the specified limit.

    Args:
        limit (int): The maximum number of datasets to retrieve.

    Returns:
        list: A list of dataset objects, each containing metadata for a Hugging Face dataset.
    """
    return list(list_datasets(limit=limit))

def fetch_datasets(limit,use_api_key=True):
    """
    Fetches metadata for multiple datasets from Hugging Face, including the 'croissant' metadata file for each.

    This is a wrapper function that retrieves a limited list of datasets using `get_datasets` 
    and then fetches the 'croissant' metadata for each dataset.

    Args:
        limit (int): The maximum number of datasets to retrieve and process.
        use_api_key (bool): A boolean determining if an API Key will be used to make the requests to Huggingface.

    Returns:
        list: A list of dictionaries, each containing the 'croissant' metadata for a dataset.
    """
    logging.info(f"Fetching {limit} datasets from Hugging Face.")

    try:
        datasets = get_datasets(limit)
        logging.info(f"Got {len(datasets)} datasets from Hugging Face.")
    except Exception as e:
        logging.error(f"Error fetching datasets: {e}")
        return []

    # Create a thread pool
    results = []
    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit each dataset to the thread pool
            futures = {executor.submit(croissant_dataset, dataset.id): dataset.id for dataset in datasets}            # Use tqdm to show progress
            for future in tqdm(as_completed(futures), total=len(futures), desc="Fetching datasets"):
                dataset_id = futures[future]
                try:
                    results.append(future.result())
                except Exception as e:
                    logging.error(f"Error processing dataset {dataset_id}: {e}")

    except KeyboardInterrupt:
        logging.warning("Process interrupted by user. Shutting down...")
        executor.shutdown(wait=False)  # Cancel remaining futures
        raise  # Reraise the exception to exit immediately

    return results