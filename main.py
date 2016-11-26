import dht
import machine
import time
import socket
from machine import I2C, Pin

sensor = dht.DHT22(Pin(2))

time.sleep(5)

addr=socket.getaddrinfo("vps.mizjo.com",8011)[0][-1]
s=socket.socket()
s.connect(addr)

while True:
	sensor.measure()
	temp='%d.1' % (sensor.temperature())
	hum='%d.1' % (sensor.humidity())
	data = '{"Temp": '+temp+'}'
	print(data)
	print(s.send(data))
	time.sleep(5)
	