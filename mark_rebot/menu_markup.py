from telebot.types import InlineKeyboardMarkup as markup
from telebot.types import InlineKeyboardButton as button

def main_bts():
    bts = markup(row_width=1)

    list_group = button(text="Список каналов", callback_data = 'open ch_list')
    setting = button(text="Настройки", callback_data = 'f f f')
    info = button(text="О боте", callback_data = 'open bot_info')
    bts.add(list_group,info)
    return bts



def size_bts():
    bts = markup()  
    bts.add(button(text='⬅️ Назад', callback_data='open ch_sett'),
                    button(text='7%', callback_data='set ch mark_size 7'),
                    button(text='9%', callback_data='set ch mark_size 9'))
    bts.add(button(text='11%', callback_data='set ch mark_size 11'),
                    button(text='13%', callback_data='set ch mark_size 13'),
                    button(text='15%', callback_data='set ch mark_size 15'))
    bts.add(button(text='18%', callback_data='set ch mark_size 18'),
                    button(text='22%', callback_data='set ch mark_size 22'),
                    button(text='28%', callback_data='set ch mark_size 28'))
    return bts


def pos_bts():
    bts = markup()
    bts.add(button(text='⬅️ Назад',  callback_data='open ch_sett'))

    bts.add(button(text='↖️',     callback_data='set ch position_mark top_left'),
                    button(text='⬆️', callback_data='set ch position_mark top'),
                    button(text='↗️', callback_data='set ch position_mark top_right'))

    bts.add(button(text='⬅️',     callback_data='set ch position_mark center_left'),
                    button(text='⬛', callback_data='set ch position_mark center'),
                    button(text='➡️', callback_data='set ch position_mark center_right'))
                    
    bts.add(button(text='↙️',     callback_data='set ch position_mark down_left'), 
                    button(text='⬇️', callback_data='set ch position_mark down'),
                    button(text='↘️', callback_data='set ch position_mark down_rignt'))
    return bts

def fonts_button():
    bts = markup()
    bts.add(button(text='⬅️ Назад',  callback_data='open ch_sett'))
    bts.add(button(text='OpenSans',  callback_data='set ch font_style_mark OpenSans'))
    bts.add(button(text='Raleway',  callback_data='set ch font_style_mark Raleway'))
    bts.add(button(text='Pixel',  callback_data='set ch font_style_mark Pixel'))
    return bts

    





