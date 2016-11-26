import dht
import ssd1306
import machine
import time
from machine import I2C, Pin, Timer

i2c = I2C(Pin(5), Pin(4))
display = ssd1306.SSD1306_I2C(64, 48, i2c)
sensor = dht.DHT22(Pin(2))

while(1)
	sensor.measure()
	display.fill(0)
	display.show()
	temp='%d.1' % (sensor.temperature())
	hum='%d.1' % (sensor.humidity())
	display.text("T:"+temp,1,10)
	display.show()
	display.text("H:"+hum,1,20)
	display.show()
	time.sleep(5)

#display.pixel(16, 16, 1)
#print(sensor.temperature())
#print(sensor.humidity())
