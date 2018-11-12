import ui

class joystick(ui.View):

	def __init__(self, stick_size, size, is_throttle_stick=False):
		self.is_throttle_stick = is_throttle_stick
		self.width = size
		self.height = size
		self.background_color = 'grey'
		self.corner_radius = self.width/2
		self.border_width = 1
		stick = ui.View()
		self.add_subview(stick)
		stick.width, stick.height = stick_size, stick_size
		stick.x, stick.y = self.width/2 - stick.width/2, self.height/2 - stick.height/2
		if self.is_throttle_stick:
			stick.y = self.height - stick.height
		stick.background_color = 'blue'
		stick.corner_radius = stick_size/2
		stick.name = 'stick'
		
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
			
		
#stick = joystick(20, 50)

#stick.present('sheet')
#stick.touch_ended(None)  # center the stick

