# PlanQK Service SDK

## Installation

The package is published on PyPI and can be installed via `pip`:

```bash
pip install --upgrade planqk-service-sdk
```

## Usage

```python
from planqk.service.client import PlanqkServiceClient

consumer_key = "..."
consumer_secret = "..."
service_endpoint = "..."

client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)

# prepare your input data and parameters
data = {"input": {"a": 1, "b": 2}}
params = {"param1": "value1", "param2": "value2"}

# start the execution
job = client.start_execution(data=data, params=params)

# check the job details
print(job.id, job.status)

# cancel the job
job.cancel()

# retrieve the job result
result = job.result()

# retrieve the job's interim results
interim_results = job.interim_results()
```

## Development

To create a new Conda environment, run:

```bash
conda env create -f environment.yml
```

Then, to activate the environment:

```bash
conda activate planqk-service-sdk
```

To install the package in development mode, run:

```bash
pip install -e .
```
