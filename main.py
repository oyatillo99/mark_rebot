print('Starting..')
import telebot
import requests
import uuid
import os
from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton,
 			InputMediaPhoto, InputMediaVideo, InputMediaAnimation)
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
editor = Editor()



@bot.message_handler(content_types = ['document'], func = lambda m: m.chat.type == 'private')
def chanel_photo_handler(message):
	print('FILE PHOTO ')
	print(message.document.thumb)
	private.main(message, is_doc=True)

@bot.message_handler(content_types = ['text'], func = lambda m: m.chat.type == 'private')
def private_handler(message):
	private.main(message)

def download_file(file_id):
	file_info = bot.get_file(file_id)  
	return bot.download_file(file_info.file_path)



def check_ch(info):
	if info:
		return True
	else:
		print('This channel not found, return')
		
		for admin in bot.get_chat_administrators(info.id):
			if admin.status == 'creator':
				print(admin.user.username)
				
				markup = InlineKeyboardMarkup()
				call_data = 'add ch_sett $ch_id=' + str(info.id)
			
				markup.add(InlineKeyboardButton(text = 'Настроить канал', callback_data = call_data ))
				try:
					msg_id = bot.send_message(admin.user.id, 'Привет оказалось я админ в твоем канале и я не знаю какую марку ставить в твоих постах. Если не хочешь это видеть можешь удалить меня из администраторов.', reply_markup = markup)
				except Exception as e:
					print('Error send block msg: ', e)
				db.msg_id(admin.user.id, msg_id.message_id)
				return False
	if info.status =='off':
		print('Channel status off, return')
		return False
	


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

	info = db.get_ch(user_id = user_id)
	

	if info.photo_id == 'off' and info.text_mark == 'off':
		print('Channel status off, return private')
		return
		
	markup.add(InlineKeyboardButton(text = 'Открить навстройки', callback_data = 'open ch_sett $is_new=True, ch_id=' + str(info.id)))
	
	in_photo = download_file(msg.photo[-1].file_id)

	if info.type_mark == 'text':
		mark = None
	else:
		mark = download_file(info.photo_id)

	photo = editor.edit_photo(info, in_photo, mark)
	
	bot.send_photo(user_id, photo = photo.getvalue(), reply_markup = markup)
	print('--------------SUCCES EDIT PRIVATE PHOTO-----------------')


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    call_back.main(call)

def edit_media(msg, media, info):
	bot.send_video
	print(f'Edit photo, msg_id: {msg.message_id}, ch_id: {msg.chat.username}')

	try:
		info = bot.edit_message_media(chat_id = info.id, message_id = msg.message_id, media = media)
		print('------------------------ SUCCESS EDITED ----------------------')
			
	except Exception as e:
		markup = InlineKeyboardMarkup()
		print('Error edit media: ', e)
		txt = '⚠️ Привет только что питался поставить водяной знак в канале '
		
		try:					
			r = bot.get_chat_member(info.id, 770141959)
										# bot id -----^
			if r.can_edit_messages:
				return# if bot can edit, return

			print('Bot can`t edit messages')
			markup.add(InlineKeyboardButton(
				text = 'Скрить', callback_data = 'open main'))

			msg_id = bot.send_message(info.user_id, 
			txt + info.past_name_ch + ', но оказалось у меня нет права Редактировать чужие сообщенияє',
				reply_markup = markup)

		except Exception as e:
			print('Error get chat member: ', e)
			msg_id = bot.send_message(info.user_id, 
			txt + info.past_name_ch + ', но оказалось я не администратор',
					reply_markup = markup)

			db.msg_id(info.user_id, msg_id.message_id)


@bot.channel_post_handler(content_types = ['photo'])
def chanel_photo_handler(msg):
	info = db.get_ch(ch_id = msg.chat.id)
	if not check_ch(info):
		return
	file = download_file(msg.photo[-1].file_id)

	if info.type_mark == 'text':
		mark = None
	else:
		mark = download_file(info.photo_id)

	photo = editor.edit_photo(info, file, mark)
	edit_media(msg, InputMediaPhoto(photo.getvalue()), info)
	db.new_edit_post(info.id, info.user_id)

@bot.channel_post_handler(content_types = ['video','document'])
def chanel_gif_handler(msg):
	print(msg)
	print('start edit..')
	info = db.get_ch(ch_id = msg.chat.id)
	if not check_ch(info):
		return
	media = None
	type_media = None
	if msg.content_type == 'document' and msg.document.mime_type == 'video/mp4':
		media = msg.document
		type_media = 'gif'
	elif msg.content_type == 'video':
		media = msg.video
		type_media = 'video'
	else:
		print("this no video or gif")
		return
		
						 
	if media.file_size > 5000000:
		print('This vidoe very big')
		return

	if not check_ch(info):
		return

	input_file_name = str(uuid.uuid4()) + '.mp4'
	file = download_file(media.file_id)
	with open(input_file_name, 'wb') as nfile:
		nfile.write(file)

	if info.type_mark == 'text':
		mark = None
	else:
		mark = download_file(info.photo_id)

	output_file_name = editor.edit_gif(info, input_file_name, mark)
	
	if info.del_or_edit == 'del' and type_media == 'gif':
		url   = f"https://api.telegram.org/bot{config.TOKEN}/sendAnimation"
		files = {'animation': open(output_file_name, 'rb')}
		data  = {'chat_id' : info.id, 'caption': msg.caption, 'disable_notification': True}
		r = requests.post(url, files=files, data=data)
		print(r.status_code, r.reason, r.content)
		bot.delete_message(info.id, message_id= msg.message_id)
	else:
		edit_media(msg, InputMediaVideo(open(output_file_name, 'rb'), caption = msg.caption), info)

	os.remove(input_file_name)
	os.remove(output_file_name)
	db.new_edit_post(info.id, info.user_id)

print('Done')

def main():
	print('Remove webhook')
	bot.remove_webhook()
	bot.polling(none_stop=True)

if __name__ == '__main__':
	main()
