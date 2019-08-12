import json
import logging
import pymongo
import telegram

from datetime import datetime
from telegram.ext import Updater
from telegram.ext import CommandHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.WARNING)

def random(bot, update):
    random_post = next(posts_collection.aggregate([{ "$sample": { "size": 1}}]))

    bot.send_message(chat_id=update.message.chat_id,
                     text=f"<a href='{random_post['url']}'>[{datetime.utcfromtimestamp(int(random_post['date'])).strftime('%d %b %Y')}]</a> {random_post['text']}",
                     parse_mode=telegram.ParseMode.HTML,
                     disable_web_page_preview=True)

    if 'photos' in random_post:
        photos = [telegram.InputMediaPhoto(media=open(f"public/{photo['url']}", "rb")) for photo in random_post['photos']]
        if len(photos) > 0:
            bot.send_media_group(chat_id=update.message.chat_id,
                                media=photos[:10], 
                                disable_notification=True)


with open('options.json') as options_file:
    options = json.load(options_file)

bot_token = options['auth']['bot_token']

client = pymongo.MongoClient('mongodb://localhost:27017/')
posts_collection = client['vk-mousemath']['posts']

updater = Updater(token=bot_token, request_kwargs=options['network'])
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('random', random))
dispatcher.add_handler(CommandHandler('start', random))

updater.start_polling()