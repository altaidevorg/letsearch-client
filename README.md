# letsearch-client

![logo](./assets/logo.jpg)

A Python client for [letsearch](https://github.com/monatis/letsearch) — the vector DB so easy, even your grandparents can build a RAG system 😁.

## ❓ What is this?

`letsearch-client` provides an easy-to-use Python interface to interact with a running `letsearch` server. With this client, you can programmatically manage collections, perform health checks, and run searches without worrying about HTTP requests or JSON parsing.

⚠️ **Note**: The main `letsearch-` project and this client are still under active development. Rapid changes may occur as `letsearch` evolves.

---

## 🖼️ Features

- Perform health checks on your `letsearch` server.
- List and retrieve collection information.
- Run searches on indexed collections.
- Automatically handle errors and raise exceptions when needed.

---

## 🏎️ Installation

Install `letsearch-client` via uv (recommended) or pip:

```sh
uv add letsearch-client
```

or:

```sh
pip install letsearch-client
```

If you want to convert models to use with `letsearch`, you need to install additional conversion-related dependencies:

```sh
pip install letsearch-client[conversion]
```

---

## 🚀 Quickstart

Here’s how you can use the `LetsearchClient` to interact with a running [letsearch](https://github.com/monatis/letsearch) instance:

### Setup

```python
from letsearch_client import LetsearchClient

# Initialize the client
client = LetsearchClient(letsearch_url="http://localhost:7898", raise_for_status=True)

# Always remember to close the client or use it in a context manager
client.close()
```

Alternatively, use a context manager to ensure proper cleanup:

```python
from letsearch_client import LetsearchClient

with LetsearchClient(letsearch_url="http://localhost:7898") as client:
    health = client.healthcheck()
    print(health)
```

---

### Example Usage

#### Health Check

```python
response = client.healthcheck()
print(response)  # Outputs server health status and version
```

#### List Collections

```python
collections = client.get_collections()
print(collections)  # Outputs a list of available collections
```

#### Retrieve Collection Info

```python
collection_info = client.get_collection("example_collection")
print(collection_info)  # Outputs details about the specified collection
```

#### Search in a Collection

```python
results = client.search(
    collection_name="example_collection",
    column_name="content",
    query="example query",
    limit=5
)
print(results)  # Outputs search results
```

---

## 🧭 Roadmap

The roadmap of the `letsearch` project can be found in [its repository](https://github.com/monatis/letsearch).
This client is intended to be a thin wrapper around the functionality of `letsearch`,
and it will continue to implement new features as `letsearch` evolves.

---

## 🌡️ Tests

Run the client’s test suite using:

```sh
pytest
```
