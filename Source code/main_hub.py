import machine
import network
import ssd1306
import ubinascii
import datacodec
import time
import OLED
from machine import SoftI2C
from machine import Pin
from time import sleep
from esp import espnow
import gc
gc.collect()



## OLED DISPLAY SETUP
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


#  OLED DISPLAY START
oled.text('EL NIDO', 35, 5)
oled.text('______________________________', 0, 10)
oled.text('WEB SERVER', 22, 30)
oled.show()
sleep(2)
oled.fill(0)
oled.text('Waiting for', 20, 20)
oled.text('CLIENT', 38, 35)
oled.show()
sleep(1)



## WIRELESS ACCESS POINT SETUP
SSID = 'EL_NIDO_WEBSERVER'
PASSWORD = '1234'
ap = network.WLAN(network.AP_IF)
ap.config(essid=SSID, password=PASSWORD)
ap.active(True)

while ap.active() == False:
  pass

print('Access point connection successful')
print(ap.ifconfig())                            # type class 'tuple'
ap_ipaddress = (ap.ifconfig()[0])
print('AP IP address: ', ap_ipaddress)


#  WIRELESS STATION INTERFACE SETUP - A WLAN interface must be active to send()/recv()
station = network.WLAN(network.STA_IF)
station.active(True)

while station.active() == False:
  pass

print('WLAN Station Interface configurated')
mac = station.config('mac')
print('MAC address of BOARD 1 HUB: ', mac)
mac = ubinascii.hexlify(network.WLAN().config('mac') , ':').decode()
print(mac)


## SOCKETS SETUP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Create STREAM TCP socket
s.bind(('', 80))
s.listen(5)
print('Sockets setup established')



# ESPNow PROTOCOL SETUP
e = espnow.ESPNow()
e.init()
peer1 = b'0\xae\xa4\x96\xbf\x90'   #  mac address of ESP32 BOARD 3
e.add_peer(peer1)
# peer = b'0\xae\xa4\x96\xceA'      #  mac address of ESP32 BOARD 2
# e.add_peer(peer2)
print('ESP-NOW protocol setup established')



## web page content
def web_page():

    html = """
    <h1 style="text-align: center;"><strong>EL NIDO Web Server</strong></h1>
    <hr />
    <table style="margin-left: auto; margin-right: auto; height: 250px; width: 600px;">
    <tbody>
    <tr style="height: 56px;">
    <td style="width: 133.55px; text-align: center; height: 56px;">
    <h4>Entrance</h4>
    </td>
    <td style="width: 126.433px; text-align: center; height: 56px;">
    <h4>Stairs</h4>
    </td>
    <td style="width: 127.617px; text-align: center; height: 56px;">
    <h4>Corridor</h4>
    </td>
    <td style="width: 184.4px; text-align: center; height: 56px;">
    <h4>Room</h4>
    </td>
    </tr>
    <tr style="height: 20px;">
    <td style="width: 133.55px; text-align: center; height: 20px;"><span style="color: #0000ff;">Temp:</span></td>
    <td style="width: 126.433px; text-align: center; height: 20px;"><span style="color: #0000ff;">Temp:</span></td>
    <td style="width: 127.617px; text-align: center; height: 20px;"><span style="color: #0000ff;">Temp:</span></td>
    <td style="width: 184.4px; text-align: center; height: 20px;"><span style="color: #0000ff;">Temp:</span></td>
    </tr>
    <tr style="height: 25.0167px;">
    <td style="width: 133.55px; text-align: center; height: 25.0167px;"><span style="color: #0000ff;">Hum:</span></td>
    <td style="width: 126.433px; text-align: center; height: 25.0167px;"><span style="color: #0000ff;">Hum:</span></td>
    <td style="width: 127.617px; text-align: center; height: 25.0167px;"><span style="color: #0000ff;">Hum:</span></td>
    <td style="width: 184.4px; text-align: center; height: 25.0167px;"><span style="color: #0000ff;">Hum:</span></td>
    </tr>
    <tr style="height: 20px;">
    <td style="width: 133.55px; text-align: center; height: 20px;"><em>Lamp 1 is</em></td>
    <td style="width: 126.433px; text-align: center; height: 20px;"><em>Lamp 2 is</em></td>
    <td style="width: 127.617px; text-align: center; height: 20px;"><em>Lamp 3 is</em></td>
    <td style="width: 184.4px; text-align: center; height: 20px;"><em>Lamp 4 is</em></td>
    </tr>
    <tr style="height: 24px;">
    <td style="width: 133.55px; text-align: center; height: 24px;"><a href="/?led=on"><button class="button">ON</button></a></td>
    <td style="width: 126.433px; text-align: center; height: 24px;"><a href="/?led=on"><button class="button">ON</button></a></td>
    <td style="width: 127.617px; text-align: center; height: 24px;"><a href="/?led=on"><button class="button">ON</button></a></td>
    <td style="width: 184.4px; text-align: center; height: 24px;"><a href="/?led=on"><button class="button">ON</button></a></td>
    </tr>
    <tr style="height: 24px;">
    <td style="width: 133.55px; text-align: center; height: 24px;"><a href="/?led=off"><button class="button button2">OFF</button></a></td>
    <td style="width: 126.433px; text-align: center; height: 24px;"><a href="/?led=off"><button class="button button2">OFF</button></a></td>
    <td style="width: 127.617px; text-align: center; height: 24px;"><a href="/?led=off"><button class="button button2">OFF</button></a></td>
    <td style="width: 184.4px; text-align: center; height: 24px;"><a href="/?led=off"><button class="button button2">OFF</button></a></td>
    </tr>
    <tr style="height: 20px;">
    <td style="width: 133.55px; text-align: center; height: 20px;">&nbsp;</td>
    <td style="width: 126.433px; text-align: center; height: 20px;">&nbsp;</td>
    <td style="width: 127.617px; text-align: center; height: 20px;">&nbsp;</td>
    <td style="width: 184.4px; text-align: center; height: 20px;">&nbsp;</td>
    </tr>
    </tbody>
    </table>
    """
    return html



## web server setup
def socket():

    global client, communication

    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    client = str(addr[0])
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    response = web_page()
    conn.send(response)
    communication = 'recv & send data'
    conn.close()



def oled_display():

    oled.fill(0)
    oled.text('ELNIDO WEBSERVER', 0, 5)
    oled.text('______________________________', 0, 10)
    oled.text(mac, 0, 25)
    oled.text(client, 0, 40)
    oled.text(communication, 0, 55)
    oled.show()


class Espnow_comm():

    def peer1_recv(self):

        global unit_di1, temp1, hum1, light1

        msg = e.irecv()
        data_raw = msg[1].decode()
        print('Data received: ', data_raw)
        unit_id1 = data_raw[0]
        temp1 = data_raw[2:4]
        hum1 = data_raw[5:8]
        light1 = data_raw[9:13]
        print(unit_id1)
        print(temp1)
        print(hum1)
        print(light1)


    def peer2_recv(self):

        global unit_di2, temp2, hum2, light2

        msg = e.irecv()
        data_raw = msg[1].decode()
        print('Data received: ', data_raw)
        unit_id2 = data_raw[0]
        temp2 = data_raw[2:4]
        hum2 = data_raw[5:8]
        light2 = data_raw[9:13]
        print(unit_id2)
        print(temp2)
        print(hum2)
        print(light2)


    def peer3_recv(self):

        global unit_di3, temp3, hum3, light3

        msg = e.irecv()
        data_raw = msg[1].decode()
        print('Data received: ', data_raw)
        unit_id3 = data_raw[0]
        temp3 = data_raw[2:4]
        hum3 = data_raw[5:8]
        light3 = data_raw[9:13]
        print(unit_id3)
        print(temp3)
        print(hum3)
        print(light3)


    def peer4_recv(self):

        global unit_di4, temp4, hum4, light4

        msg = e.irecv()
        data_raw = msg[1].decode()
        print('Data received: ', data_raw)
        unit_id4 = data_raw[0]
        temp4 = data_raw[2:4]
        hum4 = data_raw[5:8]
        light4 = data_raw[9:13]
        print(unit_id4)
        print(temp4)
        print(hum4)
        print(light4)


while True:

    socket()
    oled_display()
    dataUnit1 = Espnow_comm()
    dataUnit1.peer1_recv()


