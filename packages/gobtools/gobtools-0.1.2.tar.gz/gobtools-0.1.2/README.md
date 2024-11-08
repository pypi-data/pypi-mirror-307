# GobTools
Library to control and interact with the Goblin ecosystem.

[![Apache-2.0](https://custom-icon-badges.herokuapp.com/badge/license-Apache%202.0-8BB80A.svg?logo=law&logoColor=white)]()
![Github Tag](https://img.shields.io/github/v/tag/Hietan/gobtools)

## What is GobTools?

GobTools streamlines access to GoblinWeaver.\
By simply passing information as arguments to Python functions, requests are sent effortlessly, and responses are returned as dictionaries.

Please refer to the [official repository](https://github.com/Goblin-Ecosystem/goblinWeaver.git) for more details about GoblinWeaver.

## Installation

- pip

Run the following command:

```
pip install git+https://github.com/Hietan/gobtools.git
```

- Rye

Run the following command in a rye project:

```
rye add gobtools --git https://github.com/Hietan/gobtools.git
```

## Usage

> [!TIP]
> GobTools requires that the GoblinWeaver API server is running.\
> Ensure the GoblinWeaver is started before using GobTools.\
> You may need to provide the API server's URL when using GobTools.

### 1. Import

Import the necessary module for creating a controller instance:

```python
from gobtools.weaver.controller import WeaverController
```

### 2. Instance Creation

Create an instance of the controller by specifying the URL of the GoblinWeaver API server.

```python
controller = WeaverController("<your-api-server-url>")
```

> [!NOTE]
> Replace `<your-api-server-url>` with the actual URL for you environment (e.g., "http://localhost:8080") where your GoblinWeaver server is running\

### 3. Get Data

Get all releases of an artifact from org.apache.logging.log4j:log4j-core with added values (`CVE`, `FRESHNESS`).\
The function `get_artifact_releases` sends POST requests to `<your-api-server-url>/artifact/releases`.\
You can receive the results as dictionary.

```python
releases = controller.get_artifact_releases(
    "org.apache.logging.log4j", 
    "log4j-core", 
    ["CVE", "FRESHNESS"]
)
```

Other REST API endpoints can also be accessed through GobTools function.\
For detailed API documentation, please refer to `<your-api-server-url>/swagger-ui/index.html`

### 4. Print Result

By using `json_format`, you can format and display the results.

```python
from gobtools.utils.json import json_format

print(json_format(releases))
```
