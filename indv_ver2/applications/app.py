from flask import Flask, render_template, request, redirect
import requests
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    price_class = request.form['price_class']

    if not year.isdigit() or not month.isdigit() or not day.isdigit():
        return redirect('/user_error')  # Felinmatning så omredigeras man till user_error.html

    if is_valid_date(year, month, day):
        pass  # Om det är giltig inmatning så fortsätter programmet
    else:
        return redirect('/user_error')  # Ogiltig inmatning omdirigera man till user_error.html

    api_url = f'https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return render_template('result.html', year=year, month=month, day=day, price_class=price_class, data=data)
    elif response.status_code == 404:
        return 'Elprisinformationen är inte tillgänglig för den angivna tidpunkten/prisklassen.'
    else:
        print(f'Fel vid begäran till API:et. Statuskod: {response.status_code}')
        return 'Kunde inte hämta elprisinformation.'


@app.route('/user_error')
def user_error():
    return render_template('user_error.html')


def is_valid_date(year, month, day):
    max_date = datetime(2022, 11, 1).date()
    tomorrow = datetime.now().date() + timedelta(days=1)
    selected_date = datetime(int(year), int(month), int(day)).date()

    return max_date <= selected_date <= tomorrow


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404
