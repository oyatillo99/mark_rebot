
class CallBack(object):
    def __init__(self, view, db):
        self.view = view
        self.db = db
        self.map_method = {
            'main'      : view.main,
            'ch_add'    : view.ch_add,
            'ch_sett'   : view.ch_setting,
            'ch_list'   : view.ch_list,
            'set_mark'  : view.set_mark,
            'mark_size' : view.mark_size,
            'pos_mark'  : view.pos_mark,
            'font_style': view.font_style,
            'photo_mark': view.photo_mark,
            'bot_info'  : view.bot_info,
        }


    def main(self, call):
        print(f'\nUser {call.from_user.first_name}, id:{call.from_user.id}, send data: {call.data}')
        user_id = call.from_user.id
        data = call.data.split('$')
        cmd = data[0].split()
        if len(data) == 2:
            args = dict(e.split('=') for e in data[1].split(', '))
        else:
            args = {}

        if cmd[0] == 'set':
            if cmd[1] == 'ch':
                if cmd[2] == 'status':
                    self.db.switch_status(user_id)
                else:
                    print(cmd)
                    self.db.channel_set(user_id, cmd[2], cmd[3])
                self.view.ch_setting(user_id)

        elif cmd[0] == 'open':
            if 'ch_id' in args:
                print(99)
                self.db.user_set(user_id, 'group_select', args['ch_id'])
                args = {}
            self.db.user_set(user_id, 'menu_select', cmd[1])
            self.map_method[cmd[1]](user_id, **args)
            
