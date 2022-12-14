#!/usr/bin/env python

import RPi.GPIO as GPIO
from gpiozero import Servo
import time
from time import sleep
from gpiozero import LED

TRIG = 17  # send-pin
ECHO = 18  # receive-pin
servo_pin = 14
servo_pin2 = 8
led = LED(5)
led2= LED(9)
led3= LED(6)
DHTPIN = 27
MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT, initial=False)
GPIO.setup(servo_pin2, GPIO.OUT, initial=False)


def read_dht11_dat():
	GPIO.setup(DHTPIN, GPIO.OUT)
	GPIO.output(DHTPIN, GPIO.HIGH)
	time.sleep(0.05)
	GPIO.output(DHTPIN, GPIO.LOW)
	time.sleep(0.02)
	GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

	unchanged_count = 0
	last = -1
	data = []
	while True:
		current = GPIO.input(DHTPIN)
		data.append(current)
		if last != current:
			unchanged_count = 0
			last = current
		else:
			unchanged_count += 1
			if unchanged_count > MAX_UNCHANGE_COUNT:
				break

	state = STATE_INIT_PULL_DOWN

	lengths = []
	current_length = 0

	for current in data:
		current_length += 1

		if state == STATE_INIT_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_INIT_PULL_UP
			else:
				continue
		if state == STATE_INIT_PULL_UP:
			if current == GPIO.HIGH:
				state = STATE_DATA_FIRST_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_FIRST_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_DATA_PULL_UP
			else:
				continue
		if state == STATE_DATA_PULL_UP:
			if current == GPIO.HIGH:
				current_length = 0
				state = STATE_DATA_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_PULL_DOWN:
			if current == GPIO.LOW:
				lengths.append(current_length)
				state = STATE_DATA_PULL_UP
			else:
				continue
	if len(lengths) != 40:
		#print ("Data not good, skip")
		return False

	shortest_pull_up = min(lengths)
	longest_pull_up = max(lengths)
	halfway = (longest_pull_up + shortest_pull_up) / 2
	bits = []
	the_bytes = []
	byte = 0

	for length in lengths:
		bit = 0
		if length > halfway:
			bit = 1
		bits.append(bit)
	#print ("bits: %s, length: %d" % (bits, len(bits)))
	for i in range(0, len(bits)):
		byte = byte << 1
		if (bits[i]):
			byte = byte | 1
		else:
			byte = byte | 0
		if ((i + 1) % 8 == 0):
			the_bytes.append(byte)
			byte = 0
	#print (the_bytes)
	checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
	if the_bytes[4] != checksum:
		#print ("Data not good, skip")
		return False

	return the_bytes[0], the_bytes[2]
def distance():
    GPIO.output(TRIG, 1)  # ???Trig??????10US??????????????????
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    # ??????????????????????????????????????????
    while GPIO.input(ECHO) == 0:  # ?????? echo ??????????????????
        pass
    time1 = time.time()

    # ??????????????????????????????????????????
    while GPIO.input(ECHO) == 1:  # ?????? echo ??????????????????
        pass
    time2 = time.time()

    during = time2 - time1
    # ECHO???????????????????????????????????????????????????????????????????????????????????????
    return during * 340 / 2 * 100


# ????????????????????????340m/s,?????????????????????????????????????????????100
def loop():
    while True:
        dis = distance()
        print (dis, 'cm')
        print ('')
        result = read_dht11_dat()
        if result:
            humidity, temperature = result
            print ("humidity: %s %%,  Temperature: %s C`" % (humidity, temperature))
            time.sleep(1)
        time.sleep(0.3)
        if dis < 5:
            led.on()
            led2.off()
            led3.off()
            p.ChangeDutyCycle(angleToDutyCycle(0))
            sleep(0.1)
            p.ChangeDutyCycle(0)
            sleep(3)
            q.ChangeDutyCycle(angleToDutyCycle(90))
            sleep(0.1)
            q.ChangeDutyCycle(0)
            sleep(3)
            p.ChangeDutyCycle(angleToDutyCycle(120))
            sleep(0.1)
            p.ChangeDutyCycle(0)
            sleep(1)
            q.ChangeDutyCycle(angleToDutyCycle(0))
            sleep(0.1)
            q.ChangeDutyCycle(0)
        if dis<10 and dis>5:
            led3.on()
            led.off()
            led2.off()
        if dis>10:
            led.off()
            led3.off()
            led2.on()
            
    


def destroy():
    GPIO.cleanup()


def angleToDutyCycle(angle):
    return 2.5 + angle / 180.0 * 10


p = GPIO.PWM(servo_pin, 50)  # ???????????????50HZ
p.start(angleToDutyCycle(120))  # ????????????????????????90
sleep(0.5)
p.ChangeDutyCycle(0)  # ?????????????????????????????????????????????
q = GPIO.PWM(servo_pin2, 50)    # ???????????????50HZ
q.start(angleToDutyCycle(90))  # ????????????????????????90
sleep(0.5)
q.ChangeDutyCycle(0)           # ?????????????????????????????????????????????
if __name__ == "__main__":

    try:
        loop()

    except KeyboardInterrupt:
        destroy()


