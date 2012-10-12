from flask import Flask
from flask import render_template
import os

import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/genres')
def genre_list():
    f = open('genre_cache.json', 'r')
    genres = json.load(f)
    f.close()
    genres = genres.get('genres')
    return render_template('genres.html', genres=genres)


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

