# -*- coding: utf-8 -*-

import ui
import console
from socket import socket
import time

import joystick as js

import msppg

# Mosquito connection values
ADDRESS = '192.168.4.1'
PORT = 80
TIMEOUT = 4
INTERVAL = 0.005


def mosquito_load_view(view):
	"""
	Load a pythonista ui view and its specific 
	components from a ui filename
	"""
	ui_view = ui.load_view(view)
	if view == 'fly_mosquito.pyui':
		stick_throttle_yaw = js.joystick(60, 200,'left_stick', is_throttle_stick=True)
		stick_roll_pitch = js.joystick(60, 200, 'right_stick')
		stick_throttle_yaw.x, stick_throttle_yaw.y = 25, 60
		stick_roll_pitch.x, stick_roll_pitch.y = 340, 60
		stick_throttle_yaw.touch_ended(None)  # center the stick
		stick_roll_pitch.touch_ended(None)
		ui_view.add_subview(stick_throttle_yaw)
		ui_view.add_subview(stick_roll_pitch)
	return ui_view


# Main class for the app that switches beween views
class Mosquito(ui.View):

	def __init__(self, address=ADDRESS, port=PORT, timeout=TIMEOUT, interval=INTERVAL):
		# view handling
		self.view_dict = {'dashboard.pyui':None, 'fly_mosquito.pyui':None}
		
		# load and hide all the views
		for key in self.view_dict.keys():
			# Load view, add it to the main view and hide it
			self.view_dict[key] = mosquito_load_view(key)
			self.add_subview(self.view_dict[key])
			self.view_dict[key].hidden = True
			
		# bind actions to ui elements 
		self._bind_actions()
		
		# Show the dashboard view
		self.view_dict['dashboard.pyui'].hidden = False
		self.present('fullscreen', orientations=['landscape'])
		
		# store connection data and connect
		self._address = address
		self._port = port
		self._timeout = timeout
		self._sock = None
		# send data
		self._interval = interval
			
		# state attributes
		self._disarm_clicked = False
		self.view_dict['fly_mosquito.pyui']['aux_1_switch'].value = False
		self.view_dict['dashboard.pyui']['connected_switch'].enabled = False
		
	def _connect(self, sender=None):
		"""
		Try to connect to the mosquito
		"""
		if self._sock:
			self._sock.close()

		self._sock = socket()
		self._sock.settimeout(self._timeout)
		try:
			self._sock.connect((self._address, self._port))
			if sender.superview.name == 'dashboard':
				self.view_dict['dashboard.pyui']['connected_switch'].value = True
		except:
			resp = console.alert(
				'Could not connect to the Mosquito',
				'',
				'Retry',
				'Cancel',
				hide_cancel_button=True)
			if resp == 1:
				self._connect()

	def _send_data(self, data, sender):
		"""
		Send a serialized MSP mesage
		"""
		try:
			self._sock.send(data)
		except:
			if sender.superview.name == 'dashboard':
				self.view_dict['dashboard.pyui']['connected_switch'].value = False
			console.alert("Connection lost!")

	def _send_multiple_data(self, multiple_data, sender):
		"""
		Send multiple serialized MSP messages
		"""
		try:
			for data in multiple_data:
				self._sock.send(data)
		except:
			if sender.superview.name == 'dashboard':
				self.view_dict['dashboard.pyui']['connected_switch'].value = False
			console.alert("Connection lost!")

	def _switch_view(self, view):
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
		Show fly view and hide the rest of views
		"""
		# As a safety measure, disarm the drone
		self.disarm_mosquito(sender)
		self._switch_view('fly_mosquito.pyui')

	def _switch_to_dashboard(self, sender):
		"""
		Show dashboard view and hide the rest of views
		"""
		# As a safety measure, disarm Mosquito when going back
		self._disarm_clicked = True
		self.disarm_mosquito(sender)
		self._switch_view('dashboard.pyui')

	def arm_mosquito(self, sender):
		"""
		Arm the Mosquito via Wifi by sending appropriate RC commands.
		For Hackflight to consider a safe arming the arming switch has to
		be low on startup. To achieve so, two RC packets are send. In the
		first one, the arming switch is set to low and then the second one
		sets it to high thus arming the drone
		"""
		#data = msppg.serialize_SET_ARMED(1)
		#try:
		#	self._sock.send(data)
		#except:
		#	pass
		data = msppg.serialize_SET_RC_NORMAL(-1.0, 0.0, 0.0, 0.0, 0.0, -1.0)
		data_2 = msppg.serialize_SET_RC_NORMAL(-1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
		self._send_multiple_data([data, data_2], sender)

	@ui.in_background
	def fly_arm_mosquito(self, sender):
		"""
		Arm the Mosquito via Wifi and loop ad infinitum sending RC commands
		until disarmed
		"""
		#data = msppg.serialize_SET_ARMED(1)
		#try:
		#	self._sock.send(data)
		#except:
		#	pass	
		self._disarm_clicked = False
		first_iter = True
		# until disarmed send joystick data to the mosquito
		last = time.time()
		while not self._disarm_clicked:
			aux_2 = 1.0
			if first_iter:
				aux_2 = -1.0
				first_iter = False
			aux_1 = -1.0
			if sender.superview['aux_1_switch'].value:
				aux_1 = 1.0
			yaw, throttle = sender.superview['left_stick'].get_rc_values()
			roll, pitch = sender.superview['right_stick'].get_rc_values()
			data = msppg.serialize_SET_RC_NORMAL(throttle, roll, pitch, yaw, aux_1, aux_2)
			# see if min time has elapsed and, if so, send RC commands
			if time.time() >= (last + self._interval):
				self._send_data(data, sender)
				last = time.time()

		data = msppg.serialize_SET_RC_NORMAL(-1.0, 0.0, 0.0, 0.0, 0.0, -1.0)
		self._send_data(data, sender)
		
	def disarm_mosquito(self, sender):
		"""
		Diasrm Mosquito via Wifi by sending a set of RC values that
		disarm the drone
		"""
		#data = msppg.serialize_SET_ARMED(0)
		#try:
		#	self._sock.send(data)
		#except:
		#	pass
		if sender.superview.name == 'transmitter':
			self._disarm_clicked = True
		else:
			data = msppg.serialize_SET_RC_NORMAL(-1.0, 0.0, 0.0, 0.0, 0.0, -1.0)
			self._send_data(data, sender)
			
	def send_motor_values(self, sender):
		"""
		Send slider motor values via Wifi
		"""
		parent_view = sender.superview
		m_1 = parent_view['slider_motor_1'].value
		m_2 = parent_view['slider_motor_2'].value
		m_3 = parent_view['slider_motor_3'].value
		m_4 = parent_view['slider_motor_4'].value
		data = msppg.serialize_SET_MOTOR_NORMAL(m_1, m_2,m_3,m_4)
		self._send_data(data, sender)

	def _bind_actions(self):
		"""
		Bind action methods to UI elements
		"""
		# dashboard view actions
		self.view_dict['dashboard.pyui']['btn_fly'].action = self._switch_to_fly
		self.view_dict['dashboard.pyui']['btn_arm'].action = self.arm_mosquito
		self.view_dict['dashboard.pyui']['btn_disarm'].action = self.disarm_mosquito
		self.view_dict['dashboard.pyui']['btn_connect'].action = self._connect
		self.view_dict['dashboard.pyui']['slider_motor_1'].action = self.send_motor_values
		self.view_dict['dashboard.pyui']['slider_motor_2'].action = self.send_motor_values
		self.view_dict['dashboard.pyui']['slider_motor_3'].action = self.send_motor_values
		self.view_dict['dashboard.pyui']['slider_motor_4'].action = self.send_motor_values
		# fly mosquito view actions
		self.view_dict['fly_mosquito.pyui']['btn_arm'].action = self.fly_arm_mosquito
		self.view_dict['fly_mosquito.pyui']['btn_disarm'].action = self.disarm_mosquito
		self.view_dict['fly_mosquito.pyui']['btn_dashboard'].action = self._switch_to_dashboard

def main():
	Mosquito()
	
if __name__ == '__main__':
	main()
