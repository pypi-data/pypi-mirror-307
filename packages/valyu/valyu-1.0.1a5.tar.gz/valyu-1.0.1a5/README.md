# Valyu SDK

The Valyu SDK provides easy access to dataset samples from the Valyu Exchange, an AI Data Licensing and Attribution platform.

## Features

- Load dataset samples from the Valyu Exchange
- Load full datasets from the Valyu Exchange

## Installation

Install the Valyu SDK using pip:

```bash
pip install valyu
```

## Usage

To load dataset samples, use the `load_dataset_samples` function:
```python
from valyu import load_dataset_samples

# Load the dataset samples, passing the org_id and dataset_name
# This will download the data to the current working directory under a 'downloads' folder
load_dataset_samples("example_org/example_dataset")
```

To load full datasets, use the `load_dataset` function:
```python
from valyu import load_dataset

# Load the dataset, passing the api_key, dataset_id
# This will download the data to the current working directory under a 'downloads' folder
load_dataset(api_key="your-api-key", dataset_id="example_org/example_dataset")
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.