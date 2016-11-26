import dht
import machine
import time
import urequests
from machine import I2C, Pin

url = 'http://vps.mizjo.com:8011'
headers = {'content-type': 'application/json'}
sensor = dht.DHT22(Pin(2))
time.sleep(5)

while True:
	sensor.measure()
	temp='%d.1' % (sensor.temperature())
	hum='%d.1' % (sensor.humidity())
	data = '{"Temp": '+temp+'}'
	urequests.post(url, data=data, headers=headers)
	time.sleep(5)