from . import menu_markup
from telebot.types import InlineKeyboardMarkup as markup
from telebot.types import InlineKeyboardButton as Button

class View(object):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
        
    def gs_info(func):
        def wrapper(self, user_id, **kwarg):
            print('Kwargs: ', kwarg)
            msg_id = self.db.msg_id(user_id)
            if 'is_new' in kwarg:
                self.bot.delete_message(user_id, msg_id)
                msg_id = None

            text, buttons = func(self, user_id)
            
            if len(text.split('][')) > 1:
                print(text.split('][')[1])
                self.bot.delete_message(user_id, msg_id)
                
                msg_id2 = self.bot.send_photo(user_id, (text.split('][')[1]), reply_markup = buttons)

            elif msg_id:
                msg_id2 = self.bot.edit_message_text(chat_id = user_id, message_id = msg_id,
                text = text, parse_mode = 'Markdown', reply_markup = buttons)
            else:
                msg_id2 = self.bot.send_message(user_id, text, parse_mode = 'Markdown', reply_markup = buttons)
            
            
            if not msg_id2.message_id == msg_id:
                print('save')
                self.db.msg_id(user_id, msg_id2.message_id)
        return wrapper
        
    @gs_info
    def send(self, user_id, text, markup):
        return text, markup

    @gs_info
    def main(self, user_id):
        print(f'View menu main for user: {user_id}')
        self.db.user_set(user_id, 'menu_select', 'main')
        text = '--- Главное меню: ---'
        return text, menu_markup.main_bts()


    def welcom(self, user_id):
        print(f'View welcom menu for user: {user_id}')

        bts = markup()
        bts.add(Button(text='OK', callback_data='open main'))
        
        self.bot.send_message(user_id,
        'Привет если возникнут проблемы с клавиатурой, ты можешь вызвать новую командой /menu', reply_markup = bts)
        

    @gs_info
    def ch_list(self, user_id):
        print(f'View menu list chanels for user: {user_id}')
        
        channels = self.db.get_groups_id(user_id)

        ch_list =  markup()
        ch_list.add(Button(text='⬅️ Назад', callback_data = 'open main'),
                    Button(text=' ➕ ', callback_data = 'open ch_add'))
        if channels:
            text_lis = '=-=- Список каналов: -=-='

            for ch in channels:
                try:
                    name_group = self.bot.get_chat(ch).title
                except Exception as e:
                    print(e)
                    name_group = 'Я не админ'
                
                ch_list.add(Button(text=name_group,\
                callback_data = 'open ch_sett $ch_id=' + str(ch)))

        else:
            text_lis = 'Для начала добавь канал ⬇️'
       
        return text_lis, ch_list

        

    @gs_info
    def ch_add(self, user_id):
        bts = markup()  
        bts.add(Button(text = '⬅️ Назад ', callback_data='open ch_list'))
        return 'Добавь меня в администраторы, \nи отправь мне username канала', bts 
        

    @gs_info
    def ch_setting(self, user_id):
        
        ch_info = self.db.get_group(user_id = user_id)
        print(f'View menu setting chanel  for user: {user_id}')
        
        bts = markup()
        bts.add(Button(text = '⬅️ Назад ', callback_data='open ch_list')) 
        
        if ch_info['id_photo_mark'] == 'off' and ch_info['text_mark'] == 'off':
            text_ch_info = 'Пришлите текст или фото марку'
            self.user_set(user_id, 'menu_select', 'set_mark')
                
        else:
            bts.add(Button(text='Статус: '        + ch_info['status'], callback_data = 'set ch status'))
            bts.add(Button(text='Размер марки: '  + str(ch_info['mark_size']) + '%', callback_data = 'open mark_size'))
            bts.add(Button(text='Позиция марки: ' + ch_info['position_mark'], callback_data = 'open pos_mark'))

            if not ch_info['id_photo_mark'] == 'off':
                bts.add(Button(text = 'Фото марки', callback_data = 'open photo_mark'))
            else:
                bts.add(Button(text = 'Текст марки: ' + ch_info['text_mark'], callback_data = 'open set_mark'))
                bts.add(Button(text = 'Цвет марки: '  + ch_info['color_mark'], callback_data = 'open color_mark'))
                bts.add(Button(text = 'Стиль шрифта марки: ' + ch_info['font_style_mark'], callback_data = 'open font_style '))

            text_ch_info = 'Настройки канала: *' + self.bot.get_chat(ch_info['id']).title+'*'
        return text_ch_info, bts 

    @gs_info
    def set_mark(self, user_id): 
        bts = markup()
        bts.add(Button(text = ' ⬅️ Назад  ', callback_data='open ch_sett'))
        return 'Пришлите текст или фото марку', bts

    @gs_info
    def photo_mark(self, user_id):
        ch_id = self.db.user_get(user_id, 'group_select')
        photo_id = self.db.get_photo_mark_id(user_id)
        bts = markup()
        bts.add(Button(text = '⬅️ Назад ', callback_data = 'open ch_sett $is_new=True'),
                Button(text = 'Новая',    callback_data = 'open set_mark $is_new=True'))

        
        return 'PHG]['+photo_id, bts

    @gs_info
    def mark_size(self, user_id):
        return 'Установите размер марки', menu_markup.size_bts()

    @gs_info
    def pos_mark(self, user_id):
        return 'Вибирете позицию марки', menu_markup.pos_bts()

    @gs_info
    def font_style(self, user_id):
        text = 'Установите шрифт текста'
        return text, menu_markup.fonts_button()

    @gs_info     
    def color_mark(self, user_id):
        bts = markup()
        bts.add(Button(text = ' ⬅️ Назад  ', callback_data='open ch_sett'))
        text = 'пришлите текст в формате RGBA \nnnn nnn nnn nnn'
        return text, bts

    

    @gs_info
    def bot_info(self, user_id):
        bts = markup()
        bts.add(Button(text='⬅️ Назад', callback_data = 'open main'))

        text = '''Mark Rebot v0.0.8
Обо всех возникших проблемах и предложениях по улучшению бота пишите @PavlMais
        '''

        return text, bts


