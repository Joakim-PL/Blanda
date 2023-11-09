from flask import Flask, render_template
from applications.app import is_valid_date, result
import pytest
from app import app

def test_index_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert 'index.html' in response.data

def test_valid_date():
    assert is_valid_date('2022', '11', '15') == True


def test_invalid_date():
    result = is_valid_date('2022', '13', '15')
    assert result == False, f"ska få false då den inte ska tillåta att lägga 13 som månad {result}"

def test_invalid_date_error():
    client = app.test_client()
    response = client.get('/user_error')
    assert response.status_code == 404
    assert 'error.html' in response.data

