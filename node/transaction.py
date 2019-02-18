import os
import sys
from hashlib import sha256
sys.path.append(os.path.join(os.path.dirname(__file__), '../wallet_functions'))
from wallet import sign_message


class Transaction:
	def __init__(self):
		self.private_key = None
		self.public_key = None
		self.uncompressed_public_key = None
		self.sender_address = None
		self.recipient_address = None
		self.amount = None
		self.signed_hash = None
		self.hash = None
		self.vk = None
		self.serialize_line = None
		self.concat = None
		self.sign = None

	def hash_calculate(self):
		self.set__hash(sha256(self.concat).hexdigest())
		return self.get__hash()

	def set__amount(self, value):
		self.amount = value

	def set__private_key(self, value):
		self.private_key = value

	def set__public_key(self, value):
		self.public_key = value

	def set__sender_address(self, value):
		self.sender_address = value

	def set__recipient_address(self, value):
		self.recipient_address = value

	def set__hash(self, value):
		self.hash = value

	def set__signed_hash(self, value):
		self.signed_hash = value

	def get__signed_hash(self):
		return self.signed_hash

	def set__vk(self, value):
		self.vk = value

	def set__serialize_line(self, value):
		self.serialize_line = value

	def set__uncompressed_public_key(self, value):
		self.uncompressed_public_key = value

	def set__sign(self, value):
		self.sign = value

	def set_concat(self, sender_address, recipient_address, amount):
		self.concat = sender_address + recipient_address + amount

	def set__concat(self, value):
		self.concat = value

	def get__sign(self):
		return self.sign

	def get__uncompressed_public_key(self):
		return self.uncompressed_public_key

	def get__public_key(self):
		return self.public_key

	def get__serialize_line(self):
		return self.serialize_line

	def get__private_key(self):
		return self.private_key

	def get__sender_address(self):
		return self.sender_address

	def get__recipient_address(self):
		return self.recipient_address

	def get__hash(self):
		return self.hash

	def get__vk(self):
		return self.vk

	def get__concat(self):
		return self.concat

	def calculate_concat(self):
		self.concat = self.sender_address + self.recipient_address + ('0' * (4 - len(str(hex(int(self.amount, 10)))[2:])) + str(hex(int(self.amount, 10)))[2:])
	# def __set__private_key(self, value):
	# 	self.private_key = value

	def calculate_signed_hash(self, private_key):
		self.signed_hash = sign_message(private_key,  bytes(self.hash, "utf-8"))
		return self.signed_hash

	def set_signed_hash(self, hash):
		self.signed_hash = hash

	def get_sender_address(self):
		return self.sender_address

	def get_recipient_address(self):
		return self.recipient_address

	def get_amount(self):
		return self.amount

	def get_concat(self):
		return self.concat

	def get_hash(self):
		return self.hash

	def get_signed_hash(self):
		return self.signed_hash


class CoinbaseTransaction(Transaction):
	def __init__(self):
		Transaction.__init__(self)
