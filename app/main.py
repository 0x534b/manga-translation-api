from flask import Flask
from translate import Translator

from urllib import request
import tempfile

app = Flask(__name__)

@app.route("/")
def home_page():
    return f"<h1>out</h1>"

    # tempthing = request.urlopen(url)

    # translator= Translator(from_lang="japanese",to_lang="english")
    # boblov = translator.translate("めんどくさい")
    # return f"<h1>{boblov}</h1>"