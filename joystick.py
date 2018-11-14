import ui

class joystick(ui.View):

	def __init__(self, stick_size, size, name, is_throttle_stick=False, rc_x_range=[-1,1] , rc_y_range=[-1,1]):
		self.is_throttle_stick = is_throttle_stick
		self.name = name
		self.width = size
		self.height = size
		self.background_color = 'grey'
		self.corner_radius = self.width/2
		self.border_width = 1
		stick = ui.View()
		stick.name = 'stick'
		self.add_subview(stick)
		stick.width, stick.height = stick_size, stick_size
		stick.x, stick.y = self.width/2 - stick.width/2, self.height/2 - stick.height/2
		if self.is_throttle_stick:
			stick.y = self.height - stick.height
		stick.background_color = 'blue'
		stick.corner_radius = stick_size/2
		stick.name = 'stick'

		# For RC mapping. Stick positions are relative to joystick
		self.mx = (rc_x_range[1] - rc_x_range[0]) / float(self.width-self['stick'].width)
		self.nx = rc_x_range[0] - self.mx * self['stick'].width / 2.0
		# y axis is reversed
		self.my = (rc_y_range[0] - rc_y_range[1]) / float(self.height-self['stick'].height)
		self.ny = rc_y_range[1] - self.my * self['stick'].height / 2.0
	
	def calc_pos(self, touch):
		x_comp = touch.location[0] - touch.prev_location[0]
		x = max(min(self['stick'].x + x_comp, self.width - self['stick'].width), 0)
		
		y_comp = touch.location[1] - touch.prev_location[1]
		y = max(min(self['stick'].y + y_comp, self.height - self['stick'].height), 0)
		return x, y
		
	def touch_moved(self, touch):
		self['stick'].x, self['stick'].y = self.calc_pos(touch)
		
	def touch_ended(self, touch):
		self['stick'].x = self.width/2 - self['stick'].width/2
		if not self.is_throttle_stick:
			self['stick'].y = self.height/2 - self['stick'].height/2

	def get_rc_values(self):
		rc_x = (self['stick'].x + self['stick'].width / 2.0) * self.mx + self.nx
		rc_y = (self['stick'].y + self['stick'].height / 2.0) * self.my + self.ny
		return rc_x, rc_y
