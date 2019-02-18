import hashlib
import os, re, sys, json, requests
from block import Block
from serializer import Serializer
from serializer import Deserializer
from pending_pool import TransactionsPool
from transaction import CoinbaseTransaction
from tx_validator import sign_message as tx_sign_message
sys.path.append(os.path.join(os.path.dirname(__file__), '../wallet_functions'))
import wallet
sys.path.append(os.path.join(os.path.dirname(__file__), '../general'))
from exception_classes import *

WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
ATOI = re.compile(r'[^\d-]*(-?[\d]+(\.[\d]*)?([eE][+-]?[\d]+)?)')

CHAIN = WORKING_DIRECTORY + "/blocks"
MEMORY_POOL = WORKING_DIRECTORY + "/mempool"
MINER_ADDRESS = WORKING_DIRECTORY + "/miner_address"
CONFIGURATION = WORKING_DIRECTORY + "/configuration"

class Blockchain:
	def __init__(self, complexity=2):
		self.mine_mode = False
		self.consensus_mode = False
		self.id_blocks = 1
		self.last_hash = "0" * 64
		self.complexity = complexity
		self.main_blocks = list()
		self.last_block = None
		self.last_block_id = 0
		self.blocks_len = self.get_len_chain()
		self.coinbase_tx = None
		self.mine_mode = False

	def mine(self, block, complexity=2):
		while block.hash[:complexity] != "0" * complexity:
			block.nonce += 1
			block.calculate_hash()
		return block

	def create_block(self, index=0, coinbase=""):
		block = Block(index, 0, self.last_hash)
		# block.txs.append(coinbase)
		# block.txs.append(block.get_transactions())
		block.txs = block.get_transactions()[::]
		# if block.txs == list():
		# 	return False
		block.txs.insert(0, coinbase)
		block.calc_mekrle_tree(block.txs)
		block.calc_hash()
		print("last id = ", block.index)
		while block.hash[:self.complexity] != '0' * self.complexity:
			block.calc_hash()
			block.nonce += 1
		return block

	def create_genesis_block(self):
		block = Block(0, 0, "0" * 64)
		block.txs = block.get_transactions()
		if block.txs is None:
			return False
		block.calc_mekrle_tree(block.txs)
		block.calc_hash()
		self.id_blocks = 0
		return block

	def save_block_to_file(self, block):
		filename = CHAIN
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return
		try:
			with open(filename, "a+") as filehandler:
				filehandler.write(block.json)
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong save_block_to_file!")

	def save_block_to_blockchain(self, block):
		self.main_blocks.append(block)

	def remove_transactions(self):
		filename = MEMORY_POOL
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return
		try:
			with open(filename) as file_handle:
				lines = file_handle.readlines()
			with open(filename, "w") as file_handle:
				lines = lines[3:]
				for x in lines:
					file_handle.write(str(x))
		except PermissionError:
			print("{0:^60}: there are no permissions for opening ".format(filename))
		except:
			print("Something gone wrong remove_transactions!")

	def get_len_chain(self):
		chain_len = 0
		temp_line = ""
		filename = CHAIN
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return
		if self.last_block_id == 0:
			self.get_last_block_id()
		try:
			with open(CHAIN, "r") as file_handle:
				temp_line = file_handle.readline()
				while temp_line:
					if temp_line.find("id") != -1:
						chain_len += 1
					temp_line = file_handle.readline()
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong get_len_chain!")
		finally:
			return chain_len

	def get_last_block_id(self):
		last_block_id = -1
		filename = CHAIN
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return
		try:
			with open(filename, "r") as file_handle:
				temp_line = file_handle.readline()
				while temp_line is not "":
					if temp_line.find("\"id\":") is not -1:
						last_block_id = ATOI.match(temp_line[temp_line.find("\"id\":") + 6:])[0][1:]
					temp_line = file_handle.readline()
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong get_last_block_id!")
		finally:
			self.set__last_block_id(int(last_block_id))

	def get_pending_txs(self):
		pendings_txt = list()
		if os.path.isfile(MEMORY_POOL) is False:
			return list()
		try:
			with open(MEMORY_POOL, "r") as file_handle:
				pendings_txt = file_handle.readlines()
		except PermissionError:
			print("There are no permissions for opening ", filename)
			return list()
		finally:
			return pendings_txt

	def get_pending_txs_length(self):
		counter = 0
		filename = MEMORY_POOL
		if os.path.isfile(filename) is False:
			print("{} does not exist ".format(filename))
			return 0
		try:
			with open(filename, "r") as file_handle:
				while file_handle.readline() is not "":
					counter += 1
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong get_pending_txs_length!")
		finally:
			return counter

	def set__last_block(self, block):
		self.last_block = block

	def set__last_block_id(self, id):
		self.last_block_id = id
		print("id = ", id)

	def get_chain(self):
		filename = CHAIN
		formatted_chain = ""
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return ""
		try:
			with open(filename, 'r') as file_handle:
				chain = file_handle.readlines()
			formatted_chain = ""
			for line in chain:
				formatted_chain += line + '\n'
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong get_chain!")
		finally:
			return formatted_chain

	def get__last_block_id(self):
		self.get_last_block_id()
		return self.last_block_id

	def resolve_conflicts(self):
		pass

	def get_block_by_height(self, height):  # check height in range
		filename = CHAIN
		temp_block = ""
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return
		try:
			with open(filename, "r") as file_handle:
				temp_line = file_handle.readline()
				temp_block = ""
				while temp_line is not "":
					if temp_line.find("\"id\":") is not -1 and \
							int(height) == int(temp_line.split(':')[1].split('\"')[1]):
						temp_block = "{\n" + temp_line
						while temp_line.find("{") is -1 and temp_line is not "":
							temp_line = file_handle.readline()
							temp_block += temp_line
						break
					temp_line = file_handle.readline()
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong get_block_by_height !")
		finally:
			list_ = temp_block.split('\n')
			len_list = len(list_)
			i = 0
			while i < len_list:
				print(i)
				if list_[i] == '{' or list_[i] == '}' or list_[i] == ']':
					list_.remove(list_[i])
					len_list = len(list_)
					i = 0
				else:
					while list_[i] != "" and list_[i][0] == ' ':
						list_[i] = list_[i][1:]
					i += 1
			return list_

	def get_tx_hash(self, hash):  # check height in range
		filename = CHAIN
		temp_block = ""
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return
		try:
			with open(filename, "r") as file_handle:
				temp_line = file_handle.readline()
				temp_block = ""
				while temp_line is not "":
					if temp_line.find("\"hash\":") is not -1 and \
							hash == temp_line.split('\"hash\"')[1][3:-3]:
						while temp_block.count('\"id') > 1:
							temp_block = temp_block[2 + temp_block.find('\"id'):]
						temp_block = temp_block[temp_block.find('\"id'):]
						while temp_line.find("{") is -1 and temp_line is not "":
							temp_block += temp_line
							temp_line = file_handle.readline()
						break
					if temp_line.find("\"prev_hash\":") is not -1 or temp_line.find("\"id\":") is not -1:
						temp_block += temp_line
					temp_line = file_handle.readline()
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong get_block_by_height !")
		finally:
			list_ = temp_block.split('\n')
			len_list = len(list_)
			i = 0
			while i < len_list:
				print(i)
				if list_[i] == '{' or list_[i] == '}' or list_[i] == ']':
					list_.remove(list_[i])
					len_list = len(list_)
					i = 0
				else:
					while list_[i] != "" and list_[i][0] == ' ':
						list_[i] = list_[i][1:]
					i += 1
			return list_

	def get_last_block(self):
		last_block = ""
		filename = CHAIN
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return
		try:
			with open(filename, "r") as file_handle:
				self.get_last_block_id()
				last_block_id = self.get__last_block_id()
				if last_block_id == 0:
					return file_handle.readlines()
				temp_line = file_handle.readline()
				while temp_line is not "":
					if temp_line.find("\"id\":") is not -1 and \
							last_block_id - 1 == int(temp_line.split(':')[1].split('\"')[1]):
						break
					print("temp line = ", temp_line, "| ", len(temp_line))
					temp_line = file_handle.readline()
				while temp_line is not "" and temp_line != "{\n":
					temp_line = file_handle.readline()
				last_block = file_handle.readlines()
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong get_last_block !")
		finally:
			return last_block

	def get_balance_by_address(self, address):
		filename = CHAIN
		balance_address = 0
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return 0
		try:
			with open(filename, "r") as file_handle:
				temp_line = file_handle.readline()
				while temp_line:
					temp_line = file_handle.readline()
					if temp_line.find("transactions") is not -1:
						while temp_line.find("]") is -1:
							temp_line = file_handle.readline()
							serialize_line = temp_line.replace(" ", "").replace("\n", "").replace("\"", "").split('\\')[0]
							amount, sender_address, recipient_address = Deserializer().get_all(serialize_line)[0:3]
							if sender_address == address:
								balance_address -= int(amount, 16)
							elif recipient_address == address:
								balance_address += int(amount, 16)
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong get_balance_by_address !")
		finally:
			return balance_address


	def calculate_coinbase_tx(self, amount, sender_address='0'*64):
		filename = MINER_ADDRESS
		if not os.path.isfile(filename):
			print("{} does not exist ".format(filename))
			return ""
		try:
			with open(filename, "r") as file_handler:
				miner_wif = file_handler.readline()
		except PermissionError:
			print("There are no permissions for opening ", filename)
			return ""
		miner_private_key = wallet.wif_to_private(miner_wif)
		miner_public_key = wallet.get_public_key(miner_private_key)
		miner_address = wallet.createWallet(miner_public_key)
		self.coinbase_tx = CoinbaseTransaction()
		self.coinbase_tx.set__sender_address(sender_address)
		self.coinbase_tx.set__recipient_address(miner_address.decode("utf-8"))
		self.coinbase_tx.set__amount(amount)
		self.coinbase_tx.calculate_concat()
		hash_concat = hashlib.sha256(bytes(self.coinbase_tx.get__concat().encode('utf-8'))).hexdigest()
		self.coinbase_tx.set__hash(hash_concat)
		self.coinbase_tx.set__signed_hash(tx_sign_message(miner_private_key, hash_concat.encode("utf-8"))[0])
		serializer = Serializer(self.coinbase_tx)
		serializer.get_all("")
		serializer.serialized += self.coinbase_tx.signed_hash
		return serializer.serialized

	def get_trusted_nods(self):
		with open(CONFIGURATION) as file_handler:
			trusted_nods = "\n".join(json.load(file_handler)["trusted_nods"])
		return trusted_nods.split('\n')

	def get_len_of_trusted_nods(self, list_trusted_nods):
		chain_lengths = []
		# quantity_trusted_nods = len(list_trusted_nods)
		for node in list_trusted_nods:
			try:
				node_ip = 'http://' + node + '/chain/length'
				chain_lengths.append(requests.get(url=node_ip, json=['']).json()['chain_length'])
			except:  # TODO: come up with new moments
				chain_lengths.append(0)
		return chain_lengths

	def get_bigger_chain(self, node_ip):
		try:
			ip = 'http://' + node_ip + '/chain'
			chain = requests.get(url=ip, json=['']).json()
			if os.path.isfile(CHAIN):
				os.remove(CHAIN)
			with open(CHAIN, "w+") as file_handler:
				for x in chain:
					file_handler.write(json.dumps(x, indent=4) + "\n")
		except PermissionError:
			print("There are no permissions for opening ", CHAIN)
		except:
			print("Something gone wrong get_bigger_chain !")

	def check_consensus(self):
		trusted_nods = self.get_trusted_nods()
		if len(trusted_nods) >= 1:
			chain_lengths = self.get_len_of_trusted_nods(trusted_nods)
			if self.get_len_chain() < max(chain_lengths):
				self.get_bigger_chain(trusted_nods[chain_lengths.index(max(chain_lengths))])

	def get__coinbase_tx(self):
		pass

	def set__coinbase_tx(self, value):
		self.coinbase_tx = value

	def submit_tx(self, new_tx):
		tx_list = new_tx.split('\n')
		for tx_element in tx_list:
			tx_pool = TransactionsPool()
			result = tx_pool.create_new_transaction(tx_element)
			if not result:
				return False
		return True

	def is_valid_chain(self):
		pass

	def set__last_hash(self, value):
		self.last_hash = value

	def get__last_hash(self):
		return self.last_hash

	def get__id(self):
		return self.id_blocks

	def change_mine_status(self):
		self.mine_mode = not self.mine_mode

	def get__mine_status(self):
		return self.mine_mode

	def mine(self):
		while True:
			while self.get__mine_status() is True:
				try:
					block_ = self.create_block(self.get__last_block_id() + 1,
													self.calculate_coinbase_tx("50"))
					block_.previous_hash = self.last_hash
					block_.json = json.dumps({
						"id": str(block_.get__index()),
						"prev_hash": block_.get__previous_hash(),
						"hash": block_.get__hash(),
						"nonce": str(block_.get__nonce()),
						"timestamp": str(block_.get__timestamp()),
						"merkle_root": block_.get__merkle_tree(),
						"transactions": block_.get__txs(),
					}, indent=4) + '\n'
					self.save_block_to_file(block_)
					self.save_block_to_blockchain(block_)
					self.remove_transactions()
					self.set__last_block(block_)
					self.set__last_hash(block_.hash)
					self.set__last_block_id(block_.index)
					print("i works well")
				except:
					return