#!/usr/bin/env python2
# There are a variety of RFID readers out there, USB and non-USB variants.
# This might create problems in recognizing the reader you are using.
# We haven't found the silver bullet yet. If you can contribute to this 
# quest, please comment in the issue thread or create pull requests.
# ALTERNATIVE SCRIPTS:
# If you encounter problems with this script Reader.py
# consider and test one of the alternatives in the same scripts folder.
# Replace the Reader.py file with one of the following files:
# * Reader.py.experimental
#     This alternative Reader.py script was meant to cover not only USB readers but more.
#     It can be used to replace Reader.py if you have readers such as
#     MFRC522 or RDM6300
# * Reader.py.kkmoonRFIDreader
#     KKMOON RFID Reader which appears twice in the devices list as HID 413d:2107
#     and this required to check "if" the device is a keyboard.

import string
#import csv
import os.path
import sys

from evdev import InputDevice, categorize, ecodes, list_devices
from select import select

def get_devices():
    return [InputDevice(fn) for fn in list_devices()]

class Reader:
    reader = None

	def __init__(self):
	    self.reader = self
		path = os.path.dirname(os.path.realpath(__file__))
		self.keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
		if not os.path.isfile(path + '/deviceName.txt'):
			sys.exit('Please run RegisterDevice.py first')
		else: 
			with open(path + '/deviceName.txt','r') as f:
				deviceName = f.read()
			devices = get_devices()
			for device in devices:
				if device.name == deviceName:
					self.dev = device
					break 		
			try:
				self.dev
			except:
				sys.exit('Could not find the device %s\n. Make sure is connected' % deviceName)
		
	def readCard(self):
		stri=''
		key = ''
		while key != 'KEY_ENTER':
		   r,w,x = select([self.dev], [], [])
		   for event in self.dev.read():
			if event.type==1 and event.value==1:
				stri+=self.keys[ event.code ]
				#print( keys[ event.code ] )
				key = ecodes.KEY[ event.code ]
		return stri[:-1]
		