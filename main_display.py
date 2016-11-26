import dht
#import ssd1306
import machine
import time
import dht
import urequests
from machine import I2C, Pin, Timer
url = 'http://vps.mizjo.com:8011'
headers = {'content-type': 'application/json'}
#i2c = I2C(Pin(5), Pin(4))
#display = ssd1306.SSD1306_I2C(64, 48, i2c)
sensor = dht.DHT22(Pin(2))
time.sleep(5)

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
	data = '{"Temp": '+temp+'}'
	urequests.post(url, data=data, headers=headers)
	time.sleep(5)