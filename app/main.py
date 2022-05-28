from flask import Flask
from translate import Translator

from urllib import request
import urllib.request
import tempfile

app = Flask(__name__)

@app.route("/")
def home_page():
    return f"<h1>out</h1>"

    # temp = tempfile.TemporaryFile()
    # temp.write(url)

    # urllib.request.urlretrieve(url, filename)


    # temp.close()

    # tempthing = request.urlopen(url)

    # translator= Translator(from_lang="japanese",to_lang="english")
    # boblov = translator.translate("めんどくさい")
    # return f"<h1>{boblov}</h1>"