from secrets import sign, apikey
from time import sleep
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

def get_artist_by_genre(id, extra_info=True):
    req_vars = { "apikey": apikey(),
                 "sig": sign(),
                 "genreids": id,
                 "format": "json",
                 "country": "US",
                 "language": "en" }
 
    base_url = "http://api.rovicorp.com/data/v1.1/descriptor/significantartists" 
    r = requests.get(base_url, params=req_vars)
    data = r.json
    # Pause - don't melt down the Rovi servers
    sleep(.5)
    artists = data.get('artists')
    full_artists = [ ] 
    if extra_info == True:
        for artist in artists:
            artist_id = artist.get('id')
            print "Looking up " + str(artist.get('name', 'No Name Available')
            if artist_id:
                extra_info = get_extra_artist_info(artist_id)
                artist['bio'] = extra_info.get('bio')
                artist['hometown'] = extra_info.get('birth')
            full_artists.append(artist)
        artists = full_artists
    print str(len(artists)) + " artists"
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

def get_extra_artist_info(id):
    req_vars = { "apikey": apikey(),
                 "sig": sign(),
                 "nameid": id,
                 "format": "json",
                 "country": "US",
                 "language": "en",
                 "include": "musicbio,images"}
 
    base_url = "http://api.rovicorp.com/data/v1.1/name/info"
    r = requests.get(base_url, params=req_vars)
    data = r.json
    artist_info = data.get('name', False)
    
    if artist_info:
        birth_city = artist_info.get('birth').get('place')
        headline_bio = artist_info.get('headlineBio', "Sorry, No Bio Available")
        # pass on images for now. 

        return {'city': birth_city, 'bio': headline_bio}
    else:
        return { }

def get_artist_geodata():
    pass

if __name__ == "__main__":
    print "caching genres"
    get_genres()
    print "caching artists"
    cache_all_genres()
#    get_extra_artist_info("MN0000842802")
