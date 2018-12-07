print('Starting..')
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from Private import Private
from View import View
from CallBack import CallBack
from data_base import DB
from editor import Editor
from pprint import pprint
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


@bot.message_handler(content_types = ['photo'], func = lambda m: m.chat.type == 'private')
def private_handler(msg):
	print('--------------START EDIT PRIVATE PHOTO-----------------')
	user_id = msg.from_user.id
	bot.send_chat_action(user_id, 'upload_photo')
	markup = InlineKeyboardMarkup()
                    
	if db.user_get(user_id, 'group_select') == 0:
		markup.add(InlineKeyboardButton(text = 'Открить', callback_data = 'open ch_list'))
		bot.send_message(user_id, 'Нужно открить настройки', reply_markup = markup)
		return

	ch_info = db.get_group(user_id = user_id)


	if ch_info['status'] =='off' or ch_info['id_photo_mark'] == 'off' and ch_info['text_mark'] == 'off':
		print('Channel status off, return private')
		return
		
	markup.add(InlineKeyboardButton(text = 'Открить навстройки', callback_data = 'open ch_sett $is_new=True, ch_id=' + str(ch_info['id'])))
	pprint(ch_info)
	in_photo = editor.download_photo(msg.photo[-1].file_id)


	if not ch_info['id_photo_mark'] == 'off':
		type_mark = 'photo_mark'
		mark_photo = editor.download_photo(ch_info['id_photo_mark'])

		edit_image = editor.add_watermark(in_image = in_photo,
						watermark_image = mark_photo,
						config_ed = ch_info)

	elif not ch_info['text_mark'] == 'off': 
		type_mark = 'text_mark'
		edit_image = editor.add_textmark(in_photo, ch_info)
	
	
	bot.send_photo(user_id, photo = edit_image.getvalue(), reply_markup = markup)
	
	print('--------------SUCCES EDIT PRIVATE PHOTO-----------------')






@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    call_back.main(call)

@bot.channel_post_handler(content_types = ['photo'])
def chanel_photo_handler(message):
	editor.main(message)


print('Done')

def main():
	print('Remove webhook')
	bot.remove_webhook()
	bot.polling(none_stop=True)

if __name__ == '__main__':
	main()
