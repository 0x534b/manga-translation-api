import os
from io import BytesIO
import requests
# import tempfile
# import urllib
from uuid import uuid4
# import dill as pickle

from flask import Flask, request, send_file

from .image_processing import translate_image

app = Flask(__name__)

@app.route("/")
def home_page():
    # return f"<h1>out</h1>"
    # https://manga-translation-api.herokuapp.com/?url=jsdffja
    url = request.args.get('url')

    try:
        response = requests.get(url)
    except Exception as e:
        return f"<p>Exception encountered requesting image URL: {e}</p>"

    # generate filename
    dirname = os.path.dirname(__file__)
    dirname = os.path.join(dirname, "temp")
    filename = os.path.join(dirname, str(uuid4()) + ".jpg")
    # filename = str(uuid4()) + ".jpg"

    file = open(filename, "wb+")
    file.write(response.content)
    file.close()

    translated_image = translate_image(filename)
    os.remove(filename)

    if translated_image is None:
        return "<p>Failure translating image.</p>"

    img_io = BytesIO()
    translated_image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')