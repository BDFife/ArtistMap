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
    
    f = open("genre_cache.json", 'w')
    json.dump(data, f, indent=4)
    f.close()

if __name__ == "__main__":
    print get_genres()

