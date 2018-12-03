import menu_markup
from telebot.types import InlineKeyboardMarkup as markup
from telebot.types import InlineKeyboardButton as Button

class View(object):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
        
    def gs_info(func):
        def wrapper(self, user_id, **kwarg):

            print(f'Open {func.__name__} menu for {user_id}')
            print('Kwargs: ', kwarg)
            msg_id = self.db.msg_id(user_id)
            if 'is_new' in kwarg:
                try:
                    self.bot.delete_message(user_id, msg_id)
                except:
                    print('fail del msg')
                msg_id = None
                del kwarg['is_new']

            text, bts = func(self, user_id, **kwarg)

            if type(bts) is str:
                bts = menu_markup.get_bts(bts)




            if len(text.split('][')) > 1:
                print(text.split('][')[1])
                self.bot.delete_message(user_id, msg_id)
                
                msg_id2 = self.bot.send_document(user_id, (text.split('][')[1]), reply_markup = bts).message_id

            elif msg_id:
                try:
                    msg_id2 = self.bot.edit_message_text(chat_id = user_id, message_id = msg_id,
                    text = text, parse_mode = 'Markdown', reply_markup = bts).message_id
                    
                except:
                    msg_id2 = msg_id
                    print('Not modifed')
            else:
                msg_id2 = self.bot.send_message(user_id, text, parse_mode = 'Markdown', reply_markup = bts).message_id
            
            
            if not msg_id2 == msg_id:
                print('save')
                self.db.msg_id(user_id, msg_id2)
        return wrapper
        
    @gs_info
    def send(self, user_id, text, markup):
        return text, markup

    @gs_info
    def main(self, user_id):
        self.db.user_set(user_id, 'menu_select', 'main')
        text = '\_/\_/\_/ Главное меню \\\_\\\_\\\_ '
        return text, 'main'

    @gs_info
    def welcom(self, user_id):
        bts = markup()
        bts.add(Button(text='OK', callback_data='open main'))
        return 'Привет если возникнут проблемы с клавиатурой, ты можешь вызвать новую командой /start', bts
        

    @gs_info
    def ch_list(self, user_id):
        channels = self.db.get_groups_id(user_id)
        
        print(channels)
        ch_list = markup()
        ch_list.add(Button(text='⬅️ Назад', callback_data = 'open main'),
                    Button(text=' ➕ ', callback_data = 'open ch_add'))
        if channels:
            text_lis = '\_/\_/\_/ Список каналов \\\_\\\_\\\_'

            for ch in channels:
                try:
                    self.bot.get_chat(ch[0])  
                    name = ch[1]     
                except:
                    name = ch[1] + ' | Нет прав'

                ch_list.add(Button(text = name , callback_data = 'open ch_sett $ch_id=' + str(ch[0])))

        else:
            text_lis = 'Для начала добавь канал ⬇️'
       
        return text_lis, ch_list

        

    @gs_info
    def ch_add(self, user_id):
        bts = markup()  
        bts.add(Button(text = '⬅️ Назад ', callback_data='open ch_list'))
        return 'Добавь меня в администраторы, \nи отправь мне username канала\n Можно без @', bts 
        

    @gs_info
    def ch_setting(self, user_id):
        
        ch_info = self.db.get_group(user_id = user_id)
        


        print(f'View menu setting chanel  for user: {user_id}')
        

        bts = markup()
        

        try:
            print('ch_info:  ', ch_info)
            title = self.bot.get_chat(ch_info['id']).title

            if not title == ch_info['past_name_ch']:
                self.db.channel_set(user_id, 'past_name_ch', title)
                ch_info['past_name_ch'] = title

        except:
            bts.add(Button(text = 'Обновить', callback_data = 'open ch_sett'))
            bts.add(Button(text = '⬅️ Назад ', callback_data = 'open ch_list'))
            return 'Ти удалил меня из администраторов в канале: *'+ ch_info['past_name_ch'] +'*\
            Я не смогу ставить водяние знаки в етом канале, видай мне права админа и нажми Обновить', bts

        if ch_info['id_photo_mark'] == 'off' and ch_info['text_mark'] == 'off':
            bts.add(Button(text = '⬅️ Назад ', callback_data='open ch_list')) 
            text_ch_info = 'Для начала пришли мне фото (*ФАЙЛОМ*) или текст'
            self.db.user_set(user_id, 'menu_select', 'set_mark')
                
        else:
            bts.add(Button(text='⬅️ Назад ', callback_data='open ch_list'),
                    Button(text='Статус: '+ ch_info['status'], callback_data = 'set ch status'))
            bts.add(Button(text='Размер марки: ' + str(ch_info['mark_size']) + '%', callback_data = 'open mark_size'))
            bts.add(Button(text='Позиция марки: '+ ch_info['position_mark'], callback_data = 'open pos_mark'))
            bts.add(Button(text='Прозрачность: ' + str(ch_info['transparent_mark']) + '%', callback_data = 'open transparent_mark'))

            if not ch_info['id_photo_mark'] == 'off':
                bts.add(Button(text = 'Фото марки', callback_data = 'open photo_mark'))
            else:
                bts.add(Button(text = 'Текст марки: ' + ch_info['text_mark'], callback_data = 'open set_mark'))
                bts.add(Button(text = 'Цвет марки: '  + ch_info['color_mark'], callback_data = 'open color_mark'))
                bts.add(Button(text = 'Стиль шрифта марки: ' + ch_info['font_style_mark'], callback_data = 'open font_style '))
            bts.add(Button(text = 'Удалить настройки', callback_data='open del_ch_sett'))
            text_ch_info = 'Настройки канала: *' + ch_info['past_name_ch']+'*'
        return text_ch_info, bts 

    @gs_info
    def set_mark(self, user_id): 
        bts = markup()
        bts.add(Button(text = ' ⬅️ Назад  ', callback_data='open ch_sett'))
        return 'Пришли мне фото (*ФАЙЛОМ*) или текст', bts
    
    @gs_info
    def del_ch_sett(self, user_Id):
        btn = markup()
        btn.add(Button(text = ' ⬅️ Отмена  ', callback_data='open ch_sett'))
        btn.add(Button(text = 'Удалить!', callback_data='del ch_sett'))
        return 'Удалить настройки канала?', btn

    @gs_info
    def photo_mark(self, user_id):
        ch_id = self.db.user_get(user_id, 'group_select')
        photo_id = self.db.get_photo_mark_id(user_id)
        bts = markup()
        bts.add(Button(text = ' ⬅️ Назад ', callback_data = 'open ch_sett $is_new=True'),
                Button(text = 'Новая',    callback_data = 'open set_mark $is_new=True'))

        
        return 'PHG]['+photo_id, bts

    @gs_info
    def mark_size(self, user_id):
        return 'Установите размер марки', 'mark_size'

    @gs_info
    def pos_mark(self, user_id):
        return 'Вибирете позицию марки', 'pos_mark'

    @gs_info
    def font_style(self, user_id):
        text = 'Установите шрифт текста'
        return text, 'font_style'

    @gs_info     
    def color_mark(self, user_id):
        bts = markup()
        bts.add(Button(text = '⬅️ Назад', callback_data='open ch_sett'))
        text = 'Пришлите текст в формате RGBA \nnnn nnn nnn nnn'
        return text, bts

    

    @gs_info
    def bot_info(self, user_id):
        bts = markup()
        bts.add(Button(text='⬅️ Назад', callback_data = 'open main'))

        text = '''Mark Rebot v0.0.7
Обо всех возникших проблемах и предложениях по улучшению бота пишите @PavlMais
        '''

        return text, bts


