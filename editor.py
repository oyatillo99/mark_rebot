from pprint import pprint
import uuid
from io import BytesIO
from numpy import array as np_arr
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip

class Editor(object):
    def edit_gif(self, info, gif_path, mark = None):
        out_file = str(uuid.uuid4()) + '.mp4'
        base = VideoFileClip(gif_path)

        if mark is None:
            wmark = self.txt_mark(base.size, info)
        else:
            wmark = Image.open(BytesIO(mark)).convert('RGBA')

        wmark = self.preparation_mark(info, wmark, base.size)   
        mark = ImageClip( np_arr(wmark) ).set_position(
            self.pos_conf(*base.size, *wmark.size, info))
        
        out = CompositeVideoClip([base, mark])
        out.duration = base.duration
        out.write_videofile(out_file, threads = None)
        return out_file


    def preparation_mark(self, info, mark, base_size):
        # cut and set transparent
        wm = Image.eval(mark, # Set transparent
            lambda x: int((x /100) * info.transparent))
        mark_size = int(((sum(base_size) / 2) / 100) * info.mark_size)
        wpercent  = (mark_size / float( wm.size[0] ))
        hsize     = int((float(wm.size[1]) * float(wpercent)))
        return wm.resize((mark_size,hsize), Image.ANTIALIAS)

    def edit_photo(self, info, photo, mark = None):
        base = Image.open(BytesIO(photo)).convert('RGBA')

        if mark is None:
            wt_mark = self.txt_mark(base.size, info)
        else:
            wt_mark = Image.open(BytesIO(mark)).convert('RGBA')

        watermark   = self.preparation_mark(info, wt_mark, base.size)
        out = Image.new('RGBA', base.size, (0,0,0,0))
        out.paste(base, (0,0))
        out.paste(watermark, mask=watermark,
        box = self.pos_conf(*base.size, *watermark.size, info))

        bytes_photo = BytesIO()
        out = out.convert('RGB')
        out.save(bytes_photo, format='jpeg')
        return bytes_photo
    
    def pos_conf(self, main_W, main_H, mark_W, mark_H, info):
        position = info.pos_mark
        margin   = info.margin_mark
        if position == 'top_left':
            return margin, margin
        elif position == 'top':
            return int(main_W / 2) - int(mark_W / 2), margin
        elif position == 'top_right':
            return main_W - mark_W - margin, margin
        elif position == 'center_left':
            return margin, int(main_H / 2) - int(mark_H / 2)
        elif position == 'center':
            return int(main_W / 2) - int(mark_W/2), int(main_H/2) - int(mark_H/2)
        elif position == 'center_right':
            return main_W - mark_W - margin, int(main_H / 2) - int(mark_H / 2)
        elif position == 'down_left':
            return margin, main_H - mark_H
        elif position == 'down':
            return int(main_W / 2) - int(mark_W / 2), main_H - mark_H - margin
        elif position == 'down_right':
            return main_W - mark_W - margin, main_H - mark_H - margin   
        else:
            raise 'Error key position'

    def txt_mark(self, b_size, info):
        print(b_size)
        color = tuple(map(int, info.color_mark.split()))
        path_font_style = 'fonts/' + info.font_style + '.ttf'

        txt = Image.new('RGBA', (1000,1000), (255,255,255,0))
        fnt = ImageFont.truetype(path_font_style, 68)
        
        txt_img  = ImageDraw.Draw(txt)
        txt_size = txt_img.textsize(info.text_mark, fnt)
        txt_img.text((0, 0), info.text_mark, font = fnt, fill = color)
        txt = txt.crop((0, 0, *txt_size)) # cut everything apart text
        return txt
        