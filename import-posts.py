import urllib.request
import json
import pymongo

with (open('token', 'r')) as file:
    access_token = file.read()

response = urllib.request.urlopen(f"https://api.vk.com/method/wall.get?count=1&domain=mousemath&access_token={access_token}&v=5.101").read()
data = json.loads(response.decode('utf-8'))

count = int(data['response']['count'])
fetched = 0

client = pymongo.MongoClient('mongodb://localhost:27017/')
client['vk-mousemath']['responses'].drop()

while fetched < count:
    request = f"https://api.vk.com/method/wall.get?count=100&domain=mousemath&access_token={access_token}&v=5.101"
    if fetched > 0:
        request += f"&offset={fetched}"

    response = urllib.request.urlopen(request).read()
    data = json.loads(response.decode('utf-8'))
    fetched += len(data['response']['items'])

    client['vk-mousemath']['responses'].insert_many(data['response']['items'])

