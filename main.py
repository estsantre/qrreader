import zbar
from PIL import Image
import cv2
import math

scanner = zbar.ImageScanner()
scanner.parse_config('enable')
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, cv = cap.read()
    Originalcv = cv
    cv = cv2.cvtColor(cv, cv2.COLOR_BGR2GRAY)
    pil = Image.fromarray(cv)
    width, height = pil.size
    raw = pil.tobytes()
    
    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image
    scanner.scan(image)

    # extract results
    for symbol in image:

        [a, b, c, d] = symbol.location  # four corners of the QR code in an order
        w = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        h = math.sqrt((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2)
        Area = w * h

        cv2.putText(Originalcv, '%s' %(Area) ,(10,30), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.circle(Originalcv,(a[0],a[1]), 10, (255, 0, 0), -1)
        cv2.circle(Originalcv, (b[0], b[1]), 10, (0, 255, 0), -1)
        cv2.circle(Originalcv, (d[0], d[1]), 10, (0, 0, 255), -1)
        cv2.line(Originalcv,(a[0],a[1]), (b[0], b[1]), (255, 255, 0), 2)
        cv2.line(Originalcv, (a[0],a[1]), (d[0], d[1]), (255, 255, 0), 2)

        print(symbol.data)
        print(Area)

        #cv2.circle(Originalcv, (c[0], c[1]), 5, (0, 0, 255), -1)

    #cv2.imshow('img', cv)
    cv2.imshow('Original', Originalcv)
    
    # break the loop by pressing esc
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
