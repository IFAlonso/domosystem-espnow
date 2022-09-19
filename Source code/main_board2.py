import machine
import network
import ubinascii
import datacodec
import time
from machine import Pin
from time import sleep
from esp import espnow
import gc
gc.collect()


#  WIRELESS STATION INTERFACE SETUP - A WLAN interface must be active to send()/recv()
station = network.WLAN(network.STA_IF)
station.active(True)

while station.active() == False:
  pass

print('WLAN Station Interface configurated')
mac = station.config('mac')
print('MAC address of BOARD 2: ', mac)
mac = ubinascii.hexlify(network.WLAN().config('mac') , ':').decode()
print(mac)


# ESPNow PROTOCOL SETUP
e = espnow.ESPNow()
e.init()
peer1 = b'0\xae\xa4\x96\xbf\x90'   #  mac address of ESP32 BOARD 3
e.add_peer(peer1)
# peer = b'0\xae\xa4\x96\xceA'      #  mac address of ESP32 BOARD 2
# e.add_peer(peer2)
print('ESP-NOW protocol setup established')


## PIN allocation
light = Pin(19, Pin.OUT)

def light_test():
    
    while True:
        
        light.on()
        time.sleep_ms(1000)
        light.off()
        time.sleep_ms(1000)


def hub_recv():

    global unit_di1, temp1, hum1, light1

    msg = e.irecv()
    data_raw = msg[1].decode()
    print('Data received: ', data_raw)
    
    
light_test()
