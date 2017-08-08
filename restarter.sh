#!/bin/bash
# Author: David Del Grosso, Brian, Levitt, Liam Lawrence
# Date: July 20, 2017
# Automatically restarts camera and IMU, GPS, and temp
# data recording if it crashes

#IMU
sleep 5s
until python3 IMU.py; do
	TIME=$(date +"%F"_"%H"."%M"."%S")
    echo "$TIME" >> crashTimes/imu1.txt
	sleep 10s
done&

#GPS and temp
until python3 gps_temp.py; do
	TIME=$(date +"%F"_"%H"."%M"."%S")
	echo "$TIME" >> crashTimes/gps1.txt
	sleep 10s
done&

#Camera
while [ 1 -eq 1 ]; do
	sleep 5s
	./record.sh
	TIME=$(date +"%F"_"%H"."%M"."%S")
	echo "$Time" >> crashTimes/vid.txt
done&
