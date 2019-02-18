import os
from hashlib import sha256
from time import time, clock
from datetime import datetime
from merkle import merkle_root


WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
MEMORY_POOL = WORKING_DIRECTORY + "/mempool"


class Block:
	def __init__(self, index, data, previous_hash="0"):
		self.nonce = 0
		self.timestamp = int(datetime.now().timestamp())
		self.previous_hash = previous_hash
		self.merkle_tree = None
		self.hash = None
		self.txs = list()
		self.index = index
		self.coinbase = None
		self.data = data
		self.previous_hash = previous_hash
		self.hash = self.hash_block()
		self.json = None

	def get_transactions(self):
		nodes = list()
		filename = MEMORY_POOL
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return nodes
		try:
			with open(filename) as file_handler:
				nodes = file_handler.readlines()[:3]
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong get_transactions!")
		finally:
			if len(nodes) < 3:
				return list()
			else:
				return nodes


	def hash_block(self):
		sha = sha256()
		sha.update((str(self.index) + str(self.timestamp) + str(self.data) +
		str(self.previous_hash)).encode("utf-8"))
		return sha.hexdigest()

	def set__txs(self, value):
		self.txs = value

	def calc_mekrle_tree(self, lst):
		self.merkle_tree = merkle_root(lst)
		return self.merkle_tree

	def calc_hash(self):
		data_block = bytes(str(self.timestamp) + self.previous_hash + str(self.nonce) + str(self.merkle_tree), 'utf-8')
		self.hash = sha256(data_block).hexdigest()

	def set__index(self, value):
		self.index = value

	def get__index(self):
		return self.index

	def get__nonce(self):
		return self.nonce

	def get__txs(self):
		return self.txs

	def get__timestamp(self):
		return self.timestamp

	def get__merkle_tree(self):
		return self.merkle_tree

	def get__hash(self):
		return self.hash

	def get__previous_hash(self):
		return self.previous_hash

	def set__coinbase(self, value):
		self.coinbase = value

	def get_timestamp(self):
		return time() + clock()

	def check_tx_block(self):
		pass

