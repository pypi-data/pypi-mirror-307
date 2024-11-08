# IonQ SDK

The IonQ SDK provides tools for interacting with the IonQ platform, enabling users to manage backends, jobs, and quantum circuits programmatically.

## Features

- **Backend Management**: Access and manage quantum computers.
- **Job Management**: Submit, manage, and retrieve quantum jobs.
- **Quantum Circuit Design**: Build and manipulate quantum circuits for execution (not a focus of this SDK).

## Installation

This SDK requires Python 3.9 or later. Below are the steps to install and set it up using a virtual environment and Poetry.

### Prerequisites

Ensure you have Python and Poetry installed. Poetry is a tool for dependency management and packaging in Python. To install Poetry, you can use the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Installing the SDK

To install the SDK, clone the repository, create a virtual environment, and install the dependencies using Poetry:

```bash
# Clone the repository
git clone https://github.com/ionq/python-ionq.git
cd python-ionq

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies using Poetry
pip install poetry
poetry install

# Optional: Install with extras for development
poetry install -E all
```

## Quick Start

Here is a quick example to get you started with the IonQ SDK.

### Initialize the SDK

First, set up your API key and initialize the Backend object:

```python
from ionq import Backend

backend = Backend(api_key='your_api_key_here')
```

### List Available Backends

You can list the available backends like this:

```python
backends = backend.get_backends()
print(backends)
```

### Create and Submit a Job

To create a circuit and submit a job:

```python
from ionq import Circuit, Job

circuit = Circuit(2)
circuit.h(0)
circuit.cx(0, 1)

job = Job(api_key='your_api_key_here')
job_details = job.create_job(circuit=circuit)
print(job_details)
```

### Retrieve Job Results

To check the results of a submitted job:

```python
results = job.get_job_results(job_id='your_job_id_here')
print(results)
```

## Documentation

For more detailed information and API specifications, please refer to the [official documentation](https://docs.ionq.com/api-reference/).

## Contributing

Contributions are welcome! Please read our contributing guidelines to get started.
