# import logging
# import numpy as np
## Class for magnetic line sensor D-MNSV7-X16
class Magnetic_Line_Sensor:

	def __init__(self, client):

		# Enable logging
		# logging.basicConfig()
		# log = logging.getLogger()
		# log.setLevel(logging.DEBUG)

		self.client = client

		self.client.connect()

		self.ID = 2

		######################
		## Register Address ##
		######################
		## Analog Output/Detection value - 16 channels/16 bytes - 8 values - High byte: EVEN, Low byte: ODD
		self.HIGH_2_LOW_1 = 0x20
		self.HIGH_4_LOW_3 = 0x21
		self.HIGH_6_LOW_5 = 0x22
		self.HIGH_8_LOW_7 = 0x23
		self.HIGH_10_LOW_9 = 0x24
		self.HIGH_12_LOW_11 = 0x25
		self.HIGH_14_LOW_13 = 0x26
		self.HIGH_16_LOW_15 = 0x27

		## Digital Output/Detection value - 16 channels/2 bytes - 1 value
		self.SWITCH_OUTPUT_16_CHANNELS = 0x28

		## RS-232 and RS-485 MODBUS-based device ID (R/W)
		self.ID_ADDRESS = 0x33

	## Some time if read immediatly after write, it would show ModbusIOException when get data from registers
	def modbus_fail_read_handler(self, ADDR, WORD):
		read_success = False
		reg = [None]*WORD
		while not read_success:
			result = self.client.read_holding_registers(ADDR, WORD, unit=self.ID)
			try:
				for i in range(WORD):
					reg[i] = result.registers[i]
				read_success = True
			except AttributeError as e:
				print(e)
				pass

		return reg

	## Basic functions to read line readings
	## Analog output - Array of 16 channel value, 1 byte each
	def get_analog_output(self):
		reg = [None] * 16
		values = self.modbus_fail_read_handler(self.HIGH_2_LOW_1, 8)
		# if result.isError():
		# 	print("No values returned")
		# 	return
		# else:
		# 	print("Values received")
		for i in range(8):
			reg[2*i+1] = (values[i] & 0xFF00) >> 8
			reg[2*i] = values[i] & 0x00FF
		int_values = [int(x) for x in reg]
		return int_values

	## Digital output
	def get_digital_output(self):
		result = self.modbus_fail_read_handler(self.SWITCH_OUTPUT_16_CHANNELS, 1)
		return self.int16Dec_to_int16Hex(result.registers[0])

	def int16Dec_to_int16Hex(self,int16):

		lo_byte = (int16 & 0x00FF)
		hi_byte = (int16 & 0xFF00) >> 8

		all_bytes = (hi_byte << 8) | lo_byte

		return all_bytes

	def set_ID(self, id):
		result = self.client.write_register(self.ID_ADDRESS, id, unit=self.ID)
		if result.isError():
			print("Failed to set ID")
		else:
			print("ID set complete")
			self.ID = id
			value = self.modbus_fail_read_handler(self.ID_ADDRESS, 1)
			print("New ID: " + value)