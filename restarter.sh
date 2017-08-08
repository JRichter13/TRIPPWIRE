#!/bin/bash
# Author: Liam Lawrence
# Date: July 20, 2017
# Automatically restarts the program if it crashes and
# records the time it failed

sleep 5s
until python3 IMU_10x.py; do
	TIME=$(date +"%F"_"%H"."%M"."%S")
	echo "$TIME" >> crashTimes/imu1.txt
	sleep 10s
done&

until python3 try_main.py; do
	TIME=$(date +"%F"_"%H"."%M"."%S")
	echo "$TIME" >> crashTimes/gps1.txt
	sleep 10s
done&
while [ 1 -eq 1 ]; do
	sleep 5s
	./record.sh
	TIME=$(date +"%F"_"%H"."%M"."%S")
	echo "$Time" >> crashTimes/vid.txt
done&
