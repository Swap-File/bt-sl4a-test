#qpy:console

#Example Bluetooth Serial Script for QPython3 on Android 5.0
#connID is NOT optional

#this is the SPP UUID (Serial Port Profile)
ssp_uuid = '00001101-0000-1000-8000-00805F9B34FB'
#this is my bluetooth devices ID
BT_DEVICE_ID = '20:14:04:18:25:68'

import os
os.system('clear')
print ("Loading...")

import time
import pprint
from base64 import b64encode
from base64 import b64decode

#from androidhelper import Android  #old way
import sl4a  #new way? seems to work the same

#droid = Android() #old way
droid = sl4a.Android() #new way? seems to work the same

#stay awake
droid.wakeLockAcquirePartial()

#toggle bluetooth to get into known state
print ('Turning Bluetooth off...')
droid.toggleBluetoothState(False,False)  #turn BT off to kill old connections

print ('Turning Bluetooth on...')
while (droid.checkBluetoothState().result == False): #turn BT on
	droid.toggleBluetoothState(True,False)  
	time.sleep(1)

print ('Bluetooth is on.')
 
while True:
	#keep connection live
	while (len(droid.bluetoothActiveConnections().result) == 0):
		print ("Reconnecting..."	)
		droid.bluetoothConnect(ssp_uuid, BT_DEVICE_ID)
		time.sleep(1)
		if len(droid.bluetoothActiveConnections().result) != 0:
			#get the connID - being lazy and using the first connID in the list
			#if you have more than one bluetooth connection parse it out and find yours
			connID = list(droid.bluetoothActiveConnections().result.keys())[0]
			print ("Connected")
			print ("connID: " + connID)

	#this works for the range of 7 bit ASCII (0-127)
	#above that, correct character will not be sent
	for i in range(0, 128):
		droid.bluetoothWrite(chr(i),connID)
	
	#the encoding here is a mess, but it works for sending 8-bit values
	#b64encode changed what it requires for input and output between python 2 and 3
	for i in range(0, 256):
		droid.bluetoothWriteBinary(b64encode(chr(i).encode('latin1')).decode(),connID)
	

	while True:
		#this works for reading the range of 8-bit values (0-255)
		#requires extra encode due to changes in python 3
		if(droid.bluetoothReadReady(connID).result == True):		
			print (ord(b64decode(droid.bluetoothReadBinary(1,connID).result.encode())))
			
	while True:
		#this works for reading the range of 7 bit ASCII (0-127)
		#above that, android won't read the right characters
		if(droid.bluetoothReadReady(connID).result == True):
			print (ord((droid.bluetoothRead(1,connID).result)))
			
			
