print('Starting..  ', end='')
import telebot
from mark_rebot.Private import Private
from mark_rebot.View import View
from mark_rebot.CallBack import CallBack
from mark_rebot.data_base import DB
from mark_rebot.editor import Editor
try:
	import local_config as config
except:
	import config

bot = telebot.TeleBot(config.TOKEN)
db = DB(config)
view = View(bot, db)
private = Private(bot, db, view)
call_back = CallBack(view, db)
editor = Editor(bot, db)


@bot.message_handler(content_types = ['text'])
def private_handler(message):
	private.main(message)

@bot.message_handler(content_types = ['photo'])
def private_handler(message):
	private.main(message, is_photo=True)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    call_back.main(call)

@bot.channel_post_handler(content_types = ['photo'])
def chanel_photo_handler(message):
	editor.main(message)


print('Done')

def main():
	bot.remove_webhook()
	bot.polling(none_stop=True)

if __name__ == '__main__':
	main()
