from flask import Flask, render_template, request
import requests
from flask import redirect, url_for

app = Flask(__name__)

def fetch_el_prices(year, month, day, price_class):
    api_url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        print(data)  # Lägg till denna rad för att felsöka
        return data
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    el_prices = None  # Skapa en tom el_prices-variabel
    if request.method == "POST":
        # Hantera postdata och API-anrop
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        price_class = request.form.get("price_class")

        el_prices = fetch_el_prices(year, month, day, price_class)

    return render_template("index.html", el_prices=el_prices)

@app.route("/resultat", methods=["POST"])
def resultat():
    el_prices_list = handle_form_data()  # Antag att detta är en lista
    el_prices = {f"Tid {i}": price for i, price in enumerate(el_prices_list)}

    if el_prices:
        # Här kan du hantera el_prices och skicka den till din mall
        return render_template("result.html", el_prices=el_prices)

    # Förhindra att användare navigerar direkt till /resultat utan att posta data

    return redirect(url_for("index"))