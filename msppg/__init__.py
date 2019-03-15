'''
__init__.py Python implementation of MSPPG parser

Auto-generated code: DO NOT EDIT!

Copyright (C) Rob Jones, Alec Singer, Chris Lavin, Blake Liebling, Simon D. Levy 2015

This program is part of Hackflight

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http:#www.gnu.org/licenses/>.
'''

import struct
import sys

def _CRC8(data):

    crc = 0x00
   
    for c in data:

        crc ^= ord(c) if sys.version[0] == '2' else c

    return crc

class MSP_Parser(object):

    def __init__(self):

        self.state = 0

    def parse(self, char):
        '''
        Parses one character, triggering pre-set handlers upon a successful parse.
        '''

        byte = ord(char)

        if self.state ==  0: # sync char 1
            if byte == 36: # $
                self.state += 1

        elif self.state ==  1: # sync char 2
            if byte == 77: # M
                self.state += 1
            else: # restart and try again
                self.state = 0

        elif self.state ==  2: # direction
            if byte == 62:  # >
                self.message_direction = 1
            else: # <
                self.message_direction = 0
            self.state += 1
            
        elif self.state ==  3:
            self.message_length_expected = byte
            self.message_checksum = byte
            # setup arraybuffer
            self.message_buffer = b''
            self.state += 1

        elif self.state ==  4:
            self.message_id = byte
            self.message_length_received  = 0
            self.message_checksum ^= byte
            if self.message_length_expected > 0:
                # process payload
                self.state += 1
            else:
                # no payload
                self.state += 2

        elif self.state ==  5: # payload
            self.message_buffer += char
            self.message_checksum ^= byte
            self.message_length_received += 1
            if self.message_length_received >= self.message_length_expected:
                self.state += 1

        elif self.state ==  6:
            if self.message_checksum == byte:
                # message received, process

                if self.message_id == 102:

                    if self.message_direction == 0:

                        if hasattr(self, 'RAW_IMU_Request_Handler'):

                            self.RAW_IMU_Request_Handler()

                    else:

                        if hasattr(self, 'RAW_IMU_Handler'):

                            self.RAW_IMU_Handler(*struct.unpack('=hhhhhhhhh', self.message_buffer))

                if self.message_id == 121:

                    if self.message_direction == 0:

                        if hasattr(self, 'RC_NORMAL_Request_Handler'):

                            self.RC_NORMAL_Request_Handler()

                    else:

                        if hasattr(self, 'RC_NORMAL_Handler'):

                            self.RC_NORMAL_Handler(*struct.unpack('=ffffff', self.message_buffer))

                if self.message_id == 122:

                    if self.message_direction == 0:

                        if hasattr(self, 'ATTITUDE_RADIANS_Request_Handler'):

                            self.ATTITUDE_RADIANS_Request_Handler()

                    else:

                        if hasattr(self, 'ATTITUDE_RADIANS_Handler'):

                            self.ATTITUDE_RADIANS_Handler(*struct.unpack('=fff', self.message_buffer))

                if self.message_id == 123:

                    if self.message_direction == 0:

                        if hasattr(self, 'ALTITUDE_METERS_Request_Handler'):

                            self.ALTITUDE_METERS_Request_Handler()

                    else:

                        if hasattr(self, 'ALTITUDE_METERS_Handler'):

                            self.ALTITUDE_METERS_Handler(*struct.unpack('=ff', self.message_buffer))

                if self.message_id == 126:

                    if self.message_direction == 0:

                        if hasattr(self, 'LOITER_Request_Handler'):

                            self.LOITER_Request_Handler()

                    else:

                        if hasattr(self, 'LOITER_Handler'):

                            self.LOITER_Handler(*struct.unpack('=fff', self.message_buffer))

                if self.message_id == 199:

                    if self.message_direction == 0:

                        if hasattr(self, 'FAKE_INT_Request_Handler'):

                            self.FAKE_INT_Request_Handler()

                    else:

                        if hasattr(self, 'FAKE_INT_Handler'):

                            self.FAKE_INT_Handler(*struct.unpack('=ii', self.message_buffer))

                if self.message_id == 124:

                    if self.message_direction == 0:

                        if hasattr(self, 'GET_MOTOR_NORMAL_Request_Handler'):

                            self.GET_MOTOR_NORMAL_Request_Handler()

                    else:

                        if hasattr(self, 'GET_MOTOR_NORMAL_Handler'):

                            self.GET_MOTOR_NORMAL_Handler(*struct.unpack('=ffff', self.message_buffer))

                if self.message_id == 1:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_ARM_Request_Handler'):

                            self.WP_ARM_Request_Handler()

                    else:

                        if hasattr(self, 'WP_ARM_Handler'):

                            self.WP_ARM_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 2:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_DISARM_Request_Handler'):

                            self.WP_DISARM_Request_Handler()

                    else:

                        if hasattr(self, 'WP_DISARM_Handler'):

                            self.WP_DISARM_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 3:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_LAND_Request_Handler'):

                            self.WP_LAND_Request_Handler()

                    else:

                        if hasattr(self, 'WP_LAND_Handler'):

                            self.WP_LAND_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 4:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_TAKE_OFF_Request_Handler'):

                            self.WP_TAKE_OFF_Request_Handler()

                    else:

                        if hasattr(self, 'WP_TAKE_OFF_Handler'):

                            self.WP_TAKE_OFF_Handler(*struct.unpack('=BB', self.message_buffer))

                if self.message_id == 5:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_GO_FORWARD_Request_Handler'):

                            self.WP_GO_FORWARD_Request_Handler()

                    else:

                        if hasattr(self, 'WP_GO_FORWARD_Handler'):

                            self.WP_GO_FORWARD_Handler(*struct.unpack('=BB', self.message_buffer))

                if self.message_id == 6:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_GO_BACKWARD_Request_Handler'):

                            self.WP_GO_BACKWARD_Request_Handler()

                    else:

                        if hasattr(self, 'WP_GO_BACKWARD_Handler'):

                            self.WP_GO_BACKWARD_Handler(*struct.unpack('=BB', self.message_buffer))

                if self.message_id == 7:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_GO_LEFT_Request_Handler'):

                            self.WP_GO_LEFT_Request_Handler()

                    else:

                        if hasattr(self, 'WP_GO_LEFT_Handler'):

                            self.WP_GO_LEFT_Handler(*struct.unpack('=BB', self.message_buffer))

                if self.message_id == 8:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_GO_RIGHT_Request_Handler'):

                            self.WP_GO_RIGHT_Request_Handler()

                    else:

                        if hasattr(self, 'WP_GO_RIGHT_Handler'):

                            self.WP_GO_RIGHT_Handler(*struct.unpack('=BB', self.message_buffer))

                if self.message_id == 9:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_CHANGE_ALTITUDE_Request_Handler'):

                            self.WP_CHANGE_ALTITUDE_Request_Handler()

                    else:

                        if hasattr(self, 'WP_CHANGE_ALTITUDE_Handler'):

                            self.WP_CHANGE_ALTITUDE_Handler(*struct.unpack('=BB', self.message_buffer))

                if self.message_id == 10:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_CHANGE_SPEED_Request_Handler'):

                            self.WP_CHANGE_SPEED_Request_Handler()

                    else:

                        if hasattr(self, 'WP_CHANGE_SPEED_Handler'):

                            self.WP_CHANGE_SPEED_Handler(*struct.unpack('=BB', self.message_buffer))

                if self.message_id == 11:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_HOVER_Request_Handler'):

                            self.WP_HOVER_Request_Handler()

                    else:

                        if hasattr(self, 'WP_HOVER_Handler'):

                            self.WP_HOVER_Handler(*struct.unpack('=BB', self.message_buffer))

                if self.message_id == 12:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_TURN_CW_Request_Handler'):

                            self.WP_TURN_CW_Request_Handler()

                    else:

                        if hasattr(self, 'WP_TURN_CW_Handler'):

                            self.WP_TURN_CW_Handler(*struct.unpack('=BB', self.message_buffer))

                if self.message_id == 13:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_TURN_CCW_Request_Handler'):

                            self.WP_TURN_CCW_Request_Handler()

                    else:

                        if hasattr(self, 'WP_TURN_CCW_Handler'):

                            self.WP_TURN_CCW_Handler(*struct.unpack('=BB', self.message_buffer))

                if self.message_id == 23:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_MISSION_FLAG_Request_Handler'):

                            self.WP_MISSION_FLAG_Request_Handler()

                    else:

                        if hasattr(self, 'WP_MISSION_FLAG_Handler'):

                            self.WP_MISSION_FLAG_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 24:

                    if self.message_direction == 0:

                        if hasattr(self, 'ESC_CALIBRATION_Request_Handler'):

                            self.ESC_CALIBRATION_Request_Handler()

                    else:

                        if hasattr(self, 'ESC_CALIBRATION_Handler'):

                            self.ESC_CALIBRATION_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 25:

                    if self.message_direction == 0:

                        if hasattr(self, 'MOSQUITO_VERSION_Request_Handler'):

                            self.MOSQUITO_VERSION_Request_Handler()

                    else:

                        if hasattr(self, 'MOSQUITO_VERSION_Handler'):

                            self.MOSQUITO_VERSION_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 26:

                    if self.message_direction == 0:

                        if hasattr(self, 'POSITION_BOARD_Request_Handler'):

                            self.POSITION_BOARD_Request_Handler()

                    else:

                        if hasattr(self, 'POSITION_BOARD_Handler'):

                            self.POSITION_BOARD_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 27:

                    if self.message_direction == 0:

                        if hasattr(self, 'POSITION_BOARD_CONNECTED_Request_Handler'):

                            self.POSITION_BOARD_CONNECTED_Request_Handler()

                    else:

                        if hasattr(self, 'POSITION_BOARD_CONNECTED_Handler'):

                            self.POSITION_BOARD_CONNECTED_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 30:

                    if self.message_direction == 0:

                        if hasattr(self, 'WP_MISSION_BEGIN_Request_Handler'):

                            self.WP_MISSION_BEGIN_Request_Handler()

                    else:

                        if hasattr(self, 'WP_MISSION_BEGIN_Handler'):

                            self.WP_MISSION_BEGIN_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 50:

                    if self.message_direction == 0:

                        if hasattr(self, 'FIRMWARE_VERSION_Request_Handler'):

                            self.FIRMWARE_VERSION_Request_Handler()

                    else:

                        if hasattr(self, 'FIRMWARE_VERSION_Handler'):

                            self.FIRMWARE_VERSION_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 127:

                    if self.message_direction == 0:

                        if hasattr(self, 'GET_PID_CONSTANTS_Request_Handler'):

                            self.GET_PID_CONSTANTS_Request_Handler()

                    else:

                        if hasattr(self, 'GET_PID_CONSTANTS_Handler'):

                            self.GET_PID_CONSTANTS_Handler(*struct.unpack('=fffffffffffffffffff', self.message_buffer))

                if self.message_id == 119:

                    if self.message_direction == 0:

                        if hasattr(self, 'RC_CALIBRATION_STATUS_Request_Handler'):

                            self.RC_CALIBRATION_STATUS_Request_Handler()

                    else:

                        if hasattr(self, 'RC_CALIBRATION_STATUS_Handler'):

                            self.RC_CALIBRATION_STATUS_Handler(*struct.unpack('=B', self.message_buffer))

                if self.message_id == 125:

                    if self.message_direction == 0:

                        if hasattr(self, 'GET_BATTERY_VOLTAGE_Request_Handler'):

                            self.GET_BATTERY_VOLTAGE_Request_Handler()

                    else:

                        if hasattr(self, 'GET_BATTERY_VOLTAGE_Handler'):

                            self.GET_BATTERY_VOLTAGE_Handler(*struct.unpack('=f', self.message_buffer))

                if self.message_id == 116:

                    if self.message_direction == 0:

                        if hasattr(self, 'GET_MISSION_COMPLETE_Request_Handler'):

                            self.GET_MISSION_COMPLETE_Request_Handler()

                    else:

                        if hasattr(self, 'GET_MISSION_COMPLETE_Handler'):

                            self.GET_MISSION_COMPLETE_Handler(*struct.unpack('=B', self.message_buffer))

            else:
                print('code: ' + str(self.message_id) + ' - crc failed')
            # Reset variables
            self.message_length_received = 0
            self.state = 0

        else:
            print('Unknown state detected: %d' % self.state)



    def set_RAW_IMU_Handler(self, handler):

        '''
        Sets the handler method for when a RAW_IMU message is successfully parsed.
        You should declare this message with the following parameter(s):
            accx,accy,accz,gyrx,gyry,gyrz,magx,magy,magz
        '''
        self.RAW_IMU_Handler = handler

    def set_RC_NORMAL_Handler(self, handler):

        '''
        Sets the handler method for when a RC_NORMAL message is successfully parsed.
        You should declare this message with the following parameter(s):
            c1,c2,c3,c4,c5,c6
        '''
        self.RC_NORMAL_Handler = handler

    def set_ATTITUDE_RADIANS_Handler(self, handler):

        '''
        Sets the handler method for when a ATTITUDE_RADIANS message is successfully parsed.
        You should declare this message with the following parameter(s):
            roll,pitch,yaw
        '''
        self.ATTITUDE_RADIANS_Handler = handler

    def set_ALTITUDE_METERS_Handler(self, handler):

        '''
        Sets the handler method for when a ALTITUDE_METERS message is successfully parsed.
        You should declare this message with the following parameter(s):
            estalt,vario
        '''
        self.ALTITUDE_METERS_Handler = handler

    def set_LOITER_Handler(self, handler):

        '''
        Sets the handler method for when a LOITER message is successfully parsed.
        You should declare this message with the following parameter(s):
            agl,flowx,flowy
        '''
        self.LOITER_Handler = handler

    def set_FAKE_INT_Handler(self, handler):

        '''
        Sets the handler method for when a FAKE_INT message is successfully parsed.
        You should declare this message with the following parameter(s):
            value1,value2
        '''
        self.FAKE_INT_Handler = handler

    def set_GET_MOTOR_NORMAL_Handler(self, handler):

        '''
        Sets the handler method for when a GET_MOTOR_NORMAL message is successfully parsed.
        You should declare this message with the following parameter(s):
            m1,m2,m3,m4
        '''
        self.GET_MOTOR_NORMAL_Handler = handler

    def set_WP_ARM_Handler(self, handler):

        '''
        Sets the handler method for when a WP_ARM message is successfully parsed.
        You should declare this message with the following parameter(s):
            code
        '''
        self.WP_ARM_Handler = handler

    def set_WP_DISARM_Handler(self, handler):

        '''
        Sets the handler method for when a WP_DISARM message is successfully parsed.
        You should declare this message with the following parameter(s):
            code
        '''
        self.WP_DISARM_Handler = handler

    def set_WP_LAND_Handler(self, handler):

        '''
        Sets the handler method for when a WP_LAND message is successfully parsed.
        You should declare this message with the following parameter(s):
            code
        '''
        self.WP_LAND_Handler = handler

    def set_WP_TAKE_OFF_Handler(self, handler):

        '''
        Sets the handler method for when a WP_TAKE_OFF message is successfully parsed.
        You should declare this message with the following parameter(s):
            meters,code
        '''
        self.WP_TAKE_OFF_Handler = handler

    def set_WP_GO_FORWARD_Handler(self, handler):

        '''
        Sets the handler method for when a WP_GO_FORWARD message is successfully parsed.
        You should declare this message with the following parameter(s):
            meters,code
        '''
        self.WP_GO_FORWARD_Handler = handler

    def set_WP_GO_BACKWARD_Handler(self, handler):

        '''
        Sets the handler method for when a WP_GO_BACKWARD message is successfully parsed.
        You should declare this message with the following parameter(s):
            meters,code
        '''
        self.WP_GO_BACKWARD_Handler = handler

    def set_WP_GO_LEFT_Handler(self, handler):

        '''
        Sets the handler method for when a WP_GO_LEFT message is successfully parsed.
        You should declare this message with the following parameter(s):
            meters,code
        '''
        self.WP_GO_LEFT_Handler = handler

    def set_WP_GO_RIGHT_Handler(self, handler):

        '''
        Sets the handler method for when a WP_GO_RIGHT message is successfully parsed.
        You should declare this message with the following parameter(s):
            meters,code
        '''
        self.WP_GO_RIGHT_Handler = handler

    def set_WP_CHANGE_ALTITUDE_Handler(self, handler):

        '''
        Sets the handler method for when a WP_CHANGE_ALTITUDE message is successfully parsed.
        You should declare this message with the following parameter(s):
            meters,code
        '''
        self.WP_CHANGE_ALTITUDE_Handler = handler

    def set_WP_CHANGE_SPEED_Handler(self, handler):

        '''
        Sets the handler method for when a WP_CHANGE_SPEED message is successfully parsed.
        You should declare this message with the following parameter(s):
            speed,code
        '''
        self.WP_CHANGE_SPEED_Handler = handler

    def set_WP_HOVER_Handler(self, handler):

        '''
        Sets the handler method for when a WP_HOVER message is successfully parsed.
        You should declare this message with the following parameter(s):
            seconds,code
        '''
        self.WP_HOVER_Handler = handler

    def set_WP_TURN_CW_Handler(self, handler):

        '''
        Sets the handler method for when a WP_TURN_CW message is successfully parsed.
        You should declare this message with the following parameter(s):
            degrees,code
        '''
        self.WP_TURN_CW_Handler = handler

    def set_WP_TURN_CCW_Handler(self, handler):

        '''
        Sets the handler method for when a WP_TURN_CCW message is successfully parsed.
        You should declare this message with the following parameter(s):
            degrees,code
        '''
        self.WP_TURN_CCW_Handler = handler

    def set_WP_MISSION_FLAG_Handler(self, handler):

        '''
        Sets the handler method for when a WP_MISSION_FLAG message is successfully parsed.
        You should declare this message with the following parameter(s):
            flag
        '''
        self.WP_MISSION_FLAG_Handler = handler

    def set_ESC_CALIBRATION_Handler(self, handler):

        '''
        Sets the handler method for when a ESC_CALIBRATION message is successfully parsed.
        You should declare this message with the following parameter(s):
            protocol
        '''
        self.ESC_CALIBRATION_Handler = handler

    def set_MOSQUITO_VERSION_Handler(self, handler):

        '''
        Sets the handler method for when a MOSQUITO_VERSION message is successfully parsed.
        You should declare this message with the following parameter(s):
            mosquitoVersion
        '''
        self.MOSQUITO_VERSION_Handler = handler

    def set_POSITION_BOARD_Handler(self, handler):

        '''
        Sets the handler method for when a POSITION_BOARD message is successfully parsed.
        You should declare this message with the following parameter(s):
            hasPositionBoard
        '''
        self.POSITION_BOARD_Handler = handler

    def set_POSITION_BOARD_CONNECTED_Handler(self, handler):

        '''
        Sets the handler method for when a POSITION_BOARD_CONNECTED message is successfully parsed.
        You should declare this message with the following parameter(s):
            positionBoardConnected
        '''
        self.POSITION_BOARD_CONNECTED_Handler = handler

    def set_WP_MISSION_BEGIN_Handler(self, handler):

        '''
        Sets the handler method for when a WP_MISSION_BEGIN message is successfully parsed.
        You should declare this message with the following parameter(s):
            flag
        '''
        self.WP_MISSION_BEGIN_Handler = handler

    def set_FIRMWARE_VERSION_Handler(self, handler):

        '''
        Sets the handler method for when a FIRMWARE_VERSION message is successfully parsed.
        You should declare this message with the following parameter(s):
            version
        '''
        self.FIRMWARE_VERSION_Handler = handler

    def set_GET_PID_CONSTANTS_Handler(self, handler):

        '''
        Sets the handler method for when a GET_PID_CONSTANTS message is successfully parsed.
        You should declare this message with the following parameter(s):
            gyroRollP,gyroRollI,gyroRollD,gyroPitchP,gyroPitchI,gyroPitchD,gyroYawP,gyroYawI,demandsToRate,levelP,altHoldP,altHoldVelP,altHoldVelI,altHoldVelD,minAltitude,param6,param7,param8,param9
        '''
        self.GET_PID_CONSTANTS_Handler = handler

    def set_RC_CALIBRATION_STATUS_Handler(self, handler):

        '''
        Sets the handler method for when a RC_CALIBRATION_STATUS message is successfully parsed.
        You should declare this message with the following parameter(s):
            status
        '''
        self.RC_CALIBRATION_STATUS_Handler = handler

    def set_GET_BATTERY_VOLTAGE_Handler(self, handler):

        '''
        Sets the handler method for when a GET_BATTERY_VOLTAGE message is successfully parsed.
        You should declare this message with the following parameter(s):
            voltage
        '''
        self.GET_BATTERY_VOLTAGE_Handler = handler

    def set_GET_MISSION_COMPLETE_Handler(self, handler):

        '''
        Sets the handler method for when a GET_MISSION_COMPLETE message is successfully parsed.
        You should declare this message with the following parameter(s):
            status
        '''
        self.GET_MISSION_COMPLETE_Handler = handler

def serialize_RAW_IMU(accx, accy, accz, gyrx, gyry, gyrz, magx, magy, magz):
    '''
    Serializes the contents of a message of type RAW_IMU.
    '''
    message_buffer = struct.pack('hhhhhhhhh', accx, accy, accz, gyrx, gyry, gyrz, magx, magy, magz)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(102) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 102] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_RAW_IMU_Request():

    '''
    Serializes a request for RAW_IMU data.
    '''
    msg = '$M<' + chr(0) + chr(102) + chr(102)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_RC_NORMAL(c1, c2, c3, c4, c5, c6):
    '''
    Serializes the contents of a message of type RC_NORMAL.
    '''
    message_buffer = struct.pack('ffffff', c1, c2, c3, c4, c5, c6)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(121) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 121] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_RC_NORMAL_Request():

    '''
    Serializes a request for RC_NORMAL data.
    '''
    msg = '$M<' + chr(0) + chr(121) + chr(121)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_SET_RC_NORMAL(c1, c2, c3, c4, c5, c6):
    '''
    Serializes the contents of a message of type SET_RC_NORMAL.
    '''
    message_buffer = struct.pack('ffffff', c1, c2, c3, c4, c5, c6)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(222) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 222] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_LOST_SIGNAL(flag):
    '''
    Serializes the contents of a message of type LOST_SIGNAL.
    '''
    message_buffer = struct.pack('B', flag)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(226) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 226] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_ATTITUDE_RADIANS(roll, pitch, yaw):
    '''
    Serializes the contents of a message of type ATTITUDE_RADIANS.
    '''
    message_buffer = struct.pack('fff', roll, pitch, yaw)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(122) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 122] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_ATTITUDE_RADIANS_Request():

    '''
    Serializes a request for ATTITUDE_RADIANS data.
    '''
    msg = '$M<' + chr(0) + chr(122) + chr(122)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_ALTITUDE_METERS(estalt, vario):
    '''
    Serializes the contents of a message of type ALTITUDE_METERS.
    '''
    message_buffer = struct.pack('ff', estalt, vario)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(123) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 123] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_ALTITUDE_METERS_Request():

    '''
    Serializes a request for ALTITUDE_METERS data.
    '''
    msg = '$M<' + chr(0) + chr(123) + chr(123)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_LOITER(agl, flowx, flowy):
    '''
    Serializes the contents of a message of type LOITER.
    '''
    message_buffer = struct.pack('fff', agl, flowx, flowy)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(126) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 126] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_LOITER_Request():

    '''
    Serializes a request for LOITER data.
    '''
    msg = '$M<' + chr(0) + chr(126) + chr(126)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_SET_ARMED(flag):
    '''
    Serializes the contents of a message of type SET_ARMED.
    '''
    message_buffer = struct.pack('B', flag)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(216) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 216] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_FAKE_INT(value1, value2):
    '''
    Serializes the contents of a message of type FAKE_INT.
    '''
    message_buffer = struct.pack('ii', value1, value2)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(199) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 199] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_FAKE_INT_Request():

    '''
    Serializes a request for FAKE_INT data.
    '''
    msg = '$M<' + chr(0) + chr(199) + chr(199)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_SET_MOTOR_NORMAL(m1, m2, m3, m4):
    '''
    Serializes the contents of a message of type SET_MOTOR_NORMAL.
    '''
    message_buffer = struct.pack('ffff', m1, m2, m3, m4)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(215) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 215] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_GET_MOTOR_NORMAL(m1, m2, m3, m4):
    '''
    Serializes the contents of a message of type GET_MOTOR_NORMAL.
    '''
    message_buffer = struct.pack('ffff', m1, m2, m3, m4)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(124) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 124] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_GET_MOTOR_NORMAL_Request():

    '''
    Serializes a request for GET_MOTOR_NORMAL data.
    '''
    msg = '$M<' + chr(0) + chr(124) + chr(124)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_ARM(code):
    '''
    Serializes the contents of a message of type WP_ARM.
    '''
    message_buffer = struct.pack('B', code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(1) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 1] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_ARM_Request():

    '''
    Serializes a request for WP_ARM data.
    '''
    msg = '$M<' + chr(0) + chr(1) + chr(1)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_DISARM(code):
    '''
    Serializes the contents of a message of type WP_DISARM.
    '''
    message_buffer = struct.pack('B', code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(2) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 2] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_DISARM_Request():

    '''
    Serializes a request for WP_DISARM data.
    '''
    msg = '$M<' + chr(0) + chr(2) + chr(2)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_LAND(code):
    '''
    Serializes the contents of a message of type WP_LAND.
    '''
    message_buffer = struct.pack('B', code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(3) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 3] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_LAND_Request():

    '''
    Serializes a request for WP_LAND data.
    '''
    msg = '$M<' + chr(0) + chr(3) + chr(3)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_TAKE_OFF(meters, code):
    '''
    Serializes the contents of a message of type WP_TAKE_OFF.
    '''
    message_buffer = struct.pack('BB', meters, code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(4) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 4] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_TAKE_OFF_Request():

    '''
    Serializes a request for WP_TAKE_OFF data.
    '''
    msg = '$M<' + chr(0) + chr(4) + chr(4)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_GO_FORWARD(meters, code):
    '''
    Serializes the contents of a message of type WP_GO_FORWARD.
    '''
    message_buffer = struct.pack('BB', meters, code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(5) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 5] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_GO_FORWARD_Request():

    '''
    Serializes a request for WP_GO_FORWARD data.
    '''
    msg = '$M<' + chr(0) + chr(5) + chr(5)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_GO_BACKWARD(meters, code):
    '''
    Serializes the contents of a message of type WP_GO_BACKWARD.
    '''
    message_buffer = struct.pack('BB', meters, code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(6) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 6] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_GO_BACKWARD_Request():

    '''
    Serializes a request for WP_GO_BACKWARD data.
    '''
    msg = '$M<' + chr(0) + chr(6) + chr(6)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_GO_LEFT(meters, code):
    '''
    Serializes the contents of a message of type WP_GO_LEFT.
    '''
    message_buffer = struct.pack('BB', meters, code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(7) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 7] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_GO_LEFT_Request():

    '''
    Serializes a request for WP_GO_LEFT data.
    '''
    msg = '$M<' + chr(0) + chr(7) + chr(7)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_GO_RIGHT(meters, code):
    '''
    Serializes the contents of a message of type WP_GO_RIGHT.
    '''
    message_buffer = struct.pack('BB', meters, code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(8) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 8] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_GO_RIGHT_Request():

    '''
    Serializes a request for WP_GO_RIGHT data.
    '''
    msg = '$M<' + chr(0) + chr(8) + chr(8)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_CHANGE_ALTITUDE(meters, code):
    '''
    Serializes the contents of a message of type WP_CHANGE_ALTITUDE.
    '''
    message_buffer = struct.pack('BB', meters, code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(9) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 9] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_CHANGE_ALTITUDE_Request():

    '''
    Serializes a request for WP_CHANGE_ALTITUDE data.
    '''
    msg = '$M<' + chr(0) + chr(9) + chr(9)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_CHANGE_SPEED(speed, code):
    '''
    Serializes the contents of a message of type WP_CHANGE_SPEED.
    '''
    message_buffer = struct.pack('BB', speed, code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(10) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 10] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_CHANGE_SPEED_Request():

    '''
    Serializes a request for WP_CHANGE_SPEED data.
    '''
    msg = '$M<' + chr(0) + chr(10) + chr(10)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_HOVER(seconds, code):
    '''
    Serializes the contents of a message of type WP_HOVER.
    '''
    message_buffer = struct.pack('BB', seconds, code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(11) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 11] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_HOVER_Request():

    '''
    Serializes a request for WP_HOVER data.
    '''
    msg = '$M<' + chr(0) + chr(11) + chr(11)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_TURN_CW(degrees, code):
    '''
    Serializes the contents of a message of type WP_TURN_CW.
    '''
    message_buffer = struct.pack('BB', degrees, code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(12) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 12] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_TURN_CW_Request():

    '''
    Serializes a request for WP_TURN_CW data.
    '''
    msg = '$M<' + chr(0) + chr(12) + chr(12)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_TURN_CCW(degrees, code):
    '''
    Serializes the contents of a message of type WP_TURN_CCW.
    '''
    message_buffer = struct.pack('BB', degrees, code)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(13) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 13] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_TURN_CCW_Request():

    '''
    Serializes a request for WP_TURN_CCW data.
    '''
    msg = '$M<' + chr(0) + chr(13) + chr(13)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_MISSION_FLAG(flag):
    '''
    Serializes the contents of a message of type WP_MISSION_FLAG.
    '''
    message_buffer = struct.pack('B', flag)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(23) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 23] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_MISSION_FLAG_Request():

    '''
    Serializes a request for WP_MISSION_FLAG data.
    '''
    msg = '$M<' + chr(0) + chr(23) + chr(23)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_ESC_CALIBRATION(protocol):
    '''
    Serializes the contents of a message of type ESC_CALIBRATION.
    '''
    message_buffer = struct.pack('B', protocol)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(24) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 24] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_ESC_CALIBRATION_Request():

    '''
    Serializes a request for ESC_CALIBRATION data.
    '''
    msg = '$M<' + chr(0) + chr(24) + chr(24)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_MOSQUITO_VERSION(mosquitoVersion):
    '''
    Serializes the contents of a message of type MOSQUITO_VERSION.
    '''
    message_buffer = struct.pack('B', mosquitoVersion)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(25) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 25] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_MOSQUITO_VERSION_Request():

    '''
    Serializes a request for MOSQUITO_VERSION data.
    '''
    msg = '$M<' + chr(0) + chr(25) + chr(25)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_POSITION_BOARD(hasPositionBoard):
    '''
    Serializes the contents of a message of type POSITION_BOARD.
    '''
    message_buffer = struct.pack('B', hasPositionBoard)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(26) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 26] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_POSITION_BOARD_Request():

    '''
    Serializes a request for POSITION_BOARD data.
    '''
    msg = '$M<' + chr(0) + chr(26) + chr(26)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_POSITION_BOARD_CONNECTED(positionBoardConnected):
    '''
    Serializes the contents of a message of type POSITION_BOARD_CONNECTED.
    '''
    message_buffer = struct.pack('B', positionBoardConnected)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(27) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 27] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_POSITION_BOARD_CONNECTED_Request():

    '''
    Serializes a request for POSITION_BOARD_CONNECTED data.
    '''
    msg = '$M<' + chr(0) + chr(27) + chr(27)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_WP_MISSION_BEGIN(flag):
    '''
    Serializes the contents of a message of type WP_MISSION_BEGIN.
    '''
    message_buffer = struct.pack('B', flag)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(30) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 30] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_WP_MISSION_BEGIN_Request():

    '''
    Serializes a request for WP_MISSION_BEGIN data.
    '''
    msg = '$M<' + chr(0) + chr(30) + chr(30)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_FIRMWARE_VERSION(version):
    '''
    Serializes the contents of a message of type FIRMWARE_VERSION.
    '''
    message_buffer = struct.pack('B', version)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(50) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 50] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_FIRMWARE_VERSION_Request():

    '''
    Serializes a request for FIRMWARE_VERSION data.
    '''
    msg = '$M<' + chr(0) + chr(50) + chr(50)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_SET_MOSQUITO_VERSION(version):
    '''
    Serializes the contents of a message of type SET_MOSQUITO_VERSION.
    '''
    message_buffer = struct.pack('B', version)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(223) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 223] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_SET_PID_CONSTANTS(gyroRollP, gyroRollI, gyroRollD, gyroPitchP, gyroPitchI, gyroPitchD, gyroYawP, gyroYawI, demandsToRate, levelP, altHoldP, altHoldVelP, altHoldVelI, altHoldVelD, minAltitude, param6, param7, param8, param9):
    '''
    Serializes the contents of a message of type SET_PID_CONSTANTS.
    '''
    message_buffer = struct.pack('fffffffffffffffffff', gyroRollP, gyroRollI, gyroRollD, gyroPitchP, gyroPitchI, gyroPitchD, gyroYawP, gyroYawI, demandsToRate, levelP, altHoldP, altHoldVelP, altHoldVelI, altHoldVelD, minAltitude, param6, param7, param8, param9)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(224) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 224] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_GET_PID_CONSTANTS(gyroRollP, gyroRollI, gyroRollD, gyroPitchP, gyroPitchI, gyroPitchD, gyroYawP, gyroYawI, demandsToRate, levelP, altHoldP, altHoldVelP, altHoldVelI, altHoldVelD, minAltitude, param6, param7, param8, param9):
    '''
    Serializes the contents of a message of type GET_PID_CONSTANTS.
    '''
    message_buffer = struct.pack('fffffffffffffffffff', gyroRollP, gyroRollI, gyroRollD, gyroPitchP, gyroPitchI, gyroPitchD, gyroYawP, gyroYawI, demandsToRate, levelP, altHoldP, altHoldVelP, altHoldVelI, altHoldVelD, minAltitude, param6, param7, param8, param9)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(127) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 127] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_GET_PID_CONSTANTS_Request():

    '''
    Serializes a request for GET_PID_CONSTANTS data.
    '''
    msg = '$M<' + chr(0) + chr(127) + chr(127)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_SET_POSITIONING_BOARD(hasBoard):
    '''
    Serializes the contents of a message of type SET_POSITIONING_BOARD.
    '''
    message_buffer = struct.pack('B', hasBoard)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(225) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 225] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_SET_LEDS(red, green, blue):
    '''
    Serializes the contents of a message of type SET_LEDS.
    '''
    message_buffer = struct.pack('BBB', red, green, blue)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(227) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 227] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_RC_CALIBRATION(stage):
    '''
    Serializes the contents of a message of type RC_CALIBRATION.
    '''
    message_buffer = struct.pack('B', stage)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(214) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 214] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_RC_CALIBRATION_STATUS(status):
    '''
    Serializes the contents of a message of type RC_CALIBRATION_STATUS.
    '''
    message_buffer = struct.pack('B', status)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(119) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 119] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_RC_CALIBRATION_STATUS_Request():

    '''
    Serializes a request for RC_CALIBRATION_STATUS data.
    '''
    msg = '$M<' + chr(0) + chr(119) + chr(119)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_SET_BATTERY_VOLTAGE(batteryVoltage):
    '''
    Serializes the contents of a message of type SET_BATTERY_VOLTAGE.
    '''
    message_buffer = struct.pack('f', batteryVoltage)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(228) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 228] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_SET_EMERGENCY_STOP(flag):
    '''
    Serializes the contents of a message of type SET_EMERGENCY_STOP.
    '''
    message_buffer = struct.pack('B', flag)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(229) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 229] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_GET_BATTERY_VOLTAGE(voltage):
    '''
    Serializes the contents of a message of type GET_BATTERY_VOLTAGE.
    '''
    message_buffer = struct.pack('f', voltage)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(125) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 125] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_GET_BATTERY_VOLTAGE_Request():

    '''
    Serializes a request for GET_BATTERY_VOLTAGE data.
    '''
    msg = '$M<' + chr(0) + chr(125) + chr(125)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_GET_MISSION_COMPLETE(status):
    '''
    Serializes the contents of a message of type GET_MISSION_COMPLETE.
    '''
    message_buffer = struct.pack('B', status)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(116) + str(message_buffer)
        return '$M>' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 116] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_GET_MISSION_COMPLETE_Request():

    '''
    Serializes a request for GET_MISSION_COMPLETE data.
    '''
    msg = '$M<' + chr(0) + chr(116) + chr(116)
    return bytes(msg) if sys.version[0] == '2' else bytes(msg, 'utf-8')

def serialize_SET_RANGE_PARAMETERS(rx, ry, rz):
    '''
    Serializes the contents of a message of type SET_RANGE_PARAMETERS.
    '''
    message_buffer = struct.pack('fff', rx, ry, rz)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(221) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 221] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

def serialize_CLEAR_EEPROM(section):
    '''
    Serializes the contents of a message of type CLEAR_EEPROM.
    '''
    message_buffer = struct.pack('B', section)

    if sys.version[0] == '2':
        msg = chr(len(message_buffer)) + chr(201) + str(message_buffer)
        return '$M<' + msg + chr(_CRC8(msg))

    else:
        msg = [len(message_buffer), 201] + list(message_buffer)
        return bytes([ord('$'), ord('M'), ord('<')] + msg + [_CRC8(msg)])

