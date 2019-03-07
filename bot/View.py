import menu_markup
from telebot.types import InlineKeyboardMarkup as markup
from telebot.types import InlineKeyboardButton as btn
from strings import ru
class View(object):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.pos = {'top_left'    : '↖️', 'top'    :'⬆️', 'top_right'    :'↗️',
                    'center_left' : '⬅️', 'center':'⬛', 'center_right' :'➡️',
                    'down_left'   : '↙️', 'down'   :'⬇️', 'down_right'   :'↘️'}
    
        
    def gs_info(func):
        def wrapper(self, user_id, **kwarg):
            #print(f'Open {func.__name__} menu for {user_id} args: {kwarg}')
           
            msg_id = self.db.msg_id(user_id)
            if msg_id == 0:
                msg_id = False
                try:
                    del kwarg['is_new']
                except Exception as e:
                    print('Error 1: ', e)
            elif 'is_new' in kwarg:
                try:
                    self.bot.delete_message(user_id, msg_id)
                except Exception as e:
                    print('Faill del msg: ', e)
                msg_id = False
                del kwarg['is_new']
            

            text, bts = func(self, user_id, **kwarg)

            if type(text) is int:
                try:
                    self.bot.delete_message(user_id, msg_id)
                except Exception as e:
                    print('Error del msg: ',e)
                self.db.msg_id(user_id, text)
                return
            

            if type(bts) is str:
                bts = menu_markup.get_bts(bts)

            if msg_id:
                try:
                    new_msg_id = self.bot.edit_message_text(
                        chat_id = user_id, message_id = msg_id,
                        text = text,
                        parse_mode = 'Markdown',
                        reply_markup = bts).message_id
                except Exception as e:
                    new_msg_id = msg_id
                    print('Error edit msg: ', e)

            else:
                new_msg_id = self.bot.send_message(
                user_id, text,
                parse_mode = 'Markdown',
                reply_markup = bts).message_id
                
            if not new_msg_id == msg_id:
                self.db.msg_id(user_id, new_msg_id)
        return wrapper
        
    @gs_info
    def send(self, user_id, text, markup):
        return text, markup

    @gs_info
    def main(self, user_id):
        self.db.user_set(user_id, 'menu_select', 'main')
        return ru['main_menu'], 'main'

    @gs_info
    def welcom(self, user_id):
        bts = markup()
        bts.add(btn(text='OK', callback_data='open main'))
        return ru['welkom_menu'], bts
        

    @gs_info
    def ch_list(self, user_id):
        channels = self.db.get_channel_id(user_id)
        
        ch_list = markup()
        ch_list.add(btn(text=ru['back'], callback_data = 'open main'),
                    btn(text=ru['add'], callback_data = 'open ch_add'))
        if not channels:
            return ru['ch_list_empty'], ch_list
       
        for ch in channels:
            try:
                try:
                    self.bot.get_chat(ch[0])  
                    name = ch[1] + ' | ❌ OFF' if ch[2] == 'off' else ch[1]
                except Exception as e:
                    print('Error getchat: ',e)
                    name = ch[1] + ' | Не админ'

                ch_list.add(btn(text = name,
                    callback_data = 'open ch_sett $ch_id=' + str(ch[0])))
                
            except Exception as e:
                print('Error create btns: ', e)

        return ru['list_ch'], ch_list

    def view_position(self, position):
        return self.pos[position]
    
    @gs_info
    def ch_add(self, user_id):
        bts = markup()  
        bts.add(btn(text = ru['back'], callback_data='open ch_list'))
        return ru['add_ch'], bts 
        

    @gs_info
    def ch_setting(self, user_id):
        bts = markup()      
        ch_info = self.db.get_ch(user_id = user_id)

        try:
            title = self.bot.get_chat(ch_info.id).title
            if not title == ch_info.past_name_ch:
                self.db.channel_set(user_id, 'past_name_ch', title)
                ch_info.past_name_ch = title

        except Exception as e:
            print('Error get chat title: ', e)
            bts.add(btn(text = ru['update'], callback_data = 'open ch_sett'))
            bts.add(btn(text = ru['back'], callback_data = 'open ch_list'))
            return ru['del_bot'].format(channel_name = ch_info.past_name_ch), bts

        if ch_info.photo_id == 'off' and ch_info.text_mark == 'off':
            bts.add(btn(text = ru['back'], callback_data='open ch_list')) 
            self.db.user_set(user_id, 'menu_select', 'set_mark')
            return ru['add_watermark'], bts    
        
        status = '✅' if ch_info.status == 'on' else '❌'
        transparent = str(abs(ch_info.transparent - 100)) + '%'
        bts.add(btn(text=ru['back'], callback_data='open ch_list'),
                btn(text=ru['status'] + status, callback_data = 'set ch status'))
        bts.add(btn(text=ru['size'] + str(ch_info.mark_size) + '%', callback_data = 'open mark_size'),
                btn(text=ru['position']+ self.view_position(ch_info.pos_mark), callback_data = 'open pos_mark'))
        bts.add(btn(text='Прозрa-ть: ' + transparent, callback_data = 'open transparent_mark'),
                btn(text=ru['margin'] + str(ch_info.margin_mark) + "px", callback_data = 'open margin_mark'))

        if not ch_info.photo_id == 'off':
            bts.add(btn(text = ru['change_mark'], callback_data = 'open photo_mark'))
        else:
            bts.add(btn(text = ru['text'] + ch_info.text_mark, callback_data = 'open set_mark'))
            bts.add(btn(text = ru['color']  + ch_info.color_mark, callback_data = 'open color_mark'),
                    btn(text = ru['font_style'] + ch_info.font_style, callback_data = 'open font_style '))
        bts.add(btn(text = ru['del_setting'], callback_data='open del_ch_sett'))
        
        return ru['channel_setting'].format(channel_name = ch_info.past_name_ch), bts 

    @gs_info
    def set_mark(self, user_id): 
        bts = markup()
        bts.add(btn(text = ru['back'], callback_data='open ch_sett'))
        return ru['set_watermark'], bts

    @gs_info
    def help(self, user_id):
        bts = markup()
        bts.add(btn(text = ru['back'], callback_data='open main'))
        bts.add(btn(text = ru['instrukt_desktop'], callback_data='open instruct_desktop'))
        bts.add(btn(text = ru['instrukt_android'], callback_data='open instruct_android'))
        #bts.add(btn(text = 'Поддержка', callback_data='open support'))
        return ru['support'], bts

    @gs_info
    def instruct_desktop(self, user_id):
        bts = markup()
        bts.add(btn(text = ru['back'], callback_data='open help $is_new=True'))
        
        # ============= МАГИЯ НЕ ТРОГАТЬ!!! ======  FILE_ID 
        msg_id = self.bot.send_document(user_id, 
        'CgADAgADPQMAAiyPeUj1Zvh-g7paNwI', reply_markup = bts)
        # =================================================
        return msg_id.message_id, None

    @gs_info
    def instruct_android(self, user_id):
        bts = markup()
        bts.add(btn(text = ru['back'], callback_data='open help $is_new=True'))
        msg_id = self.bot.send_video(user_id, 
        'BAADAgADNQMAAiyPeUhFeyeXLMOadQI', reply_markup = bts)    
        return msg_id.message_id, None

    @gs_info
    def del_ch_sett(self, user_Id):
        bts = markup()
        bts.add(btn(text = ru['back'], callback_data='open ch_sett'))
        bts.add(btn(text = ru['del'], callback_data='del ch_sett'))
        return ru['del_ch'], bts

    @gs_info
    def transparent_mark(self, user_id):
        return ru['set_trans_mark'], 'transparent_mark'

    @gs_info
    def photo_mark(self, user_id):
        photo_id = self.db.get_photo_mark_id(user_id)
        bts = markup()
        bts.add(btn(text = ru['back'], callback_data = 'open ch_sett $is_new=True'),
                btn(text = ru['new'], callback_data = 'open set_mark $is_new=True'))

        msg_id2 = self.bot.send_document(user_id, photo_id, reply_markup = bts)

        return msg_id2.message_id, None

    @gs_info
    def mark_size(self, user_id):
        return ru['set_size_mark'], 'mark_size'
    @gs_info
    def margin_mark(self, user_id):
        return ru['set_margin_mark'], 'margin_mark'

    @gs_info
    def pos_mark(self, user_id):
        return ru['set_pos_mark'], 'pos_mark'

    @gs_info
    def font_style(self, user_id):
        
        return ru['set_fontstyle_mark'], 'font_style'

    @gs_info     
    def color_mark(self, user_id):
        bts = markup()
        bts.add(btn(text = ru['back'], callback_data='open ch_sett'))
    
        return ru['set_color_mark'], bts

    @gs_info
    def bot_info(self, user_id):
        count_edited_post = self.db.get_bot_info()
       
        bts = markup()
        bts.add(btn(text=ru['back'], callback_data = 'open main'))
        
        return ru['bot_info'].format(count_edited_post = count_edited_post), bts


