print('Starting..')
import telebot
from Private import Private
from View import View
from CallBack import CallBack
from data_base import DB
from editor import Editor
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

@bot.message_handler(content_types = ['document'], func = lambda m: m.chat.type == 'private')
def chanel_photo_handler(message):
	print('FILE PHOTO ')
	print(message.document.thumb)
	private.main(message, is_doc=True)

@bot.message_handler(content_types = ['text'], func = lambda m: m.chat.type == 'private')
def private_handler(message):
	private.main(message)



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
