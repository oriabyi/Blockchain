# super(Serializer, self).__init__() ?
# 0..3 - the number of coins in hex
# 4..38 - the address of the sender
# 39..73 - the address of the recipient
# 74..201 - the public key of the sender hex string format
# 202 .. - Signature
# send 17JsmEygbbEUEpvt4PFtYaTeSqfb9ki1F1 23


class Serializer:
	def __init__(self, transactionGiven):
		self.TX = transactionGiven
		self.sender_public_key = None
		self.serialized = None

	def get_all(self, sender_public_key):
		self.sender_public_key = sender_public_key
		self.serialized = '0' * (4 - len(str(hex(int(self.TX.amount, 10)))[2:])) + str(hex(int(self.TX.amount, 10)))[2:]
		temp = self.TX.sender_address
		while len(temp) < 35:
			temp += "0"
		self.serialized += temp
		temp = self.TX.recipient_address
		while len(temp) < 35:
			temp += "0"
		self.serialized += temp
		self.serialized += self.sender_public_key
		temp = self.TX.get_signed_hash()
		self.serialized += temp
		return self.serialized

	def get__serialized(self):
		return self.serialized

class Deserializer:
	def __init__(self):
		self.amount = 0
		self.sender_address = ""
		self.recipient_address = ""
		self.sender_public_key = ""
		self.signed_hash = ""
		self.concat = ""

	def get_all(self, line):
		self.amount = line[0:4]
		self.sender_address = line[4:39].split('0')[0]
		self.recipient_address = line[39:73].split('0')[0]
		self.sender_public_key = line[74:204]
		self.signed_hash = line[204:]
		self.concat = self.sender_address + self.recipient_address + self.amount
		return self.amount, self.sender_address, self.recipient_address, self.sender_public_key, self.signed_hash
