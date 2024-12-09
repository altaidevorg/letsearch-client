import pytest
from letsearch_client import LetsearchClient


@pytest.fixture
def client():
    client = LetsearchClient()
    return client


def test_healthcheck(client):
    res = client.healthcheck()
    assert res.status == "ok"


def test_collections(client):
    result = client.get_collections()
    assert len(result.collections) > 0
    assert result.collections[0].name is not None


def test_collection(client):
    result = client.get_collection("test2")
    assert result.name == "test2"


def test_search(client):
    result = client.search("test2", "context", "something", 10)
    assert len(result.results) == 10
