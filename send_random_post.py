import json
import logging
import pymongo
import telegram

from datetime import datetime
from telegram.utils.request import Request


CHAT_ID = -1001359975213

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)

with open('options.json') as options_file:
    options = json.load(options_file)

bot_token = options["auth"]["bot_token"]

client = pymongo.MongoClient('mongodb://localhost:27017/')
random_post = next(client['vk-mousemath']['posts'].aggregate([{"$sample": {"size": 1}}]))

request = Request(proxy_url=options['network']['proxy_url'])

post_date = datetime.utcfromtimestamp(int(random_post['date'])).strftime('%d %b %Y')
post_text = random_post['text']
post_url = random_post['url']
params = {'chat_id': CHAT_ID,
          'text': f"<a href='{post_url}'>[{post_date}]</a> {post_text}",
          'parse_mode': 'HTML',
          'disable_web_page_preview': True
          }
request.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', params)

if 'photos' in random_post:
    photos = [telegram.InputMediaPhoto(media=open(f"public/{photo['url']}", "rb")) for photo in random_post['photos']]
    if len(photos) > 0:
        params = {'chat_id': CHAT_ID,
                  'media': photos[:10],
                  'disable_notification': True
                  }
        request.post(f'https://api.telegram.org/bot{bot_token}/sendMediaGroup', params)
