# import math
# import os

# from guo import grace
from PIL import Image, ImageDraw, ImageFont
# from dill import pickle

from .find_speech import TranslatedBubble 

# function to help format the translated bubble
def text_wrap(text, w, font=None, min_word_on_line=0.3):
    def text_width(line):
        if line:
            return drawing.textsize(line, font=font)[0]
        else:
            return 0

    drawing_image = Image.new("RGB", (100, 100))
    drawing = ImageDraw.Draw(drawing_image)

    lines = []
    idx = 0
    line = ""
    
    while idx < len(text):
        if not line and text[idx] == "":
            idx += 1

        running_width = text_width(line)
        next_token = text.find(" ", idx + 1)

        if next_token != -1:
            c_text = text[idx:next_token]

        else:
            c_text = text[idx:]
        
        c_width = text_width(c_text)
        fit = float(w - running_width) / c_width

        if fit > 0.95:
            line += c_text
            idx += len(c_text)

        else:
            if len(line) > 0:
                lines.append(line)
                line = ""

            else:
                split = max(int(fit * len(c_text)) / 2, 1)
                c_text = c_text[:split] + "-"
                lines.append(c_text)
                idx += len(c_text) - 1

    if len(line) > 0:
        lines.append(line)

    return "\n".join(lines)

# actually typesetting the bubbles in the right places
def typeset_bubble(img, bubble):
    if isinstance(bubble, TranslatedBubble):
        text = bubble.translation

    else:
        text = bubble.text

    area = bubble.w * bubble.h
    font_size = 16
    font = ImageFont.truetype("arial.ttf", font_size)
    # font = ImageFont.truetype("app/unifont-14.0.03.ttf")#font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', size=fontsize)
    draw_thingo = ImageDraw.Draw(img)
    wrap = text_wrap(text, bubble.w, font=font)
    size = draw_thingo.textsize(wrap, font=font)
    
    x = (bubble.x + bubble.w // 2) - (size[0] // 2)
    y = (bubble.y + bubble.h // 2) - (size[1] // 2)
    
    img.paste((255,255,255), (x, y, x + size[0], y + size[1]))
    draw_thingo.text((x,y), wrap.strip(), fill=(0,0,0), font=font) #yessir