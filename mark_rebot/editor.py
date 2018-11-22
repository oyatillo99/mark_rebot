import io
from pprint import pprint
from telebot import types
from PIL import Image, ImageDraw, ImageFont


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
        group = self.db.get_group(ch_id = message.chat.id)
        caption = message.caption
        chat_id = message.chat.id
        msg_id = message.message_id
        
        pprint(group)

        if not group:
            print('This channel not found, return')
            return
        if group['status'] =='off' or group['id_photo_mark'] == 'off' and group['text_mark'] == 'off':
            print('Channel status off, return')
            return

        in_photo = self.download_photo(message.photo[-1].file_id)


        if not group['id_photo_mark'] == 'off':
            type_mark = 'photo_mark'
            mark_photo = self.download_photo(group['id_photo_mark'])

            edit_image = self.add_watermark(in_image = in_photo,
                            watermark_image = mark_photo,
                            position = group['position_mark'],
                            mark_size = group['mark_size'])

        elif not group['text_mark'] == 'off': 
            type_mark = 'text_mark'
            edit_image = self.add_textmark(in_photo, group)
        
        self.photo_edit(chat_id, msg_id, edit_image, caption)

        self.db.new_edit_post(chat_id, group['user_id'], type_mark)


    def add_textmark(self,in_image, group):
        color = tuple(map(int, group['color_mark'].split()))
        url_for_font_style = 'fonts/'+group['font_style_mark']+'.ttf'
        mark_size = int(group['mark_size']) * 3

        base = Image.open(io.BytesIO(in_image)).convert('RGBA')
        main_W, main_H = base.size

        txt = Image.new('RGBA', base.size, (255,255,255,0))
        fnt = ImageFont.truetype(url_for_font_style, mark_size)
        
        d = ImageDraw.Draw(txt)

        text_W, text_H = d.textsize(group['text_mark'], fnt)
        d.text(self.pos_conf(main_W, main_H, text_W, text_H, group['position_mark']), group['text_mark'], font = fnt, fill = color)
        
        out = Image.alpha_composite(base, txt)

        bytes_photo = io.BytesIO()
        out.save(bytes_photo, format='PNG')
        return bytes_photo


    def add_watermark(self,in_image,mark_size,position,watermark_image):
        input_image = Image.open(io.BytesIO(in_image)).convert("RGBA")
        main_W, main_H = input_image.size
        watermark = Image.open(io.BytesIO(watermark_image)).convert("RGBA")

        mark_size = int((((main_H+main_W)/2)/100)*int(mark_size))

        wpercent = (mark_size/float(watermark.size[0]))
        hsize = int((float(watermark.size[1])*float(wpercent)))
        watermark = watermark.resize((mark_size,hsize), Image.ANTIALIAS)

        mark_W, mark_H = watermark.size

        transparent = Image.new('RGBA', (main_W, main_H), (0,0,0,0))
        transparent.paste(input_image, (0,0))
        transparent.paste(watermark, box = self.pos_conf(main_W, main_H, mark_W, mark_H, position),mask=watermark) # mask=watermark

        bytes_photo = io.BytesIO()
        transparent.save(bytes_photo, format='PNG')
        return bytes_photo

    def photo_edit(self,chat_id,msg_id,bytes_photo, caption):
        print('Edit photo... , msg_id: {}, name_photo: {}'.format(chat_id, msg_id))             
        info = self.bot.edit_message_media(chat_id = chat_id, message_id = msg_id, media = types.InputMediaPhoto(bytes_photo.getvalue(), caption = caption))
        print('-------------------------- SUCCESS EDITED ---------------------------')

    
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


                
