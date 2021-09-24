import cv2
import numpy as np
import pytesseract
import re
class Dictionary:
   def slicee(self,text):
       text = text.replace("    ","")
       regex = "[\]* [\S]*,"
       deu = re.findall(regex,text)
       regex = ",.*[\S]*"
       pol = re.findall(regex,text)
       #deu = str(deu).replace("\n","")
       #pol = str(pol).replace("\n","")
       #deu = deu.replace(",","")
       #pol = pol.replace(",","")
       #deu = str(deu).replace("    ","")
       #pol = str(pol).replace("    ","")
       return [deu,pol]

    def ocrImage(ImagePath):
        # Load Image
        image = cv2.imread(str(ImagePath))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Smooth out image
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        image = cv2.filter2D(image, -1, kernel)
        # Denoise image
        image = cv2.medianBlur(image,5)
        # OCR the image
        custom_config = r'-l pol+deu --oem 3 --psm 6 -c tessedit_char_whitelist="AĄBCĆEĘFGHIJKLŁMNŃOÓPRSŚTUVWXŹZŻaąbcćdeęfghijklłmnńoópqrsśtuvwxźyzżäÄéöÖüÜUß -,"'
        ocr = pytesseract.image_to_string(image, config=custom_config)
        # Return string
        return str(ocr)

    def splitDeuPol(text):

        #NIE DOTYKAĆ To Rozdziela polskie i niemieckie słówka!!!
        regex = " [-*_]([^\s]*) "
        text = re.sub(regex,"",text)
        #Usun podwojne linie
        regex = "\n\n"
        text = re.sub(regex,"\n",text)

        return str(text)

#print(splitDeuPol(ocrImage('image.jpg')))
text = """
    das Boot,łódka
    der Bus,autobus
    das Fahrrad,rower
    das Flugzeug,samolot
    die S-Bahn,szybka kolej miejska
    das Schiff,statek
    die U-Bahn,metro
    der Zug,pociąg
    mit dem Flugzeug fliegen,latać samolotem
    mit dem Zug fahren,jeździć pociągiem
    bequem,wygodnie
    besichtigen,zwiedzać
    das Fahrrad,rower
    die Fahrt,jazda
    der Flughafen,lotnisko
    die GroBstadt,duże miasto
    der Hafen,port
    halten,zatrzymywać się
    der Hauptbahnhof,dworzec główny
    die Hauptstadt,stolica
    der Kanal,kanał
    kennenlernen,poznawać
    langweilig,nudno
    laut,głośno
    leihen,pożyczać
    liegen,leżeć
    der Parkplatz, parking, miejsce parkingowe
    schnell,szybko
    die StraBe,ulica
    teuer,drogo
    die Apotheke,apteka
    der Bahnhof,dworzec kolejowy
    die Bank,bank
    das Hotel,hotel
    das Kino,kino
    das Krankenhaus, er szpital
    der Park,park
    die Post,poczta
    das Restaurant,restauracjo
    die Schule,szkoła
    der Supermarkt,superno
    das Theater,teatr
    """
dick = Dictionary()
print(dick.slicee(text)[1][2])