import asyncio
import time
import pymem
import threading
import struct
from flask_socketio import SocketIO
import ctypes

class ScoreScanner:
	def __init__(self, socketio: SocketIO):
		self.socketio = socketio
		self.exe_name = "Sinmai.exe"
		self.dll_name = "UnityPlayer.dll"
		self.base_offset = 0x014AD9C0
		self.offset_levels = [0x2B8, 0x40, 0x168, 0x58, 0x10, 0x20, 0x20]
		self.achv_base_offset = 0x01503948
		self.achv_offset_levels = [0x18, 0x290, 0x3A0, 0x468, 0x260, 0x28, 0x6E0]
		self.actual_data = []
		self.running = False
		self.value = '-----'
		self.max_notes = 0
		self.prev_value = -1
		self.addr = None
		self.achv_addr = None
		self.valid = False
		self.addrcap = ctypes.WinDLL("./address_capture.dll")
		self.addrcap.capture_address.argtypes = [
			ctypes.wintypes.HANDLE,
			ctypes.c_uint64,
			ctypes.POINTER(ctypes.c_uint64),
			ctypes.c_int
		]
		self.addrcap.capture_address.restype = ctypes.c_uint64

	def start(self):
		if self.running:
			return
		self.running = True

		def update_score():
			self.valid = False
			while self.running:
				try:
					# Init
					if not self.valid:
						self.addr = None
						pm = pymem.Pymem(self.exe_name)
						module = pymem.process.module_from_name(pm.process_handle, self.dll_name).lpBaseOfDll
						# Convert offsets into C array
						offsets_array = (ctypes.c_uint64 * len(self.offset_levels))(*self.offset_levels)
						# Call into C
						while self.addr is None:
							try:
								self.addr = self.addrcap.capture_address(pm.process_handle, module + self.base_offset, offsets_array,
															   len(self.offset_levels))
							except:
								pass
						validation_array = [
							pm.read_int(self.addr + i) for i in range(4, 304, 4)
						]
						# Address is correct only if all these values are w/i acceptable values
						# spoiler: This is judgment table lol
						if (not (any(x >= 2000 for x in validation_array) or any(x < 0 for x in validation_array))
								and self.addr % 16 == 0):
							self.valid = True
						else:
							self.valid = False
					else:
						pm = pymem.Pymem(self.exe_name)
						self.value = pm.read_int(self.addr)
						self.actual_data = [
								pm.read_int(self.addr + i) for i in range(4, 304, 4)
						]
						achv = str(pm.read_int(self.achv_addr) / 10000.0) + '%'
						if self.actual_data == [0] * 75:
							self.max_notes = self.value
						if self.value <= 0 or self.value > 10000:
							self.value = '------'
							self.valid = False
				except Exception as e:
					self.value = '------'
					self.valid = False
				self.socketio.emit('score_scanner', {'data': self.actual_data,
													 'max_notes': self.max_notes})
				time.sleep(1/120)
		threading.Thread(target=update_score, daemon=True).start()


	# def get_score():
	# 	addresses = []
	# 	for i in range(5):
	# 		addresses.append(read_multilevel_pointers(exe_name, dll_name, base_offset[i],
	# 												  offset_levels[i]))
	# 	try:
	# 		if (addresses[0][0] == addresses[1][0] == addresses[2][0] == addresses[3][0]
	# 				== addresses[4][0]):
	# 			return str(addresses[0][1])
	# 		else:
	# 			return '------'
	# 	except Exception as e:
	# 		return '------'

	# # For test
	# addresses = []
	# for i in range(5):
	# 	addresses.append(read_multilevel_pointers(exe_name, dll_name, base_offset[i],
	# 											  offset_levels[i]))
	# if (addresses[0][0] == addresses[1][0] == addresses[2][0] == addresses[3][0]
	# 		== addresses[4][0]):
	# 	print(addresses[0][1])
	# else:
	# 	print('------')