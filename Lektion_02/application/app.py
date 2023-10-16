from flask import Flask

app = Flask(__name__)

page = '''
    <!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="">
        <title>Flask Test</title>
    </head>

    <body>
        <h1>TEST</h1>
        <p>hej hej</p>
        <br>
        <list>
            <ol> hej 1</ol>
            <ol> hej 2</ol>
            <ol> hej 3</ol>
        </list>
    </body>

</html>

'''


@app.route("/")
def hello_world():
    return page


if __name__ == "__main__":
    app.run(debug=True)
