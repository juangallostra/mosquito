#import ui
import fly_mosquito
import msppg


def arm_mosquito(sender):
	'''
	Arm the Mosquito via Wifi
	'''
	data = msppg.serialize_SET_ARMED(1)
	sender.superview._sock.send(data)
	
def disarm_mosquito(sender):
	'''
	Diasrm Mosquito via Wifi
	'''
	data = msppg.serialize_SET_ARMED(0)
	sender.superview._sock.send(data)
	
def send_motor_values(sender):
	'''
	Set motor values via Wifi
	'''
	v = sender.superview
	m_1 = v['slider_motor_1'].value
	m_2 = v['slider_motor_2'].value
	m_3 = v['slider_motor_3'].value
	m_4 = v['slider_motor_4'].value
	data = msppg.serialize_SET_MOTOR_NORMAL(m_1, m_2,m_3,m_4)
	sender.superview._sock.send(data)

def fly_clicked(sender):
		return sender.superview.update_view('fly_mosquito.pyui', ['landscape'])
	
	
	
#v = ui.load_view()
#v.present('fullscreen', orientations=['portrait'])

#try:
#    console.alert('Connecting...')
#    sock = socket()
#    sock.settimeout(TIMEOUT)
#    sock.connect((ADDR, PORT))
#except:
#    console.alert('Could not connect to the Mosquito')

