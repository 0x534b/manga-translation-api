# manga-translation-api
A Python Flask API to translate manga pages.

submitted to TO hacks and used alongside [boblov](https://github.com/0x534b/boblov)

# setup
## heroku
In theory, this API is ready to host on heroku. However, heroku limits the compressed slug size to 500MB, and with opencv and tesesract, this project is ~550MB.

## debug
### dependencies
This project relies on opencv and tesseract-ocr, so you need both of these installed for your OS. You also need to download `jpn_vert.traineddata` and place it in your `tessdata` folder to add support for vertical Japanese text.

Install the Python dependencies from `requirements.txt`

### running the server
With all the dependencies installed, you can run the server with `waitress` via this command:\
```
waitress-serve --port=8000 wsgi:app
```

Note: you can change the port, but currently [boblov](https://github.com/0x534b/boblov) expects the server to be found at `localhost:8000`

# usage
You can make a request to the API using a URL like this:\
`http://<host>/?url=<source image url>`

The API should respond with a translated image.
