import dht
import machine
import time
import socket
import ubinascii
#import ssd1306
import network
from machine import I2C, Pin
sensor = dht.DHT22(Pin(2))

##########################################################
SSID = 'yai'
PASSWORD = 'schumacher14'
INTERVAL=30000
##########################################################
#i2c = I2C(Pin(5), Pin(4))
#display = ssd1306.SSD1306_I2C(64, 48, i2c)
led = Pin(2, Pin.OUT)
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
else:
    print('power on or hard reset')

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        pass
print('Network configuration:', sta_if.ifconfig())

mac=ubinascii.hexlify(sta_if.config('mac'),':').decode()

while True:
	addr=socket.getaddrinfo("vps.mizjo.com",8011)[0][-1]
	s=socket.socket()
	try:
		s.connect(addr)
	except OSError:
		print('Connect Exception, rebooting!')
		led.low()
		time.sleep(5)
		machine.reset()

	print('Socket Open to vps.mizjo.com')
	print('Measuring DHT')
	sensor.measure()
	#display.fill(0)
	#display.show()
	temp='%d.1' % (sensor.temperature())
	hum='%d.1' % (sensor.humidity())
	#display.text("T:"+temp,1,10)
	#display.show()
	#display.text("H:"+hum,1,20)
	#display.show()
	data= 'MAC='+mac+',Temp='+temp+',Humidity='+hum+'\r\n'
	print(data)
	s.send(data)
	print('Going into deep sleep!')
	time.sleep(5)
	rtc.alarm(rtc.ALARM0, INTERVAL)
	machine.deepsleep()