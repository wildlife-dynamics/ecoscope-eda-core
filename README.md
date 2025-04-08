# Ecoscope EDA core
Common schemas & utilities for event-driven workflows.

---
## Installation
### Install the package using conda, mamba:
```bash
conda install -c https://repo.prefix.dev/ecoscope-workflows ecoscope-eda-core
mamba install -c https://repo.prefix.dev/ecoscope-workflows ecoscope-eda-core
```
### ... or pixi, e.g.:
```bash
pixi init
pixi project channel add https://repo.prefix.dev/ecoscope-workflows
pixi add ecoscope-eda-core
```
### Install the package using pip:
```bash
pip install ecoscope-eda-core
```
---
## Usage
### Messages
Messages are the core of the event-driven architecture. They are used to communicate between different components of the system. Messages are defined using Pydantic models, which provide validation and serialization.


There are two types of messages: `Command` and `Event`. Commands represent an intent (a request to do something), while events represent immutable facts (somthing that already happened). For example, the `RunWorkflow` command represents a request to run a workflow.

### Publishing Messages
Use a `Publisher` to publish messages to the message broker.

#### Example: Publishing a command to trigger a workflow using GCPPubSubPublisher:
```python
from ecoscope_eda_core.publishers import GCPPubSubPublisher
from ecoscope_eda_core.messages import RunWorkflow, RunWorkflowParams

# Create a command message
run_workflow_command = RunWorkflow(
    payload=RunWorkflowParams(
        conda_channel="https://repo.prefix.dev/ecoscope-workflows/",
        conda_package="events",
        conda_package_version="1.2.3",
        command="run",
        invoker_kwargs={
            "mock_io": True,
            "results_url": "gs://bucket/results",
            "filter_events": {"min_x": -98.567, "max_x": 53.234},
        },
    )
)

# Publish the command message to the GCP Pub/Sub topic
publisher = GCPPubSubPublisher(project="your-project")
await publisher.publish(messages=[run_workflow_command], topic="workflow-requests")
await publisher.close()  # Close the publisher when done

# or use it as an async context manager so that it closes automatically
async with GCPPubSubPublisher(project="your-project") as publisher:
    await publisher.publish(messages=[run_workflow_command], topic="workflow-requests")

```
---
## Development
### Setting up your development environment
```bash
pixi install
```
### Building the conda package
```bash
pixi build
```
### Building the Pypi package
```bash
pip install build
python -m build
```

### Release
To release packages for `ecoscope-eda-core` checkout the `main` branch, and then push a new tag:
   ```bash
   $ git tag v0.1.1
   $ git push origin --tags
   ```
The `publish.yml` github workflow will then build and push a new release to both GitHub Releases with conda and pypi packages attached, and will also publish to prefix.dev at
https://prefix.dev/channels/ecoscope-workflows
