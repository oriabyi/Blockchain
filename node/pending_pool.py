import os
from transaction import Transaction
from serializer import Deserializer
from tx_validator import check_availiability_address, check_ratio_public_and_address, check_validity_signature, \
		validate_signature, verif_signature

WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
MEMORY_POOL = WORKING_DIRECTORY + "/mempool"

def check_new_tx(tx):
	if check_availiability_address(tx.get__sender_address()) is False:
		return False
	elif check_ratio_public_and_address(tx.get__public_key(), tx.get__sender_address().encode("utf-8"), False) is False:
		return False
	elif verif_signature(tx.get__public_key()[2:], tx.get__concat(), tx.get__sign()) is False:
		return False
	else:
		return True

class TransactionsPool:
	def __init__(self):
		pass

	def create_pool(self, filename):
		try:
			with open(filename, "w+"):
				pass
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong create_pool !")

	def check_exist_of_file(self, filename):
		if os.path.isfile(filename) is False:
			self.create_pool(filename)

	def save_to_mempool(self, set_tx):
		filename = MEMORY_POOL
		self.check_exist_of_file(filename)
		try:
			with open(filename, 'a+') as file_handle:
				file_handle.write("%s\n" % set_tx)
		except PermissionError:
			print("There are no permissions for opening ", filename)
		except:
			print("Something gone wrong save_to_mempool !")

	def create_new_transaction(self, serialized_tx):
		# amount, sender_address, recipient_address, sender_public_key, signed_hash = Deserializer().get_all(serialized_tx)
		# tx = Transaction()
		# tx.set__amount(amount)
		# tx.set__sender_address(sender_address)
		# tx.set__recipient_address(recipient_address)
		# tx.set_concat(sender_address.encode("utf-8"), recipient_address.encode("utf-8"), amount.encode("utf-8"))
		# tx.set__hash(tx.hash_calculate())
		# tx.set__vk(sender_public_key)
		# tx.set__sign(signed_hash)
		# tx.set__public_key(sender_public_key)
		# tx.set__sender_address(sender_address)
		# if check_new_tx(tx) is True:
		self.save_to_mempool(serialized_tx)
		return True
		# return False


def save_results_to_file(serialized_line):
	filename = MEMORY_POOL
	try:
		with open(filename, "a+") as file_handler:
			file_handler.write(serialized_line + "\n")
	except PermissionError:
		print("There are no permissions for opening ", filename)
	except:
		print("Something gone wrong save_results_to_file !")


def getNotes():
	nodes = list()
	filename = MEMORY_POOL
	if not os.path.isfile(filename):
		print("{} does not exist ".format(filename))
		return ""
	try:
		with open(filename) as file_hanfdler:
			nodes = file_hanfdler.readlines()[-3:]
		if len(nodes) < 3:
			return list()
		else:
			return nodes
	except PermissionError:
		print("There are no permissions for opening ", filename)
	except:
		print("Something gone wrong get_notes !")
	finally:
		return nodes



def pending_pool(tx, serialized_line, vk, primeval_hash):
	deserializer = Deserializer()
	amount, sender_address, recipient_address, \
		sender_public_key, signed_hash = deserializer.get_all(tx.get__serialize_line())
	check = check_availiability_address(sender_address)
	if check is True:
		check = check_availiability_address(recipient_address)
	if check is True:
		check = check_ratio_public_and_address(sender_public_key, sender_address.encode("utf-8"), False)
	if check is True:
		check = check_validity_signature(signed_hash, primeval_hash, vk)
	if check is False:
		return False
	# save_results_to_file(serialized_line)
	return serialized_line
