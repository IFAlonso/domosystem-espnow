class Encoder():

  def __init__(self, mcu_id, temp, hum, light):

    self.mcu_id = mcu_id
    self.temp = temp
    self.hum = hum
    self.light = light

  def conversion(self):

    global temp, hum, light, unit_id

    unit_id = str(self.mcu_id)
    temp = str(self.temp)
    hum = str(self.hum)
    light = str(self.light)

  def coding(self):

    global datapacket

    if len(temp) == 1:
      data_temp = 'T' + '0' + temp
    elif len(temp) == 2:
      data_temp = 'T' + temp

    if len(hum) == 1:
      data_hum = 'H' + '00' + hum
    elif len(hum) == 2:
      data_hum = 'H' + '0' + hum
    elif len(hum) == 3:
      data_hum = 'H' + str(hum)

    if len(light) == 1:
      data_light = 'L' + '000' + light
    elif len(light) == 2:
      data_light = 'L' + '00' + light
    elif len(light) == 3:
       data_light = 'L' + '0' + light
    elif len(light) == 4:
       data_light = 'L' + light

    datapacket = unit_id + data_temp + data_hum + data_light


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
