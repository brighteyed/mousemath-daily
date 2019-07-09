import html
import json
import pymongo
import re
import urllib.request

from datetime import datetime


class TextProcessor:
    # https://vk.com/wall-143897455_775; https://vk.com/wall-143897455_925
    URL_PATTERN = re.compile(r'(https?://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')

    # https://vk.com/wall-143897455_762
    MARKUP_LINK_PATTERN = re.compile(r'\[\s*(\S+)\s*\|\s*(.*)\s*\]')

    def __init__(self, text):
        self.text = text

    def replace_hyperlinks(self):
        """Detect hyperlinks"""
        self.text = TextProcessor.URL_PATTERN.sub(r'<a href="\g<1>\g<2>\g<3>">\g<2>\g<3></a>', self.text)
        return self

    def replace_markup_links(self):
        """Detect internal (?) links in markup format"""
        self.text = TextProcessor.MARKUP_LINK_PATTERN.sub(r'<a href="https://vk.com/\g<1>">\g<2></a>', self.text)
        return self


class Item:
    def __init__(self, raw_item):
        self.url = f'https://vk.com/wall{raw_item["owner_id"]}_{raw_item["id"]}'
        self.date = raw_item['date']
        self.id = raw_item['id']

        if 'attachments' in raw_item:
            self.photos = []
            for attachment in raw_item['attachments']:
                photo = {}
                if attachment['type'] == 'photo':
                    for size in attachment['photo']['sizes']:
                        photo[size['type']] = size

                if photo:            
                    self.photos.append(photo)

        self.text = TextProcessor(html.escape(raw_item['text'])) \
            .replace_hyperlinks().replace_markup_links() \
            .text


with (open('token', 'r')) as file:
    access_token = file.read()

response = urllib.request.urlopen(f"https://api.vk.com/method/wall.get?count=1&domain=mousemath&filter=owner&access_token={access_token}&v=5.101").read()
data = json.loads(response.decode('utf-8'))

count = int(data['response']['count'])
fetched = 0

client = pymongo.MongoClient('mongodb://localhost:27017/')
client['vk-mousemath']['responses'].drop()
client['vk-mousemath']['posts'].drop()

def transform_item(item):
    return Item(item).__dict__

while fetched < count:
    request = f"https://api.vk.com/method/wall.get?count=100&domain=mousemath&filter=owner&access_token={access_token}&v=5.101"
    if fetched > 0:
        request += f"&offset={fetched}"

    response = urllib.request.urlopen(request).read()
    data = json.loads(response.decode('utf-8'))
    fetched += len(data['response']['items'])

    client['vk-mousemath']['responses'].insert_many(data['response']['items'])

    posts = list(map(transform_item, data['response']['items']))
    client['vk-mousemath']['posts'].insert_many(posts)
