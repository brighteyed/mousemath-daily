import html
import json
import os
import pymongo
import re
import ssl
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
        self.text = TextProcessor.URL_PATTERN.sub(r'<a href="\g<1>\g<2>\g<3>">\g<2>\g<3></a>',
                                                  self.text)
        return self

    def replace_markup_links(self):
        """Detect internal (?) links in markup format"""
        self.text = TextProcessor.MARKUP_LINK_PATTERN.sub(r'<a href="https://vk.com/\g<1>">\g<2></a>',
                                                          self.text)
        return self


class Item:
    def __init__(self, raw_item):
        self.url = f'https://vk.com/wall{raw_item["owner_id"]}_{raw_item["id"]}'
        self.date = raw_item['date']
        self.id = raw_item['id']

        if 'attachments' in raw_item:
            self.photos = []
            for attachment in raw_item['attachments']:
                if attachment['type'] == 'photo':
                    photo = {}
                    for size in attachment['photo']['sizes']:
                        photo[size['type']] = size

                    max_photo_size = next(s for s in ['w', 'z', 'y', 'x', 'm'] if s in photo.keys())
                    max_photo = photo[max_photo_size]

                    url = max_photo['url']
                    img = f"public/images/{'_'.join(url.split('/')[3:])}"

                    if not os.path.exists(img):
                        gcontext = ssl.SSLContext()        
                        link = urllib.request.urlopen(url, context=gcontext)
                        print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ==> {url}')
                        with open(img, 'wb') as image_file:
                            image_file.write(link.read())
                            print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] <== {url}')

                    max_photo['url'] = '/'.join(img.split('/')[1:])
                    self.photos.append(max_photo)

        self.text = TextProcessor(html.escape(raw_item['text'])) \
            .replace_hyperlinks().replace_markup_links() \
            .text


with open('options.json') as options_file:
    options = json.load(options_file)

vk_token = options['auth']['vk_token']

response = urllib.request.urlopen(f"https://api.vk.com/method/wall.get?count=1&domain=mousemath&filter=owner&access_token={vk_token}&v=5.101").read()
data = json.loads(response.decode('utf-8'))

count = int(data['response']['count'])
fetched = 0

client = pymongo.MongoClient('mongodb://localhost:27017/')
client['vk-mousemath']['responses'].drop()
client['vk-mousemath']['posts'].drop()

def transform_item(item):
    return Item(item).__dict__

def filter_item(item):
    if 'attachments' in item:
        if all([attachment['type'] == 'poll' for attachment in item['attachments']]):
            return False

    return True

while fetched < count:
    request = f"https://api.vk.com/method/wall.get?count=100&domain=mousemath&filter=owner&access_token={vk_token}&v=5.101"
    if fetched > 0:
        request += f"&offset={fetched}"

    response = urllib.request.urlopen(request).read()
    data = json.loads(response.decode('utf-8'))
    fetched += len(data['response']['items'])

    client['vk-mousemath']['responses'].insert_many(data['response']['items'])

    posts = list(map(transform_item, filter(filter_item, data['response']['items'])))
    client['vk-mousemath']['posts'].insert_many(posts)
