from telebot.types import InlineKeyboardMarkup as markup
from telebot.types import InlineKeyboardButton as button

def main_bts():
    bts = markup(row_width=1)

    list_group = button(text="Список каналов", callback_data = 'open ch_list')
    setting = button(text="Настройки", callback_data = 'f f f')
    info = button(text="О боте", callback_data = 'main bot_info')
    bts.add(list_group,info)
    return bts



def size_bts(ch_id):
    bts = markup()  
    bts.add(button(text='⬅️ Назад', callback_data='open ch_sett ' + ch_id),
                    button(text='%7', callback_data='set mark_size 7'),
                    button(text='%9', callback_data='set mark_size 9'))
    bts.add(button(text='%11', callback_data='set mark_size 11'),
                    button(text='%13', callback_data='set mark_size 13'),
                    button(text='%15', callback_data='set mark_size 15'))
    bts.add(button(text='%18', callback_data='set mark_size 18'),
                    button(text='%22', callback_data='set mark_size 22'),
                    button(text='%28', callback_data='set mark_mark_size 28'))
    return bts


def pos_bts():
    bts = markup()
    bts.add(button(text='⬅️ Назад',  callback_data='set set'))

    bts.add(button(text='↖️',     callback_data='set pos top_left'),
                    button(text='⬆️', callback_data='set pos top'),
                    button(text='↗️', callback_data='set pos top_right'))

    bts.add(button(text='⬅️',     callback_data='set pos center_left'),
                    button(text='⬛', callback_data='set pos center'),
                    button(text='➡️', callback_data='set pos center_right'))
                    
    bts.add(button(text='↙️',     callback_data='set pos down_left'), 
                    button(text='⬇️', callback_data='set pos down'),
                    button(text='↘️', callback_data='set pos down_rignt'))
    return bts

def fonts_button():
    bts = markup()
    bts.add(button(text='⬅️ Назад',  callback_data='set set'))
    bts.add(button(text='OpenSans',  callback_data='set font OpenSans'))
    bts.add(button(text='Raleway',  callback_data='set font Raleway'))
    bts.add(button(text='Pixel',  callback_data='set font Pixel'))
    return bts

    





