from flask import Flask, render_template, request
import requests

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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404
