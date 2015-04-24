#qpy:console

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
			#get the connIDd - being lazy and using the first (and only) connID in the list
			#if I had more than one bluetooth connection at a time I would need to find my connID
			#conID is NOT OPTIONAL and MUST Be used when reading data
			connID = list(droid.bluetoothActiveConnections().result.keys())[0]
			
			print ("Connected")
			print ("connID: " + connID)

	#this works for the range of 7 bit ASCII (0-127)
	#above that, android won't send the right characters
	print ("Sending 256 characters one at a time")
	start_time = time.time()
	for j in range(0, 2):	
		for i in range(0, 128):
			droid.bluetoothWrite(chr(i),connID)
	print("--- %s seconds ---" % (time.time() - start_time))
	#about 0.58 seconds on my S4
	
	print ("Sending 256 characters as a list")
	start_time = time.time()
	data = []
	for j in range(0, 2):	
		for i in range(0, 128):
			data.append(chr(i))
	droid.bluetoothWrite(data,connID)
	print("--- %s seconds ---" % (time.time() - start_time))
	#about 0.0044 seconds on my S4
	
	#the data encoding here is a mess, but it works to send 8-bit values
	#b64encode changed what it requires for input and output between python 2 and 3
	print ("Sending 256 bytes one at a time")
	start_time = time.time()
	for i in range(0, 256):
		droid.bluetoothWriteBinary(b64encode(bytearray([i])).decode(),connID)
	print("--- %s seconds ---" % (time.time() - start_time))
	#about 0.57 seconds on my S4
	

	#the data encoding here is a mess, but it works to send 8-bit values
	#b64encode changed what it requires for input and output between python 2 and 3
	print ("Sending 256 bytes as a byte array")
	start_time = time.time()
	data = bytearray()
	for i in range(0, 256):
		data.append(i)
	droid.bluetoothWriteBinary(b64encode(data).decode(),connID)
	print("--- %s seconds ---" % (time.time() - start_time))
	#about 0.0025 seconds on my S4
	
	while True:
		#this works for the range of 8-bit values (0-255)
		#requires extra encode due to changes in python 3
		if(droid.bluetoothReadReady(connID).result == True):		
			print (ord(b64decode(droid.bluetoothReadBinary(1,connID).result.encode())))
			
	while True:
		#this works for the range of 7 bit ASCII (0-127)
		#above that, android won't read the right characters
		if(droid.bluetoothReadReady(connID).result == True):
			print (ord((droid.bluetoothRead(1,connID).result)))
			
			
