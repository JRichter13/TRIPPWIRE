# TRIPPWIRE
This repo contains code that governs a Raspberry Pi powered high altitude balloon gondola payload. The goal of the mission was to collect GPS, IMU, and temperature sensor data as well as record a video stream of the flight. The codes has to be autonomous as no RF communication would be available during the flight.

IMU.py = Collect and store IMU data 10x per second

gps_temp.py = Collect and store GPS and temperature data 1x per second, also control payload heaters

record.sh = Record and store video streams of the flight

restarter.sh = Log error time and restart any code that fails during the flight.

All of these codes are set to run on reboot.
