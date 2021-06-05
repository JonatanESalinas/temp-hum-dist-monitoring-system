'''
Proyecto final de Arquitectura de Computadoras.
Interfaz de usuario para monitoreo de temperatura, humedad y nivel de agua.

Carlos Mario Bielma Avendaño A01730645
Jonatan Emanuel Salinas Ávila A01731815
Sergio Alonso Saldaña Millán A01731958

04/06/2021

    Para correr toda la interfaz:
        python3 mainRiego.py
    Para cambiar de .ui a .py:
        pyuic5 nombreArchivo.ui -o nombreArchivo.py
    Para generar el archivo Imag_rc.py:
        pyrcc5 Imag.qrc -o Imag_rc.py
'''
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MonitoreoRiego import *
import random
import datetime
import time
import threading
import serial
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import BlynkLib
import RPi.GPIO as GPIO
import adafruit_dht
import signal
import sys


# use Raspberry Pi board pin numbers
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
pinTrigger = 18
pinEcho = 24

dhtDevice = adafruit_dht.DHT11(board.D17, use_pulseio=False)

# Initialize Blynk
blynk = BlynkLib.Blynk('LZQUvA7lj5kncfTqvwxKdU4IW2r55Vgw')

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# Load default font.
font = ImageFont.load_default()


def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	GPIO.cleanup() 
	sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

bandera_detener = False
ahora_mostrando = -1

temp = -1
hum = -1
lev = -1

# Register Virtual Pin
@blynk.VIRTUAL_READ(2)
# Register Virtual Pin
@blynk.VIRTUAL_READ(3)
# Register Virtual Pin
@blynk.VIRTUAL_READ(4)
def my_read_handler():
     global temp
     #temp = random.randrange(0,10,1)
     blynk.virtual_write(2, temp)
     global hum
     #hum = random.randrange(20,30,1)
     blynk.virtual_write(3, hum)
     global lev
     #lev = random.randrange(40,60,1)
     blynk.virtual_write(4, lev)

def subir_datos_dashboard():
    print("started!")
    while True:
        blynk.run()
        
class Ui_MonitoreoRiego(QtWidgets.QMainWindow,Ui_MonitoreoRiego):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.temp_boton.clicked.connect(self.muestraDatosTemp)
        self.humedad_boton.clicked.connect(self.muestraDatosHume)
        self.nivel_boton.clicked.connect(self.muestraDatosNivel)
        self.stop_boton.clicked.connect(self.detener_muestra_datos)
        hiloDash = threading.Thread(target=subir_datos_dashboard)
        hiloDash.start()
        
    def limpiaTabla(self):
        miSistemaRiego.tablaDatos.clearContents()
        miSistemaRiego.tablaDatos.setRowCount(0)

    def muestraDatosTemp(self):
        global ahora_mostrando
        ahora_mostrando = 1
        
        self.limpiaTabla()

        hiloTemp = threading.Thread(target=self.insertaDatosTemp)
        hiloTemp.start()


    def insertaDatosTemp(self):
        global bandera_detener
        bandera_detener = False
        
        while(ahora_mostrando == 1 and bandera_detener == False):
            print("bandera_detener: " + str(bandera_detener))
            try:
                numRandom = dhtDevice.temperature
            except RuntimeError as error:
                numRandom = numRandom
            global temp
            temp = numRandom
            print(numRandom)
            text = "Temperature(C°):"
            (font_width, font_height) = font.getsize(text)
            draw.text(
                (oled.width // 2 - font_width // 2, oled.height // 4 - font_height // 2),
                text,
                font=font,
                fill=255,
            )
            text1 = str(numRandom) 
            draw.text(
            (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
            text1,
            font=font,
            fill=255,
            )
            # Display image
            oled.image(image)
            oled.show()
            time.sleep(0.01)
            
            datoDate = datetime.datetime.now()
            fecha = str(datoDate.day) + "/" + str(datoDate.month) + "/" + str(datoDate.year)
            hora = str(datoDate.hour) + ":" + str(datoDate.minute) + ":" + str(datoDate.second)

            renglonPos = miSistemaRiego.tablaDatos.rowCount()
            miSistemaRiego.tablaDatos.insertRow(renglonPos)
            miSistemaRiego.tablaDatos.setItem(renglonPos , 0, QtWidgets.QTableWidgetItem(str(numRandom)))
            miSistemaRiego.tablaDatos.setItem(renglonPos , 1, QtWidgets.QTableWidgetItem(fecha))
            miSistemaRiego.tablaDatos.setItem(renglonPos , 2, QtWidgets.QTableWidgetItem(hora))

            time.sleep(1)
            # Draw a smaller inner rectangle
            draw.rectangle(
              (BORDER, BORDER, oled.width - BORDER - -7, oled.height - BORDER - -7),
              outline=0,
              fill=0,
            )
            oled.image(image)
            oled.show()
            time.sleep(0.01)
            

    def muestraDatosHume(self):
        global ahora_mostrando
        ahora_mostrando = 2
        
        self.limpiaTabla()

        hiloHume = threading.Thread(target=self.insertaDatosHume)
        hiloHume.start()        

    def insertaDatosHume(self):
        global bandera_detener
        bandera_detener = False
        
        while(ahora_mostrando == 2 and bandera_detener == False):
            print("bandera_detener: " + str(bandera_detener))
            try:
                numRandom= dhtDevice.humidity
            except RuntimeError as error:
                numRandom = numRandom
            global hum
            hum = numRandom
            print(numRandom)
            text = "Humidity(%):"
            (font_width, font_height) = font.getsize(text)
            draw.text(
                (oled.width // 2 - font_width // 2, oled.height // 4 - font_height // 2),
                text,
                font=font,
                fill=255,
            )
            text1 = str(numRandom) 
            draw.text(
            (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
            text1,
            font=font,
            fill=255,
            )
            # Display image
            oled.image(image)
            oled.show()
            time.sleep(0.01)
            datoDate = datetime.datetime.now()
            fecha = str(datoDate.day) + "/" + str(datoDate.month) + "/" + str(datoDate.year)
            hora = str(datoDate.hour) + ":" + str(datoDate.minute) + ":" + str(datoDate.second)

            renglonPos = miSistemaRiego.tablaDatos.rowCount()
            miSistemaRiego.tablaDatos.insertRow(renglonPos)
            miSistemaRiego.tablaDatos.setItem(renglonPos , 0, QtWidgets.QTableWidgetItem(str(numRandom)))
            miSistemaRiego.tablaDatos.setItem(renglonPos , 1, QtWidgets.QTableWidgetItem(fecha))
            miSistemaRiego.tablaDatos.setItem(renglonPos , 2, QtWidgets.QTableWidgetItem(hora))            

            time.sleep(1)      
             # Draw a smaller inner rectangle
            draw.rectangle(
              (BORDER, BORDER, oled.width - BORDER - -7, oled.height - BORDER - -7),
              outline=0,
              fill=0,
            )
            oled.image(image)
            oled.show()
            time.sleep(0.01)  

    def muestraDatosNivel(self):
        global ahora_mostrando
        ahora_mostrando = 3
        
        self.limpiaTabla()

        hiloNivel = threading.Thread(target=self.insertaDatosNivel)
        hiloNivel.start()

    def insertaDatosNivel(self):
        global bandera_detener
        bandera_detener = False
        
        while(ahora_mostrando == 3 and bandera_detener == False):
            print("bandera_detener: " + str(bandera_detener))
            # set Trigger to HIGH
            GPIO.output(pinTrigger, True)
            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(pinTrigger, False)

            startTime = time.time()
            stopTime = time.time()

            # save start time
            while 0 == GPIO.input(pinEcho):
                startTime = time.time()

            # save time of arrival
            while 1 == GPIO.input(pinEcho):
                stopTime = time.time()

            # time difference between start and arrival
            TimeElapsed = stopTime - startTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            distance = (TimeElapsed * 34300) / 2
            numRandom = round(distance,2)
            global lev
            lev = numRandom
            print(numRandom)
            text = "H2O level(m):"
            (font_width, font_height) = font.getsize(text)
            draw.text(
                (oled.width // 2 - font_width // 2, oled.height // 4 - font_height // 2),
                text,
                font=font,
                fill=255,
            )
            text1 = str(numRandom) 
            draw.text(
            (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
            text1,
            font=font,
            fill=255,
            )
            # Display image
            oled.image(image)
            oled.show()
            time.sleep(0.01)
            
            datoDate = datetime.datetime.now()
            fecha = str(datoDate.day) + "/" + str(datoDate.month) + "/" + str(datoDate.year)
            hora = str(datoDate.hour) + ":" + str(datoDate.minute) + ":" + str(datoDate.second)

            renglonPos = miSistemaRiego.tablaDatos.rowCount()
            miSistemaRiego.tablaDatos.insertRow(renglonPos)
            miSistemaRiego.tablaDatos.setItem(renglonPos , 0, QtWidgets.QTableWidgetItem(str(numRandom)))
            miSistemaRiego.tablaDatos.setItem(renglonPos , 1, QtWidgets.QTableWidgetItem(fecha))
            miSistemaRiego.tablaDatos.setItem(renglonPos , 2, QtWidgets.QTableWidgetItem(hora))

            time.sleep(1)  
            # Draw a smaller inner rectangle
            draw.rectangle(
              (BORDER, BORDER, oled.width - BORDER - -7, oled.height - BORDER - -7),
              outline=0,
              fill=0,
            )
            oled.image(image)
            oled.show()
            time.sleep(0.01)

    def detener_muestra_datos(self):
        global bandera_detener
        bandera_detener = True
        global ahora_mostrando
        ahora_mostrando = -1

        print("lo puse en: " + str(bandera_detener))
        print("Detener!")
        
    

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    miSistemaRiego = Ui_MonitoreoRiego()
    miSistemaRiego.show()
    app.exec_()
