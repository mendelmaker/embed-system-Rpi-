import os Temp. Sensor
import glob
import time
import RPi.GPIO as GPIO
from time import sleep 

threshold_temp = 27
hertz = 500
PIR_count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.IN)	#button
GPIO.setup(22,GPIO.OUT)	#buzzer
#GPIO.setup(27,GPIO.OUT)	#led
GPIO.setup(7,GPIO.IN)	#PIR

#initialize the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#temperature
def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()

	equals_pos = lines[1].find('t=')

	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c#, temp_f

#buzzer
def buszzer(hertz):
	GPIO.output(22,GPIO.HIGH)
	time.sleep(1/2*hertz)
	GPIO.output(22,GPIO.LOW)
	time.sleep(1/2*hertz)

#wait for button press
while True:
	if ( GPIO.input(10) == True ):
		print("Button Pressed")
		break;	
	print("waiting to start")

#after the button is pressed	
while read_temp() < threshold_temp:
	print(read_temp())
	time.sleep(1)

while True:
	GPIO.output(22,GPIO.HIGH)
	time.sleep(1/2*hertz)
	GPIO.output(22,GPIO.LOW)
	time.sleep(1/2*hertz)