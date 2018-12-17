import io
from pprint import pprint
from telebot import types
from PIL import Image, ImageDraw, ImageFont
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Editor(object):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
    def download_photo(self, photo_id):
        file_info = self.bot.get_file(photo_id) 
        downloaded_file = self.bot.download_file(file_info.file_path)
        return downloaded_file
        
        
    def main(self, message,):
        print('\n-------------------------  START EDIT PHOTO  ------------------------------')
        print(f'chat: {message.chat.username} msg.id: {message.message_id}, {message.chat.id}')
        config_ed = self.db.get_group(ch_id = message.chat.id)
        caption = message.caption
        chat_id = message.chat.id
        msg_id = message.message_id
        

        if not config_ed:
            print('This channel not found, return')
            
            for admin in self.bot.get_chat_administrators(chat_id):
                if admin.status == 'creator':
                    print(admin.user.id)
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton(text = 'Настроить канал', callback_data = 'add ch_sett $ch_id=' + str(chat_id) + ', username='+ message.chat.title ))
                    
                    msg_id = self.bot.send_message(admin.user.id, 'Привет оказалось я админ в твоем канале и я не знаю какую марку ставить в твоих постах. Если не хочешь это видеть можешь удалить меня из администраторов.', reply_markup = markup)
                    self.db.msg_id(admin.user.id, msg_id.message_id)
            
            
            return
        if config_ed['status'] =='off' or config_ed['id_photo_mark'] == 'off' and config_ed['text_mark'] == 'off':
            print('Channel status off, return')
            return
        pprint(config_ed)
        in_photo = self.download_photo(message.photo[-1].file_id)


        if not config_ed['id_photo_mark'] == 'off':
            type_mark = 'photo_mark'
            mark_photo = self.download_photo(config_ed['id_photo_mark'])

            edit_image = self.add_watermark(in_image = in_photo,
                            watermark_image = mark_photo,
                            config_ed = config_ed)

        elif not config_ed['text_mark'] == 'off': 
            type_mark = 'text_mark'
            edit_image = self.add_textmark(in_photo, config_ed)
        
        self.photo_edit(chat_id, msg_id, edit_image, caption, config_ed)

        self.db.new_edit_post(chat_id, config_ed['user_id'], type_mark)


    def add_textmark(self,in_image, config_ed):

        color = list(map(int, config_ed['color_mark'].split()))
        color.append(int((255 / 100) * config_ed['transparent_mark']))
        
        url_for_font_style = 'fonts/'+config_ed['font_style_mark']+'.ttf'
        mark_size = int(config_ed['mark_size']) * 2

        base = Image.open(io.BytesIO(in_image)).convert('RGBA')
        main_W, main_H = base.size

        txt = Image.new('RGBA', base.size, (255,255,255,0))
        fnt = ImageFont.truetype(url_for_font_style, mark_size)
        
        d = ImageDraw.Draw(txt)

        text_W, text_H = d.textsize(config_ed['text_mark'], fnt)
        d.text(self.pos_conf(main_W, main_H, text_W, text_H,
         config_ed['position_mark']), config_ed['text_mark'], font = fnt, fill = tuple(color))
        
        out = Image.alpha_composite(base, txt)

        bytes_photo = io.BytesIO()
        out.save(bytes_photo, format='PNG')
        return bytes_photo


    def add_watermark(self,in_image,watermark_image, config_ed):

        input_image = Image.open(io.BytesIO(in_image)).convert("RGBA")
        main_W, main_H = input_image.size
        watermark = Image.open(io.BytesIO(watermark_image)).convert("RGBA")
        watermark = Image.eval(watermark, lambda x: int((x /100) * config_ed['transparent_mark']))


        mark_size = int((((main_H+main_W)/2)/100)*int(config_ed['mark_size']))

        wpercent = (mark_size/float(watermark.size[0]))
        hsize = int((float(watermark.size[1])*float(wpercent)))
        watermark = watermark.resize((mark_size,hsize), Image.ANTIALIAS)

        mark_W, mark_H = watermark.size

        transparent = Image.new('RGBA', (main_W, main_H), (0,0,0,0))
        transparent.paste(input_image, (0,0))
        transparent.paste(watermark, box = self.pos_conf(main_W, main_H, mark_W, mark_H, config_ed['position_mark']),mask=watermark) # mask=watermark

        bytes_photo = io.BytesIO()
        t = transparent.convert('RGB')
        t.save(bytes_photo, format='jpeg')
        return bytes_photo



    def photo_edit(self,ch_id,msg_id,bytes_photo, caption, config_ed):
        print(f'Edit photo... , msg_id: {msg_id}, ch_id: {ch_id}')
        try:
            info = self.bot.edit_message_media(chat_id = ch_id, message_id = msg_id, media = types.InputMediaPhoto(bytes_photo.getvalue(), caption = caption))
            print('-------------------------- SUCCESS EDITED ---------------------------')
            
        except Exception as e:
            markup = InlineKeyboardMarkup()
            print('Error edit media: ', e)
            try:
                
                r = self.bot.get_chat_member(ch_id, 770141959)

                if not r.can_edit_messages:
                    print('can`t_edit_messages')
                    markup.add(InlineKeyboardButton(text = 'Скрить', callback_data = 'open main'))

                    msg_id = self.bot.send_message(config_ed['user_id'], 
'⚠️ Привет только что питался поставить водяной знак в канале '+config_ed['past_name_ch']+', но оказалось у меня нет права Редактировать чужие сообщенияє',
                     reply_markup = markup)

            except Exception as e:
                print('Error get chat member: ', e)
                msg_id = self.bot.send_message(config_ed['user_id'], 
'⚠️ Привет только что питался поставить водяной знак в канале '+config_ed['past_name_ch']+', но оказалось я не администратор',
                     reply_markup = markup)







            
            
            self.db.msg_id(config_ed['user_id'], msg_id.message_id)


    
    def pos_conf(self, main_W, main_H, mark_W, mark_H, position):
        if position == 'top_left':
            return 0,0
        elif position == 'top':
            return int(main_W/2) - int(mark_W/2), 0
        elif position == 'top_right':
            return main_W - mark_W, 0
        elif position == 'center_left':
            return 0, int(main_H/2) - int(mark_H/2)
        elif position == 'center':
            return int(main_W/2) - int(mark_W/2), int(main_H/2) - int(mark_H/2)
        elif position == 'center_right':
            return main_W - mark_W, int(main_H/2) - int(mark_H/2)
        elif position == 'down_left':
            return 0, main_H - mark_H
        elif position == 'down':
            return int(main_W/2) - int(mark_W/2), main_H - mark_H
        elif position == 'down_right':
            return main_W - mark_W, main_H - mark_H


                
