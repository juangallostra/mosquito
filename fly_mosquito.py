import ui
import joystick as js
import msppg
from socket import socket

def load_fly_view():
	v = ui.load_view('fly_mosquito.pyui')
	stick_1 = js.joystick(50, 150, is_throttle_stick=True)
	stick_2 = js.joystick(50, 150)
	stick_1.x = 25
	stick_1.y = 115
	stick_2.x = 385
	stick_2.y = 115
	#stick.present('sheet')
	stick_1.touch_ended(None)  # center the 
	#stick
	stick_2.touch_ended(None)
	v.add_subview(stick_1)
	v.add_subview(stick_2)
	return v

ADDR = "192.168.4.1"
PORT = 80
TIMEOUT = 4

def arm_mosquito(sender):
	'''
	Arm the Mosquito via Wifi
	'''
	data = msppg.serialize_SET_ARMED(1)
	sock.send(data)

def disarm_mosquito(sender):
	'''
	Diasrm Mosquito via Wifi
	'''
	data = msppg.serialize_SET_ARMED(0)
	sock.send(data)


