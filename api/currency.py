import requests
import datetime
import json

sana = datetime.date.today()
url = f'https://cbu.uz/uz/arkhiv-kursov-valyut/json/all/{sana}/ '

response = requests.request("GET", url=url)
data = json.loads(response.text)
print(data)
print(data[0]['Rate'])
print(data[2]['Rate'])
