from libs.oscilloscope.tek import TDS1012B
import matplotlib.pyplot as plt
#import requests

device = TDS1012B()

device.set_channel(1)

device.get_scale_parameters(device.channel1)

for n in range(1000):
     print ("Now output file" + str(n) + "." + str(1000 - n) +"to go.\n")
     outfile = open("data/1225/"+str(n)+".data", 'w+')
     e = device.get_wave_form(device.channel1)
     x, y = device.wave.get_wave()
     #print(x, y)
     for _x, _y in zip(x,y):
          outfile.write(str(_x) +  '\t' +  str(_y) + '\n')
     outfile.close()
     # resp = requests.post("localhost:9900", data = data)

