class Encoder_sensors():

  def __init__(self, mcu_id, temp, hum, light):

    self.mcu_id = mcu_id
    self.temp = temp
    self.hum = hum
    self.light = light

  def coding(self):

    global unit_id, temp, hum, light, datapacket

    unit_id = 'ID' + str(self.mcu_id)
    
    if len(str(self.temp)) == 0:
      data_temp = 'T' + '00' + str(sefl.temp)
    elif len(str(self.temp)) == 1:
      data_temp = 'T' + '0' + str(self.temp)
    elif len(str(self.temp)) == 2:
      data_temp = 'T' + str(self.temp)

    if len(str(self.hum)) == 0:
      data_hum = 'H' + '000' + str(self.hum)
    elif len(str(self.hum)) == 1:
      data_hum = 'H' + '00' + str(self.hum)
    elif len(str(self.hum)) == 2:
      data_hum = 'H' + '0' + str(self.hum)
    elif len(str(self.hum)) == 3:
      data_hum = 'H' + str(self.hum)

    if len(str(self.light)) == 0:
      data_light = 'L' + '0000' + str(self.light)
    elif len(str(self.light)) == 1:
      data_light = 'L' + '000' + str(self.light)
    elif len(str(self.light)) == 2:
      data_light = 'L' + '00' + str(self.light)
    elif len(str(self.light)) == 3:
       data_light = 'L' + '0' + str(self.light)
    elif len(str(self.light)) == 4:
       data_light = 'L' + str(self.light)

    datapacket = unit_id + data_temp + data_hum + data_light

  def output(self):

    return datapacket



class Encoder_switches():

  def __init__(self, mcu_id, switch1, switch2):

    self.mcu_id = mcu_id
    self.switch1 = switch1
    self.switch2 = switch2
    
  def coding(self):

    global unit_id, switch1, switch2, datapacket

    unit_id = 'ID' + str(self.mcu_id)
    switch1 = 'SW1' + str(self.switch1)
    switch2 = 'SW2' + str(self.switch2)
    datapacket = unit_id + switch1 + switch2

  def output(self):

    return datapacket



class Decoder():

  def __init__(self, datapacket):

    self.datapacket = datapacket


  def decode(self):

    global unit_id, temperature, humidity, light

    data = str(self.datapacket)

    print('Data: ', data)

    unit_id = data[0]
    temperature = data[2:4]
    humidity = data[5:8]
    light = data[9:13]

    return unit_id, temperature, humidity, light


## EXAMPLE
board = 1
temperature = 23
humidity = 55
lux = 105

sensor1 = Encoder_sensors(board, temperature, humidity, lux)
sensor1.coding()
print(sensor1.output())
