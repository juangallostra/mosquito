
import ui
import console
from socket import socket

import fly_mosquito
import dashboard
import joystick as js
import msppg

def mosquito_load_view(view):
	"""
	Load a pythonista ui view and its specific 
	components from a ui filename
	"""
	ui_view = ui.load_view(view)
	if view == 'fly_mosquito.pyui':
		stick_throttle_yaw = js.joystick(50, 150, is_throttle_stick=True)
		stick_roll_pitch = js.joystick(50, 150)
		stick_throttle_yaw.x, stick_throttle_yaw.y = 25, 115
		stick_roll_pitch.x, stick_roll_pitch.y = 385, 115
		#stick.present('sheet')
		stick_throttle_yaw.touch_ended(None)  # center the stick
		stick_roll_pitch.touch_ended(None)
		ui_view.add_subview(stick_throttle_yaw)
		ui_view.add_subview(stick_roll_pitch)
	return ui_view


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
