class ChInfo(object):
    def __init__(self, data):
        self.id           = data['id']
        self.user_id      = data['user_id']
        self.status       = data['status']
        self.photo_id     = data['id_photo_mark']
        self.text_mark    = data['text_mark']
        self.mark_size    = data['mark_size']
        self.color_mark   = data['color_mark']
        self.transparent  = data['transparent_mark']
        self.past_name_ch = data['past_name_ch']
        self.pos_mark     = data['position_mark']
        self.font_style   = data['font_style_mark']
        self.del_or_edit  = 'del'
        self.margin_mark  = data['margin_mark']
        self.type_mark    = 'photo' if self.text_mark == 'off' else 'text'

       
      
    