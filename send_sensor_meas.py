#!/usr/bin/python

import time
import board
import adafruit_dht
import os
from twilio.rest import Client
import spidev
import time
import datetime as dt
import io
import sys
import fcntl
import copy
import string
from AtlasI2C import (
         AtlasI2C
)

DEFAULT_TEMP = 60
DELAY = 0.2
NUM_MOISTURE_MEAS = 50
TEMP_HIST_FILE = "temp_hist.csv"

def get_devices():
	device = AtlasI2C()
	device_address_list = device.list_i2c_devices()
	device_list = []

	for i in device_address_list:
		try:
			device.set_i2c_address(i)
			response = device.query("I")
			moduletype = response.split(",")[1] 
			response = device.query("name,?").split(",")[1]
		except Exception:
			continue
		device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
	return device_list


def get_todays_temp():
	dhtDevice = adafruit_dht.DHT11(board.D17)
	for i in range(100):
	        try:
	                temperature_c = dhtDevice.temperature
        	        temperature_f = temperature_c * (9 / 5) + 32
	                humidity = dhtDevice.humidity
        	        return temperature_f
	        except RuntimeError as error:
        	        pass
        	time.sleep(5)
	return  -1


def send_todays_temp_and_moisture_and_pH():
	account_sid = "AC4e6bd38a02ec20478fa1caf668434116"
	auth_token = "3fa734f4d8164ae9d1a4c98ccddfc3af"
	client = Client(account_sid, auth_token)
	todays_temp = get_todays_temp()
	avg_temp = get_average_temp(todays_temp)
	avg_temp = round(avg_temp, 3)

	todays_moisture = get_soil_moisture()
	todays_moisture = round(todays_moisture, 3)

	todays_pH = get_pH()

	msg_body = f"From Raspberry Pi: Avg temp={avg_temp}, Soil Moisture={todays_moisture}%, Soil pH={todays_pH}. "
	msg_body += "To make the soil more acidic, a remedy would be to either add lemon peels or orange peels to the soil. "
	msg_body += "To make to soil more alkaline, a remedy would be to thoroughly mix baking soda in the soil. "
	phone_numbers = ['+19087239883', '+19082793566']
	for num in phone_numbers:
		message = client.messages.create(
			body = msg_body,
         		from_='+15102567788',
         		to=num
     		)
	return msg_body


def get_average_temp(todays_temp):
	# three steps:
	# 1. read last 2 days from a file
	# 2. get todays temparature
	# 3. get average
	# return this
	last_few_days_temp = read_temp_hist()
	sum_temp = todays_temp + sum(last_few_days_temp)
	save_temp_to_file(last_few_days_temp, todays_temp)
	return sum_temp/(len(last_few_days_temp))


def get_soil_moisture():
	spi = spidev.SpiDev()
	spi.open(0,0)
	spi.max_speed_hz=1000000
	all_moisture_levels = []
	for x in range(NUM_MOISTURE_MEAS):
		val = readChannel(0, spi)
		if val < 200:
			val = 200
		elif val > 1000:
			val = 1000
		if (val != 0):
			all_moisture_levels.append(val)
		time.sleep(DELAY)
	if len(all_moisture_levels) == 0:
		return 25

	avg_moist_lvl = 1.0 * sum(all_moisture_levels)/len(all_moisture_levels)
	pct_moist_lvl = 100 - ((avg_moist_lvl-200)/100)*12.5
	return pct_moist_lvl

def readChannel(channel, spi):
	val = spi.xfer2([1,(8+channel)<<4,0])
	data = ((val[1]&3) << 8) + val[2]
	return data


def read_temp_hist():
	temp_hist = []
	with open(TEMP_HIST_FILE) as file:
		for line in file:
			temp_hist.append(float(line))

	return temp_hist[-2:]


def save_temp_to_file(temp_hist, todays_temp):
	temp_hist.append(todays_temp)
	temp_hist = temp_hist[-2:]
	today_date = str(dt.datetime.now().date())
	file_change_date = str(
		dt.datetime.fromtimestamp(os.path.getmtime(TEMP_HIST_FILE)).date()
	)
	if today_date == file_change_date:
		return
	with open(TEMP_HIST_FILE, "w") as file:
		file.write('\n'.join(str(temp) for temp in temp_hist))
	return


def get_pH():
	device_list = get_devices()
	device = device_list[0]
	pH_meas = []

	for i in range(10):
		delaytime = device.long_timeout
		try:
			device.write("R")
			time.sleep(delaytime)
			meas_str = device.read().strip("\x00")
			new_pH = meas_str.split(":")[1].strip()
			pH_meas.append(float(new_pH))
		except:
			continue

	if len(pH_meas) == 0:
		return  6.9878

	return 1.0 * sum(pH_meas)/len(pH_meas)


if __name__ == '__main__':
	print(send_todays_temp_and_moisture_and_pH())

