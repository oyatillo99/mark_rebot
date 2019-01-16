from telebot.types import InlineKeyboardMarkup as markup
from telebot.types import InlineKeyboardButton as button



def main():
    bts = markup(row_width = 1)
    
    list_group = button(text="Список каналов", callback_data = 'open ch_list')
    help = button(text="Помощь", callback_data = 'open help')
    info = button(text="О боте", callback_data = 'open bot_info')
    bts.add(list_group, help, info)
    return bts



def mark_size():
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


def pos_mark():
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
                    button(text='↘️', callback_data='set ch position_mark down_right'))
    return bts

def font_style():
    bts = markup()
    bts.add(button(text='⬅️ Назад',  callback_data='open ch_sett'))
    bts.add(button(text='OpenSans',  callback_data='set ch font_style_mark OpenSans'))
    bts.add(button(text='Raleway',  callback_data='set ch font_style_mark Raleway'))
    bts.add(button(text='Pixel',  callback_data='set ch font_style_mark Pixel'))
    
    bts.add(button(text='Caveat',  callback_data='set ch font_style_mark Caveat'))
    bts.add(button(text='Lobster',  callback_data='set ch font_style_mark Lobster'))
    bts.add(button(text='Oswald',  callback_data='set ch font_style_mark Oswald'))
    bts.add(button(text='Pacifico',  callback_data='set ch font_style_mark Pacifico'))
    bts.add(button(text='Rubik Mono',  callback_data='set ch font_style_mark RubikMonoOne'))
    return bts  

    
def transparent_mark():
    bts = markup()
    bts.add(button(text='⬅️ Назад',  callback_data='open ch_sett'))
    bts.add(button(text='0%',  callback_data='set ch transparent_mark 100'),
            button(text='5%',  callback_data='set ch transparent_mark 95'),
            button(text='10%',  callback_data='set ch transparent_mark 90'))
    
    bts.add(button(text='15%',  callback_data='set ch transparent_mark 85'),
            button(text='20%',  callback_data='set ch transparent_mark 80'),
            button(text='25%',  callback_data='set ch transparent_mark 75'))
    
    bts.add(button(text='40%',  callback_data='set ch transparent_mark 60'),
            button(text='50%',  callback_data='set ch transparent_mark 50'),
            button(text='60%',  callback_data='set ch transparent_mark 40'))
    return bts
    
    
def margin_mark():
    bts = markup()
    bts.add(button(text='⬅️ Назад',  callback_data='open ch_sett'))
    bts.add(button(text='0 px',  callback_data='set ch margin_mark 0'),
            button(text='1 px',  callback_data='set ch margin_mark 1'),
            button(text='2 px',  callback_data='set ch margin_mark 2'))
    
    bts.add(button(text='3 px',  callback_data='set ch margin_mark 3'),
            button(text='5 px',  callback_data='set ch margin_mark 5'),
            button(text='7 px',  callback_data='set ch margin_mark 7'))
    
    bts.add(button(text='10 px',  callback_data='set ch margin_mark 10'),
            button(text='15 px',  callback_data='set ch margin_mark 15'),
            button(text='20 px',  callback_data='set ch margin_mark 20'))
    return bts


    
def get_bts(name_bts):
    return eval(name_bts)()

