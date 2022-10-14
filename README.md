# remote_monitoring
Remote Monitoring System for Plant Growth

This implements Raspberry Pi code for Plant Monitoring. There are 3 sensors used in 
the project: moisture sensor, temperature sensor and soil pH sensor. The main entry
point of the project is send_sensor_meas.py which performs the 2 following steps:

1. Collects measurement from the 3 sensors as abive and processes them.
2. Sends the measurement to a registered mobile no using Twilio library.

It also prints the message on terminal when executed from cmdline.
