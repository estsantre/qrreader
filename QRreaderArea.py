import zbar
from PIL import Image
import cv2
import numpy as np

scanner = zbar.ImageScanner()
scanner.parse_config('enable')
cap = cv2.VideoCapture(0)

template = cv2.imread('QRtemplate.png',0)
w, h = template.shape[::-1]

first_match = [0,0]

threshold = 0.5

while (True):
    ret, cv = cap.read()


    cv = cv2.cvtColor(cv, cv2.COLOR_BGR2GRAY)
    pil = Image.fromarray(cv)
    width, height = pil.size
    raw = pil.tobytes()

    res = cv2.matchTemplate(cv, template, cv2.TM_CCOEFF_NORMED)  # template 1
    loc = np.where(res >= threshold)

    for i, pt in enumerate(zip(*loc[::-1])):
        print([pt[0],pt[1]])
        if i == 0:
            first_match = pt
        else:
            if (abs(pt[0] - first_match[0]) > 10) and (abs(pt[1] - first_match[1]) < 10):
                cv2.line(cv,pt, first_match, (0,0,0),5)
            if (abs(pt[1] - first_match[1]) > 10) and (abs(pt[0] - first_match[0]) < 10):
                cv2.line(cv,pt, first_match, (0,0,0),5)

#        cv2.rectangle(cv, pt, (pt[0] + w, pt[1] + h), (0,0,0), 2)

    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image
    scanner.scan(image)

    # extract results
    for symbol in image:
        print(width,height)
        print(symbol.data)

    cv2.imshow('img', cv)

    # break the loop by pressing esc
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()