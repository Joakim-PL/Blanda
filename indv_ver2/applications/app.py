from flask import Flask, render_template, request, redirect
import requests
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/')  # routen för startsidan
def index():
    return render_template('index.html')  # retunerar index.html som för html filen för startsidan där inputs finns


@app.route('/result', methods=['POST'])  # routen för hantering av inmatningen och visa resultaten
def result():
    year = request.form['year']  # formulär datan
    month = request.form['month']
    day = request.form['day']
    price_class = request.form['price_class']

    if not year.isdigit() or not month.isdigit() or not day.isdigit():  # kontrollerar om inmatning är siffror för år, månad och dag
        return redirect('/user_error')  # Felinmatning så omredigeras man till user_error.html

    if is_valid_date(year, month, day):  # kontrollerar att datummet är giltigt
        pass  # Om det är giltig inmatning så fortsätter programmet
    else:
        return redirect('/user_error')  # Ogiltig inmatning omdirigera man till user_error.html

    api_url = f'https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json'
    response = requests.get(api_url)  # gör en förfrågning till API:et

    if response.status_code == 200:  # hanterar API svaret
        data = response.json()  # Om API ger 200 så fortsätter man till result.html
        return render_template('result.html', year=year, month=month, day=day, price_class=price_class, data=data)
    elif response.status_code == 404:  # om API ger 404 så får man ett felmeddelande istället för errors
        return 'Elprisinformationen är inte tillgänglig för den angivna tidpunkten.'
    else:
        print(f'Fel vid begäran till API:et. Statuskod: {response.status_code}')  # skriver ut statuskoden så man kan felsöka vad som är fel
        return 'Kunde inte hämta elprisinformation.'  # om något annat händer så får man ett felmeddelande istället för errors


@app.route('/user_error')  # routen för fel från användaren
def user_error():
    return render_template('user_error.html')  # retunerar en html fil för fel från användaren


def is_valid_date(year, month, day):
    try:  # Testar om inmatningen av datum stämmer
        # om det är fel inmatning så ska man inte på ValueError
        # kontrollerar om månaden är mellan 1 - 12
        if 1 <= int(month) <= 12:
            max_date = datetime(2022, 11, 1).date()  # gör så att senast man kan få elpriser från är 2022-11-1
            tomorrow = datetime.now().date() + timedelta(days=1)  # beräknar morgondagens datum så att man kan alltid välja en dag fram
            selected_date = datetime(int(year), int(month), int(day)).date()

            return max_date <= selected_date <= tomorrow  # checkar att datummet är inom 2022-11-1 till imorgon
        else:
            return False  # månaden är inte mellan 1 - 12

    except ValueError:
        return False  # om det var ogiltig inmatning så ska man inte få en ValueError


@app.errorhandler(404)  # felhanterare för 404
def not_found_error(error):
    return render_template('error.html'), 404
