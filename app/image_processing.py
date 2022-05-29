# import sys
# import re

# import dill as pickle
# from nintendo import wii, switch
# from guo import grace
# from wee import woo
import cv2
# import numpy as np
from PIL import Image
from googletrans import Translator

from .find_speech import get_bubbles, Bubble, TranslatedBubble
from .typesetting import typeset_bubble

def translate_text(text):
    translator = Translator()
    translated = translator.translate(text, src="ja", dest="en").text
    translated = translated.encode("latin-1", "ignore").decode("latin-1")
    return translated


# returns 
def translate_image(filename):
    img = cv2.imread(filename)

    if img is None:
        # image bad is the do thing bad d
        # do a thing the image is badd
        return None

    bubbles = get_bubbles(img) # returns list of text bubbles
    base_img = Image.fromarray(img.copy())

    for bubble in bubbles: # translates each bubble
        translated = translate_bubble(bubble)
        # print(f"bubble:\n{bubble.clean_text()}\n{translated.translation}\n")
        typeset_bubble(base_img, translated) # puts translated text on bubble

    return base_img


# returns translated speech bubble object
def translate_bubble(bubble):
    translation = translate_text(bubble.clean_text())
    return TranslatedBubble.as_translated(bubble, translation)