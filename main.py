import dht
import machine
import time
import socket
import ubinascii
import network
from machine import Pin	
from time import sleep_ms

sensor = dht.DHT22(Pin(2))

##########################################################
SSID = 'yai'
PASSWORD = 'schumacher14'
INTERVAL=60000
##########################################################

rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
led = Pin(2, Pin.OUT)

def led_flash(count,waiton,waitoff):
	for i in range(count):
		led.low()
		time.sleep_ms(waiton)
		led.high()
		time.sleep_ms(waitoff)
	return

def connect_network():
	led.low()
	sta_if = network.WLAN(network.STA_IF)
	sta_if.active(True)
	sta_if.connect(SSID, PASSWORD)
	attempts=0
	print('NET: Connecting to network...')
	while not sta_if.isconnected():
	    attempts += 1
	    time.sleep_ms(1000)
	    print('..')
	print('NET: Connected:', sta_if.ifconfig())
	led.high()
	mac=ubinascii.hexlify(sta_if.config('mac'),'-').decode()
	return mac

def main():
	if machine.reset_cause() == machine.DEEPSLEEP_RESET:
	    print('SYS: Woke from a deep sleep')
	else:
	    print('SYS: Power on or hard reset')

	mac=connect_network();

	while True:
		try:
			addr=socket.getaddrinfo("vps.mizjo.com",8011)[0][-1]
		except OSError:
			print('SOCK: getaddress Fail!')
			led_flash(3,100,50)
			machine.reset()
		try:
			s=socket.socket()
		except OSError:
			print('SOCK: Create Fail!')
			led_flash(5,100,50)
			machine.reset()
		try:
			s.connect(addr)
		except OSError:
			print('SOCK: Connect Fail!')
			led_flash(7,100,50)
			machine.reset()
		
		print('SOCK: Socket Open to vps.mizjo.com')
		time.sleep(1)
		sensor.measure()
		temp='%d.1' % (sensor.temperature())
		hum='%d.1' % (sensor.humidity())
		print('DHT: Measurement complete')
		data= 'MAC='+mac+',Temp='+temp+',Humidity='+hum+'\r\n'
		print(data)
		s.send(data)
		print('SYS: Going into deep sleep!')
		time.sleep(1)
		rtc.alarm(rtc.ALARM0, INTERVAL)
		machine.deepsleep()

if __name__ == '__main__':
		main()
