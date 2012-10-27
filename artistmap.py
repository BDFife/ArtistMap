from flask import Flask
from flask import render_template
from flask import url_for
from secrets import apikey, sign

import requests
import os

import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Sorry, this space empty."

@app.route('/genres')
def genre_list():
    f = open('genre_cache.json', 'r')
    genres = json.load(f)
    f.close()
    return render_template('genres.html', genres=genres)

@app.route('/artists/genre/<id>')
def get_artist_by_genre(id):
    f = open ('genre_' + str(id) + '.json', 'r')
    artists = json.load(f)
    f.close()
    return render_template('artist_list.html', artists=artists)

@app.route('/map/genre/<id>')
def map_artist_by_genre(id):
    return "Sorry, this space empty."

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

