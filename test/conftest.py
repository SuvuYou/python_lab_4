import pytest
from flask import Flask
from rest_api import app

@pytest.fixture
def client():
    with app.app_context():
        from app import views

    yield app.test_client()