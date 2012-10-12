from secrets import sign, apikey
import requests
import json

def get_genres():
    req_vars = { "apikey": apikey(),
                 "sig": sign(),
                 "include": "subgenres",
                 "format": "json",
                 "country": "US",
                 "language": "en" }
 
    base_url = "http://api.rovicorp.com/data/v1.1/descriptor/musicgenres" 
    r = requests.get(base_url, params=req_vars)
    data = r.json
    data = data.get('genres')
    
    f = open("genre_cache.json", 'w')
    json.dump(data, f, indent=4)
    f.close()

def get_artist_by_genre(id):
    req_vars = { "apikey": apikey(),
                 "sig": sign(),
                 "genreids": id,
                 "format": "json",
                 "country": "US",
                 "language": "en" }
 
    base_url = "http://api.rovicorp.com/data/v1.1/descriptor/significantartists" 
    r = requests.get(base_url, params=req_vars)
    data = r.json
    artists = data.get('artists')
    print len(artists) + " artists"
    f = open("genre_" + str(id) + ".json", 'w')
    json.dump(artists, f, indent=4)
    f.close()

def cache_all_genres():
    f = open("genre_cache.json", 'r')
    genres = json.load(f)
    f.close()
    
    for genre in genres: 
        print 'caching ' + genre.get('name')
        get_artist_by_genre(genre.get('id'))
        subgenre = genre.get('subgenres')
        for sub in subgenre:
            print 'caching sub ' + sub.get('name')
            get_artist_by_genre(sub.get('id'))

if __name__ == "__main__":
    print "caching genres"
    get_genres()
    print "caching artists"
    cache_all_genres()
