import json
import urllib.request

url = 'http://calmcode.io/datasets/pokemon.json'
with urllib.request.urlopen(url) as f:
    pokemon = json.loads(f.read())
