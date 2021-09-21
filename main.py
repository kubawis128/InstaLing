import cv2
import numpy as np
import filters as fl
import pytesseract
import re
image = cv2.imread('image.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
image = cv2.filter2D(image, -1, kernel)
image = cv2.medianBlur(image,5)
custom_config = r'-l pol+deu --oem 3 --psm 6 -c tessedit_char_whitelist="AĄBCĆEĘFGHIJKLŁMNŃOÓPRSŚTUVWXŹZŻaąbcćdeęfghijklłmnńoópqrsśtuvwxźyzżß -,"'
ocr = pytesseract.image_to_string(image, config=custom_config)
regex = " [-*_]([^\s]*) " #NIE DOTYKAĆ To Rozdziela polskie i niemieckie słówka!!!
ocr = re.sub(regex,"",ocr)
print(str(ocr))