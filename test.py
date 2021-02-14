import time
from pprint import pprint
import requests

url = "http://localhost:8000/api/match/get_match/"

while True:
    result = requests.get(url)
    result = result.json()
    pprint(result)
    time.sleep(2)
