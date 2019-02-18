import threading

class FirstThread(threading.Thread):
	def init(self):
		threading.Thread.__init__(self)

	def run(self):
		go_ser()


class SecondThread(threading.Thread):
	def init(self):
		threading.Thread.__init__(self)

	def run(self):
		cflag()