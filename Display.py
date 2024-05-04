#!/usr/bin/python
# -*- coding:utf-8 -*-
# importieren von System Tools.
import sys
# importieren derv Fähigkeit für den Zugriff auf externer Dateien.
sys.path.append('lib/')

import os
# importieren für Feedback in der Konsole.
import logging
# importieren der Daten des E-Paper-Displays.
from waveshare_epd import epd1in54b_V2
# importieren von Zeitverzögerungen und co.
import time
# importieren .
from PIL import Image, ImageDraw, ImageFont
# importieren der library und aller wichtigen Daten.
logging.basicConfig(level=logging.DEBUG)
# festlegung epd
epd = epd1in54b_V2.EPD()

# Gibt Betriebs Informationen in der Konsole aus.
logging.info("epd1in54b V2 Demo")

# gibt an die Konsole den nächsten Schritt.
logging.info("init and Clear")
# überprüft ob das Display vorhanden ist.
epd.init()
# wartet eine Sekunde.
time.sleep(1)


## Gibt output in der Konsole
#logging.info("1.Das Bild wird gezeichnet...")

## Der Befehl wird in einer Variable Gespeichert.
## "1" mein das es eine Abstufung der Hellichkeit gibt.
## (epd.width, epd.height) setzt einen tuple(einen unveränderbaren Wert) zur Skalierung des Bildes
## 255 meint das die Farbe Weiß(Hellichkeitsabstufung) angezeigt wird. 0=Schwarz, 255=Weiß.
## Letzendlich löscht es einfach nur den Frame.
#blackimage = Image.new('1', (epd.width, epd.height), 255)
#redimage = Image.new('1', (epd.width, epd.height), 255)

## font ist die Schrift art. Genauer hiermit verändern wir die Schrift größe.
## os.path.join('Font.ttc') sagt das es sich aus dieser Datei die date herzieht.
## 24 meint die Schriftgröße des angezeigten Textes.
#font = ImageFont.truetype(os.path.join('Font.ttc'), 24)
#font18 = ImageFont.truetype(os.path.join('Font.ttc'), 18)
font = ImageFont.truetype(os.path.join('Font.ttc'), 24)

## Der Befehl wird wie vorhin wieder in einer Variable gespeichert.
## Die Funktion ImageDraw wird .Draw ausgeführt mit einem Parameter, der die vorhin abgeürzten Befehl beinhaltet.
#drawblack = ImageDraw.Draw(blackimage)
#drawred = ImageDraw.Draw(redimage)
        
def Display1(PM1_0, PM2_5, PM10, CO2, CO, O3, NO2, Temperature, Humidity, AQI_NO2, AQI_PM2_5, AQI_PM10, AQI_O3, Time):
    blackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    redimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
    drawblack = ImageDraw.Draw(blackimage)
    drawred = ImageDraw.Draw(redimage)
    # drawred ist die eben erstellte Variable.
    # .text führt den Befehl aus, damit ein Text, auf dem E-Ink Display, angezeigt wird.
    # (8, 12) gibt die Pixel Koordinaten, der oberen rechten Ecke an.
    # "Hello World" zeigt welcher String angezeigt werden soll.
    # font = font wählt die Schriftart die wir vorhin ausgewählt haben aus.
    # fill = 0 ist die Hellichkeit, in dem die Schriftart angezeigt wird. 0 = Schwarz, 255 = Weiß.
    drawblack.text((0, 0), f'AQI NO2: {AQI_NO2}', font = font, fill = 0)
    drawblack.text((0, 22), f'AQI PM2.5: {AQI_PM2_5}', font = font, fill = 0)
    drawblack.text((0, 44), f'AQI PM10: {AQI_PM10}', font = font, fill = 0)
    drawblack.text((0, 66), f'AQI PMO3: {AQI_O3}', font = font, fill = 0)
    drawblack.text((0, 88), f'CO2: {CO2} ppm', font = font, fill = 0)
    drawblack.text((0, 110), f'CO: {CO} ppm', font = font, fill = 0)
    drawblack.text((0, 132), f'O3: {O3} ppm', font = font, fill = 0)
    drawblack.text((0, 154), f'NO2: {NO2} ppm', font = font, fill = 0)
    
    # epd meint das E-Paper-Display.
    # .display ist der Befehl zum anzeigen der bisherigen plazierten Texte auf dem Display.
    # In den Parametern steht, dass sowohl die schwarzen als auch die roten Zeichen ausgewehlt werden.
    epd.display(epd.getbuffer(blackimage),epd.getbuffer(redimage))

    # Danach soll 1 Sekunde nicht passieren.
    time.sleep(10)
    
def Display2(PM1_0, PM2_5, PM10, CO2, CO, O3, NO2, Temperature, Humidity, AQI_NO2, AQI_PM2_5, AQI_PM10, AQI_O3, Time):
    blackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    redimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
    drawblack = ImageDraw.Draw(blackimage)
    drawred = ImageDraw.Draw(redimage)
    
    drawblack.text((0, 0), f'PM1.0: {PM1_0} Ug/m3', font = font, fill = 0)
    drawblack.text((0, 22), f'PM2.5: {PM2_5} Ug/m3', font = font, fill = 0)
    drawblack.text((0, 44), f'PM10: {PM10} Ug/m3', font = font, fill = 0)
    drawblack.text((0, 66), f'Temp.: {Temperature} °C', font = font, fill = 0)
    drawblack.text((0, 88), f'Humid.: {Humidity} %RH', font = font, fill = 0)
    drawblack.text((0, 110), f'Time: {Time}', font = font, fill = 0)
    
    epd.display(epd.getbuffer(blackimage),epd.getbuffer(redimage))

    time.sleep(10)


def Anzeigen(PM1_0, PM2_5, PM10, CO2, CO, O3, NO2, Temperature, Humidity, AQI_NO2, AQI_PM2_5, AQI_PM10, AQI_O3, Time):
    # Versucht Code auszuführen. Bei einem Error wird der Code übersprungen
    #try:  
        for i in range(2):
            Display1(PM1_0, PM2_5, PM10, CO2, CO, O3, NO2, Temperature, Humidity, AQI_NO2, AQI_PM2_5, AQI_PM10, AQI_O3, Time)
            Display2(PM1_0, PM2_5, PM10, CO2, CO, O3, NO2, Temperature, Humidity, AQI_NO2, AQI_PM2_5, AQI_PM10, AQI_O3, Time)

        
        
# Funktionen für AQI
def BewertungNO2(Wert):
    Response = "Error"
    if Wert > 200:
        Response = "v. bad"
    elif Wert >= 101:
        Response = "bad"
    elif Wert >= 41:
        Response = "OK"
    elif Wert >= 21:
        Response = "good"
    elif Wert >= 0:
        Response = "v. good"
    return Response

def BewertungPM10(Wert):
    Response = "Error"
    if Wert > 100:
        Response = "v. bad"
    elif Wert >= 51:
        Response = "bad"
    elif Wert >= 36:
        Response = "OK"
    elif Wert >= 21:
        Response = "good"
    elif Wert >= 0:
        Response = "v. good"
    return Response

def BewertungPM2_5(Wert):
    Response = "Error"
    if Wert > 50:
        Response = "v. bad"
    elif Wert >= 26:
        Response = "bad"
    elif Wert >= 21:
        Response = "OK"
    elif Wert >= 11:
        Response = "good"
    elif Wert >= 0:
        Response = "v. good"
    return Response

def BewertungO3(Wert):
    Response = "Error"
    if Wert > 240:
        Response = "v. bad"
    elif Wert >= 181:
        Response = "bad"
    elif Wert >= 121:
        Response = "OK"
    elif Wert >= 61:
        Response = "good"
    elif Wert >= 0:
        Response = "v. good"
    return Response


def Programm(PM1_0, PM2_5, PM10, CO2, CO, O3, NO2, Temperature, Humidity, Time):
    AQI_NO2 = BewertungNO2(NO2)
    AQI_PM2_5 = BewertungPM2_5(PM2_5)
    AQI_PM10 = BewertungPM2_5(PM10)
    AQI_O3 = BewertungO3(O3)
    Anzeigen(PM1_0, PM2_5, PM10, CO2, CO, O3, NO2, Temperature, Humidity, AQI_NO2, AQI_PM2_5, AQI_PM10, AQI_O3, Time)