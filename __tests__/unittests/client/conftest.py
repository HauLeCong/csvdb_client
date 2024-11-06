import pytest
from dbcsv import Connection
import requests


@pytest.fixture(scope="function")
def connection():
    return Connection(path_file="../util_folder/db.sqlite")


class MockResponseSelect:
    @staticmethod
    def json():
        return {
            "data": [
                {"column 1": 1, "column 2": "abc", "column 3": "2024-12-31"},
                {"column 1": 2, "column 2": "def", "column 3": "2024-10-23"},
                {"column 1": 3, "column 2": "ghi", "column 3": "2024-11-02"},
            ],
            "description": {
                "column 1": {"name": "column 1", "type": "integer"},
                "column 2": {"name": "column 2", "type": "string"},
                "column 3": {"name": "column 3", "type": "string"},
            },
        }


class MockResponseCreateTable:
    @staticmethod
    def json():
        return {}


@pytest.fixture
def mock_repsonse(monkeypatch, response_type):
    """
    Request.get() mocked return
    """

    def mock_get(*args, **kwargs):
        if response_type == "select":
            return MockResponseSelect()
        elif response_type == "create":
            return MockResponseCreateTable()

    monkeypatch.setattr(requests, "get", mock_get)
