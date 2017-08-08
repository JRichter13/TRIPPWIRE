from vnpy import *
import csv
import datetime

file_name = "Data/imu1.csv"
baudrate = 115200

#Get IMU data
def getIMU():
        #Connect to sensor
        sensor = VnSensor()
        #If the sesnor is not connected it tries to reestablish connection
        #while sensor.is_connected != True:
        	#sensor.connect('/dev/ttyUSB0',baudrate)

        #It will only take data when the IMU is connected
        sensor.connect('/dev/ttyUSB0',baudrate)
        if sensor.is_connected == True:
                data = []
                imu = sensor.read_yaw_pitch_roll_magnetic_acceleration_and_angular_rates()
                yaw = imu.yaw_pitch_roll.x
                pitch = imu.yaw_pitch_roll.y
                roll = imu.yaw_pitch_roll.x
                accel = imu.accel
                gyro = imu.gyro
                mag = imu.mag
                data.append(str(yaw))
                data.append(str(pitch))
                data.append(str(roll))
                data.append(str(accel)[6:-1])
                data.append(str(gyro)[6:-1])
                data.append(str(mag)[6:-1])
		#if len(data)==6:
                        #break
                        #Return and clear data if pi running slow

        #Return yaw, pitch, roll, acceleration, gyro, and magnetic field
        sensor.disconnect()
        return data

#Format csv header
data_header = ["Date", "Time", "Yaw", "Pitch", "Roll", "Acceleration", "Gyro", "Magnetic Field"]

#Test if csv file exists
try:
        with open(file_name, 'r') as csv_file:
                reader = csv.reader(csv_file)
        with open(file_name, 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow("")
                writer.writerow("")
                writer.writerow("")
except:
        with open(file_name, 'w') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(data_header)

#Initialize continuous loop
sec2 = -1
#sensor = VnSensor()
#sensor.connect('/dev/ttyUSB0',baudrate)
while(1):
	final_data = [] #Initialize data list

        #Get standard time
	utcnow = datetime.datetime.utcnow()
	utcstr = str(utcnow)
	sec1 = sec2
	sec2 = utcstr[-6]
	#Only update once per second
	if sec1 != sec2:
		IMU_data = getIMU()
		utcstr_array = utcstr.split(' ')
		datestr = utcstr_array[0]
		timestr = utcstr_array[1]
		final_data.append(datestr)
		final_data.append(timestr)
		final_data.append(IMU_data[0])
		final_data.append(IMU_data[1])
		final_data.append(IMU_data[2])
		final_data.append(IMU_data[3])
		final_data.append(IMU_data[4])
		final_data.append(IMU_data[5])
		print(final_data)

                #Write to csv file
		with open(file_name, 'a') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(final_data)

