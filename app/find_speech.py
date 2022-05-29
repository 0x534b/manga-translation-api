import re

import numpy as np
import cv2

from PIL import Image
from pytesseract import image_to_string


class Bubble(object):
    def __init__(self, x, y, w, h, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text

    def clean_text(self):
        text = self.text
        text = re.sub(r"\n", "", text)
        return text

    def __unicode__(self):
        return str(self.x)+','+str(self.y)+' '+str(self.w)+'x'+str(self.h)+' '+ self.text


class TranslatedBubble(Bubble):
    def __init__(self, x, y, w, h, text, translation):
        Bubble.__init__(self, x, y, w, h, text)
        self.translation = translation

    @classmethod
    def as_translated(cls, parent, translation):
        return cls(parent.x,
                    parent.y,
                    parent.w,
                    parent.h,
                    parent.text,
                    translation)

# parameters helpful for increasing tesseract-ocr accuracy for Japanese
def tesseract_params():
    params = ""
    params += "--psm 12"

    configParams = []
    def configParam(param, val):
      return "-c " + param + "=" + val

    configParams.append(("chop_enable", "T"))
    configParams.append(('use_new_state_cost','F'))
    configParams.append(('segment_segcost_rating','F'))
    configParams.append(('enable_new_segsearch','0'))
    configParams.append(('textord_force_make_prop_words','F'))
    configParams.append(('tessedit_char_blacklist', '}><L'))
    configParams.append(('textord_debug_tabfind','0'))
    params += " ".join([configParam(p[0], p[1]) for p in configParams])
    return params


# find and returns a list of text bubbles 
def get_bubbles(img): 
    # preprocess image for easier reading
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.bitwise_not(cv2.adaptiveThreshold(img_gray, 255, cv2.THRESH_BINARY, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 75, 10)) #contrast

    kernel = np.ones((2,2),np.uint8)
    img_gray = cv2.erode(img_gray, kernel,iterations = 2)
    img_gray = cv2.bitwise_not(img_gray)

    # find potential bubbles
    contours, hierarchy = cv2.findContours(img_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    pruned_contours = []
    mask = np.zeros_like(img)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    height, width, channel = img.shape

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100 and area < ((height / 3) * (width / 3)):
            pruned_contours.append(cnt)

    # find contours for the mask for a second pass after pruning the large and small contours
    cv2.drawContours(mask, pruned_contours, -1, (255,255,255), 1)

    Image.fromarray(mask).save('oi.jpg')

    new_contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    # final_mask = cv2.cvtColor(np.zeros_like(img), cv2.COLOR_BGR2GRAY)

    # grab the text from the bubbles
    bubbles = []
    for contour in new_contours:
        area = cv2.contourArea(contour)

        # filter to only reasonable sized bubbles
        if area > 6000:
            drawing_mask = cv2.cvtColor(np.zeros_like(img), cv2.COLOR_BGR2GRAY)

            # approximating polygonal curves  
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

            cv2.fillPoly(drawing_mask, [approx], (255, 0, 0))
            
            masked = cv2.bitwise_and(drawing_mask, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

            x = approx[:, 0, 0].min()
            y = approx[:, 0, 1].min()
            width = approx[:, 0, 0].max() - x
            height = approx[:, 0, 1].max() - y

            masked = masked[y:y + height, x:x + width]
            pil_cutout = Image.fromarray(masked)

            # run OCR
            text = image_to_string(pil_cutout, lang='jpn_vert', config=tesseract_params())

            if text:
                bubble = Bubble(x, y, width, height, text)
                bubbles.append(bubble)

    # 🤩 🔫 
    return bubbles


