import requests
import os
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

VALYU_INTERMEDIARY_ENDPOINT = 'http://ec2-35-177-58-41.eu-west-2.compute.amazonaws.com:3000'

def load_dataset(api_key, dataset_id, save_path='downloads', node_id='valyu'):
    try:
        """Retrieve and download data from the intermediary service to a specified file path."""
        
        print(f"Fetching dataset {dataset_id}...")

        if node_id == 'valyu':
            intermediary_url = VALYU_INTERMEDIARY_ENDPOINT
        else:
            raise ValueError('Invalid node ID')

        time.sleep(2)
        headers = {'x-api-key': api_key}
        body = {
            "datasetId": dataset_id
        }
    
        # Fetch the manifest URL
        response = requests.post(f"{intermediary_url}/fetchData", headers=headers, json=body)
        response.raise_for_status()

        data = response.json()
        manifest_url = data['presignedURL']
    
        # Download the manifest file
        response = requests.get(manifest_url)
        response.raise_for_status()
        manifest = response.json()

        # Create the save directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)

        # Function to download a single file
        def download_file(file_info):
            # Skip directories
            if file_info['key'].endswith('/'):
                return
            
            file_url = file_info['presignedUrl']
            file_path = os.path.join(save_path, file_info['key'])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file_response = requests.get(file_url)
            with open(file_path, 'wb') as f:
                f.write(file_response.content)

        # Download files concurrently
        with ThreadPoolExecutor() as executor:
            list(tqdm(executor.map(download_file, manifest), total=len(manifest), desc="Downloading files"))

        print(f"\nDataset downloaded successfully into {save_path}.")
    
    except Exception as e:
        raise Exception(f"Error occurred: {e}")
