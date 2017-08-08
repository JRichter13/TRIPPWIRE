# David Del Grosso
# 2017/08/03
# This code reads GPS and temperature sensor data once per second
# and prints it to a csv file

import csv
import datetime
import serial
import Adafruit_MCP9808.MCP9808 as MCP9808 
import RPi.GPIO as GPIO

#Change before launch
file_name = "Data/gps1.csv"
chan = 5

#Setup relay GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(chan, GPIO.OUT)
GPIO.output(chan, False)

#Function to get the temperature from the MCP9808 Sensors
def getTemp(A):
	sensor = MCP9808.MCP9808(address=A)
	sensor.begin()
	temp = sensor.readTempC()
	return temp

#Get GPS data
def getGPS():
	#Open serial port
	GPS = serial.Serial('/dev/ttyAMA0',9600)
	
	data = [] #Initialize data list
	try:
		while(1):
			while GPS.inWaiting()==0:
				pass
			NMEA = GPS.readline()
			if NMEA.startswith(b'$GPGGA'): #Find GGA lines
				NMEA = str(NMEA)[1:]
				NMEA_array = NMEA.split(',')
				lat = str(NMEA_array[2])+str(NMEA_array[3])
				lon = str(NMEA_array[4])+str(NMEA_array[5])
				alt = str(NMEA_array[9])+str(NMEA_array[10])
				data.append(lat)
				data.append(lon)
				data.append(alt)
			if len(data)>=3:
				break
	
		#Close serial port
		GPS.close()
	except:
		print("Fail Inside")
		GPS.close()

	#Return latitude, longitude, and altitude
	return data

#Format csv header
data_header = ["Date", "Time", "Latitude", "Longitude", "Altitude", "Temperature1 C", "Temperature2 C"]

#Test if csv file exists
try:
	with open(file_name, 'r') as csv_file:
		reader = csv.reader(csv_file)
	with open(file_name, 'a') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow("")
		writer.writerow("")
		writer.writerow("")
#If not, create one
except:
	with open(file_name, 'w') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(data_header)

#Initialize continuous loop
sec2 = -1

"""
GPS = serial.Serial('/dev/ttyAMA0',9600)
sensor = VnSensor()
sensor.connect('/dev/ttyUSB0',9600)
"""
while(1):
	final_data = [] #Initialize data list
	
	#Get standard time
	utcnow = datetime.datetime.utcnow()
	utcstr = str(utcnow)
	sec1 = sec2
	sec2 = utcstr[-8]
	
	#Only update once per second
	if sec1 != sec2:
		try:
			GPS_data = getGPS() #get GPS reading
		except:
			print("Fail Outside")
		#IMU_data = getIMU()
		try:
			temp_data1 = getTemp(0x18) #get Temp 1 reading
		except:
			print("Fail Temp")
			temp_data1 = 20 #set default temp to 20
		try:
			temp_data2 = getTemp(0x1F) #get Temp 2 reading
		except:
			print("Fail Temp2")
			temp_data2 = 20 #set default temp to 20

		utcstr_array = utcstr.split(' ')
		datestr = utcstr_array[0]
		timestr = utcstr_array[1]
		final_data.append(datestr)
		final_data.append(timestr)
		try:
			final_data.append(GPS_data[0])
			final_data.append(GPS_data[1])
			final_data.append(GPS_data[2])
			final_data.append(temp_data1)
			final_data.append(temp_data2)
		except:
			print("Fail Append")
		print(final_data)
		
		#Write to csv file
		with open(file_name, 'a') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(final_data)
	#Set temperature ranges to control heaters
	if temp_data1 < 10 or temp_data2 < 10:
		GPIO.output(chan, True)
	elif temp_data1 < 15 and temp_data2 < 15:
		GPIO.output(chan, True)
	elif temp_data1 > 40 or temp_data2 > 40:
		GPIO.output(chan, False)
	elif temp_data1 > 35 and temp_data2 > 35:
		GPIO.output(chan, False)
	else:
		GPIO.output(chan, False)

	if temp_data1 == 20 and temp_data2 == 20:
		GPIO.output(chan, False)
