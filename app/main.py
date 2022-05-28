from flask import Flask

app = Flask(__name__)

@app.route("/")
def home_page():
    return "<h1>boblov</h1>"