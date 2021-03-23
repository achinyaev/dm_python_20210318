import requests
from pathlib import Path

url = "http://www.magnit.ru/promo/"

response = requests.get(url)

print(response)