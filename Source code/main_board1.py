## mac address:  b'0\xae\xa4\x96\xbf\x90'
## mac address decoded:  30:ae:a4:96:bf:90
##

import network
import ubinascii
import time
import dht
import machine
import bh1750fvi
import datacodec
from time import sleep
from esp import espnow
from machine import Pin
from machine import PWM
from machine import Timer
from machine import WDT
from machine import SoftI2C


#   A WLAN interface must be active to send()/recv()
wireless = network.WLAN(network.STA_IF)
wireless.active(True)					    #  Station is activated
mac = wireless.config('mac')
print('mac address: ', mac)
mac2 = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
print('mac address decoded: ', mac2)


## PIN ALLOCATION
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))     # i2c is obsolete, research on SoftI2C
dht_sensor = dht.DHT11(Pin(19))


# ESPNOW SETUP
e = espnow.ESPNow()
e.init()
hub = b'0\xae\xa4\x96\xce@'                 #  mac address of HUB
e.add_peer(hub)
id_device = 1
#  peer = b'\xec\x94\xcb[\xc2l'            #  mac address of test board
#  peer = b'\xacg\xb27}\xb0'               #  mac address of



def sensor_dht11():

    global temp, hum, error

    i = 0

    while i <= 0:

        try:

            dht_sensor.measure()
            temp = dht_sensor.temperature()
            hum = dht_sensor.humidity()
            print('Temp: ', temp)
            print('Hum: ', hum)
            i = i + 1

        except OSError as e:

            error = 'Reading error'
            print('Failed to read sensor.')
            return error
            i = i + 1


def sensor_light():

    global light

    i = 0

    while i <= 0:

        try:
            light = bh1750fvi.sample(i2c)       # in lux
            print('Lux: ', light)
            i = i + 1

        except OSError as e:

            error = 'Reading error'
            print('Failed to read sensor.')
            return error
            i = i + 1


def communication_hub():

    esp_hub = datacodec.Encoder(id_device, temp, hum, light)
    esp_hub.conversion()
    esp_hub.coding()
    packet = esp_hub.output()
    print('Data encoded: ', packet)
    e.send(hub, packet, True)


while True:

    print('PROCESS STARTING')
    sensor_dht11()
    sensor_light()
    communication_hub()
    print('PROCESS COMPLETED', '\n')
    time.sleep_ms(2000)
