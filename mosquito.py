
import ui
import console
from socket import socket

import fly_mosquito
import dashboard
import joystick as js
import msppg

def mosquito_load_view(view):
	v = ui.load_view(view)
	if view == 'fly_mosquito.pyui':
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


# Main class for the app that switches beween views
class Mosquito(ui.View):

	def __init__(self, address='192.168.4.1', port=80, timeout=4):
		
		# view handling
		self.view_names = ['dashboard.pyui', 'fly_mosquito.pyui']
		self.view_index = 0
		self.view_array = []
		
		# load and hide views
		for i in range(len(self.view_names)):
			self.view_array.append(mosquito_load_view(self.view_names[self.view_index]))
			self.add_subview(self.view_array[self.view_index])
			self.view_array[self.view_index].hidden = True
			
			self.view_index += 1
			
		# bind actions
		self.view_array[0]['fly_button'].action = self.switch_to_fly
		
		self.view_array[0].hidden = False
		self.present('fullscreen', orientations=['portrait', 'landscape'])
		
		# Connection data
		self._address = address
		self._port = port
		self._timeout = timeout
		self._sock = socket()
		self._sock.settimeout(self._timeout)
		try:
			self._sock.connect((self._address, self._port))
		except:
			console.alert('Could not connect to the Mosquito')	
		
	def switch_views(self):
			for i in range(len(self.view_array)):
				self.view_array[i].hidden = True
			self.view_array[self.view_index].hidden = False
			self.name = self.view_names[self.view_index]
			
	def switch_to_fly(self, sender):
			self.view_index = (self.view_index + 1) % len(self.view_array)
			self.switch_views()


def main():
	Mosquito()
	
if __name__ == '__main__':
	main()
