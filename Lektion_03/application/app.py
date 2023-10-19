from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

dictionary = {
    "landsdel": ["Götaland", "Svealand", "Norrland"],
    "Landskap": ["Östergötland", "Södermanland", "Norbotten"],
    "Stad": ["Linköping", "Mariefred", "Piteå"]
}
df = pd.DataFrame(dictionary)

json_data = df.to_dict(orient="records")


@app.route("/")
def hello_world():
    return render_template('template.html', json_data=json_data)


if __name__ == "__main__":
    app.run(debug=True)
