import time
import board
import adafruit_dht
dhtDevice = adafruit_dht.DHT11(board.D17)
for i in range(10):
	try:
		temperature_c = dhtDevice.temperature
		temperature_f = temperature_c * (9 / 5) + 32
		humidity = dhtDevice.humidity
		print(f"Temp = {temperature_f} deg F, humidity={humidity}")
	except RuntimeError as error:
		pass
	time.sleep(5)
