import dht
import machine
import time
import socket
import ssd1306

from machine import I2C, Pin

sensor = dht.DHT22(Pin(2))
#i2c = I2C(Pin(5), Pin(4))
#display = ssd1306.SSD1306_I2C(64, 48, i2c)
time.sleep(5)
addr=socket.getaddrinfo("vps.mizjo.com",8011)[0][-1]
s=socket.socket()
s.connect(addr)

while True:
	sensor.measure()
#	display.fill(0)
#	display.show()
	temp='%d.1' % (sensor.temperature())
	hum='%d.1' % (sensor.humidity())
#	display.text("T:"+temp,1,10)
#	display.show()
#	display.text("H:"+hum,1,20)
#	display.show()
	data= 'Device=001,Temp='+temp+',Humidity='+hum+'\r\n'
	s.send(data)
	time.sleep(5)