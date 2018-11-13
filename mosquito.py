
import ui
import console
from socket import socket

import fly_mosquito
import dashboard
import joystick as js

import msppg

# Connection constants
ADDRESS = '192.168.4.1'
PORT = 80
TIMEOUT = 4

def mosquito_load_view(view):
	"""
	Load a pythonista ui view and its specific 
	components from a ui filename
	"""
	ui_view = ui.load_view(view)
	if view == 'fly_mosquito.pyui':
		stick_throttle_yaw = js.joystick(50, 150,'left_stick', is_throttle_stick=True)
		stick_roll_pitch = js.joystick(50, 150, 'right_stick')
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

	def __init__(self, address=ADDRESS, port=PORT, timeout=TIMEOUT):
		
		# view handling
		self.view_dict = {'dashboard.pyui':None, 'fly_mosquito.pyui':None}
		
		# load and hide views
		for key in self.view_dict.keys():
			# Load view, add it to the main view and hide it
			self.view_dict[key] = mosquito_load_view(key)
			self.add_subview(self.view_dict[key])
			self.view_dict[key].hidden = True
			
		# bind actions
		# dashboard view actions
		self.view_dict['dashboard.pyui']['btn_fly'].action = self._switch_to_fly
		self.view_dict['dashboard.pyui']['btn_arm'].action = self.arm_mosquito
		self.view_dict['dashboard.pyui']['btn_disarm'].action = self.disarm_mosquito
		self.view_dict['dashboard.pyui']['slider_motor_1'].action = self.send_motor_values
		self.view_dict['dashboard.pyui']['slider_motor_2'].action = self.send_motor_values
		self.view_dict['dashboard.pyui']['slider_motor_3'].action = self.send_motor_values
		self.view_dict['dashboard.pyui']['slider_motor_4'].action = self.send_motor_values
		# fly mosquito view actions
		self.view_dict['fly_mosquito.pyui']['btn_arm'].action = self.fly_arm_mosquito
		self.view_dict['fly_mosquito.pyui']['btn_disarm'].action = self.disarm_mosquito
		self.view_dict['fly_mosquito.pyui']['btn_dashboard'].action = self._switch_to_dashboard
		
		# Show the dashboard view
		self.view_dict['dashboard.pyui'].hidden = False
		self.present('fullscreen', orientations=['portrait', 'landscape'])
		
		# store connection data and try to connect to the mosquito
		self._address = address
		self._port = port
		self._timeout = timeout
		self._sock = socket()
		self._sock.settimeout(self._timeout)
		try:
			self._sock.connect((self._address, self._port))
		except:
			console.alert('Could not connect to the Mosquito')	
			
		# state attributes
		self._disarm_clicked = False
		self.view_dict['fly_mosquito.pyui']['aux_1_switch'].value = False
		
	def switch_view(self, view):
		"""
		Make the requested view visible and hide all the rest
		"""
		for key in self.view_dict.keys():
			self.view_dict[key].hidden = True
			if key == view:
				self.view_dict[key].hidden = False
	

	# Action methods
	def _switch_to_fly(self, sender):
		"""
		Show fly view
		"""
		self.switch_view('fly_mosquito.pyui')

	def _switch_to_dashboard(self, sender):
		"""
		Show dashboard view
		"""
		# As a safety measure, disarm Mosquito when going back
		self._disarm_clicked = True
		self.disarm_mosquito(sender)
		self.switch_view('dashboard.pyui')

	def arm_mosquito(self, sender):
		"""
		Arm the Mosquito via Wifi
		"""
		data = msppg.serialize_SET_ARMED(1)
		try:
			self._sock.send(data)
		except:
			pass

	@ui.in_background
	def fly_arm_mosquito(self, sender):
		"""
		Arm the Mosquito via Wifi and loop sending RC commands
		until disarmed
		"""
		data = msppg.serialize_SET_ARMED(1)
		try:
			self._sock.send(data)
		except:
			pass	
		self._disarm_clicked = False
		# until disarmed send joystick data to the mosquito
		while not self._disarm_clicked:
			aux_1 = 0.0
			if sender.superview['aux_1_switch'].value:
				aux_1 = 1.0
			yaw, throttle = sender.superview['left_stick'].get_rc_values()
			roll, pitch = sender.superview['right_stick'].get_rc_values()
			data = msppg.serialize_SET_RC_NORMAL(throttle, roll, pitch, yaw, aux_1, 1.0)
			self._sock.send(data)
		
	def disarm_mosquito(self, sender):
		"""
		Diasrm Mosquito via Wifi
		"""
		data = msppg.serialize_SET_ARMED(0)
		try:
			self._sock.send(data)
		except:
			pass
		if sender.superview.name == 'Fly':
			self._disarm_clicked = True
			
	def send_motor_values(self, sender):
		"""
		Set motor values via Wifi
		"""
		parent_view = sender.superview
		m_1 = parent_view['slider_motor_1'].value
		m_2 = parent_view['slider_motor_2'].value
		m_3 = parent_view['slider_motor_3'].value
		m_4 = parent_view['slider_motor_4'].value
		data = msppg.serialize_SET_MOTOR_NORMAL(m_1, m_2,m_3,m_4)
		self._sock.send(data)

def main():
	Mosquito()
	
if __name__ == '__main__':
	main()
