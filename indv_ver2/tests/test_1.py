from flask import request
from applications import app
import urllib.request
import unittest


def test_valid_input():  # Testar giltig inmatning som borde ge statuskoden 200
    response = app.post('/result', data=dict(year='2022', month='11', day='01', price_class='SE3'))
    assertEqual(response.status_code, 200)


def test_invalid_input():   # Testar ogiltig inmatning så att användaren hamnar i user_error
    response = app.post('/result', data=dict(year='x', month='11', day='01', price_class='SE3'))
    assertEqual(response.status_code, 302)
    assertIn(b'/user_error', response.location)
