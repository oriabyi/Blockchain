import os
import json
from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain
from flask_cors import CORS


import logging, threading, time
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

node = Flask(__name__)
node.config['DEBUG'] = False

CORS(node)

WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CHAIN = WORKING_DIRECTORY + "/blocks"
CONFIGURATION = WORKING_DIRECTORY + "/configuration"

# A completely random address of the owner of this node
miner_address = "00453233600a96384bb8d73d400984117ac84d7e8b512f43c4"
# This node's blockchain copy
blockchain_ = None


def run_node(host, port):
	global node

	node.run(host=host, port=port, threaded=True)
	# node.run(host=host, port=port, threaded=True, ssl_context='adhoc')


class NodeServer(threading.Thread):
	def __init__(self, host, port):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port

	def run(self):
		run_node(self.host, self.port)


class MineProcess(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global blockchain_

		blockchain_.mine()


def arr_str_to_json(ser_txs):
	len_txs = len(ser_txs)
	json_txs = json.dumps([json.JSONDecoder().decode(
		json.dumps({'id': i, 'ser_tx': ser_txs[i]})) for i in range(0, len_txs)])
	return json.dumps(json_txs)


def convert_list_to_dictionary():
	dict_list = list()
	filename = CHAIN
	if not os.path.isfile(filename):
		print("{} does not exist ".format(filename))
		return
	try:
		with open(filename, 'r') as file_handle:
			temp_line = file_handle.readline()
			dict_list = list()
			dictionary = {}
			while temp_line is not "":
				if temp_line.find("\"id\":") is not -1:
					value = temp_line[temp_line.find("\"id\":") + 6:].split(',')[0][1:-1]
					dictionary["id"] = value
				elif temp_line.find("\"prev_hash\":") is not -1:
					value = temp_line[temp_line.find("\"prev_hash\":") + 14:].split(',')[0][:-1]
					dictionary["prev_hash"] = value if value is not "" else str()
				elif temp_line.find("\"hash\":") is not -1:
					value = temp_line[temp_line.find("\"hash\":") + 9:].split(',')[0][:-1]
					dictionary["hash"] = value if value is not "" else str()
				elif temp_line.find("\"nonce\":") is not -1:
					value = temp_line[temp_line.find("\"nonce\":") + 8:].split(',')[0][2:-1]
					dictionary["nonce"] = value
				elif temp_line.find("\"timestamp\":") is not -1:
					value = temp_line[temp_line.find("\"timestamp\":") + 13:].split(',')[0][1:-1]
					dictionary["timestamp"] = value
				elif temp_line.find("\"merkle_root\":") is not -1:
					value = temp_line[temp_line.find("\"merkle_root\":") + 16:].split(',')[0][:-1]
					dictionary["merkle_root"] = value
				elif temp_line.find("\"transactions\":") is not -1:
					tx_list = list()
					temp_line = file_handle.readline()
					while temp_line.find("]") is -1 and temp_line is not "":
						tx_list.append((temp_line.split(',')[0][9:])[:-4])
						temp_line = file_handle.readline()
					dictionary["transactions"] = tx_list
					dict_list.append(dictionary.copy())
					continue
				temp_line = file_handle.readline()
	except PermissionError:
		print("There are no permissions for opening ", filename)
	except:
		print("Something gone wrong convert_list_to_dictionary!")
	finally:
		return dict_list


@node.route('/transaction/new', methods=['POST', 'HTTP'])
def get_new_transaction():
	global blockchain_

	try:
		if not request.is_json:
			pass  # TODO: except
		tx = request.get_json()
		if not blockchain_.submit_tx(tx['serialized_tx']):
			pass  # TODO: error
	except:
		pass
	return jsonify('')

# @app.route('/qwe', methods=['GET'])

def list_to_dictionary(dict_):
	new_dict = dict()
	for i in range(0, len(dict_)):
		temp = dict_[i].split('\"')
		if temp[1] == "transactions":
			temp_lst = list()
			i += 1
			while i < len(dict_) and dict_[i]:
				temp_lst.append(dict_[i].split('\"')[1][:-3])
				i += 1
			new_dict[temp[1]] = temp_lst
			break
		else:
			new_dict[temp[1]] = temp[3]
	return new_dict


@node.route('/block', methods=['GET'])
def get_blockbyheight():
	global blockchain_

	height = request.args.get('height')
	return jsonify(list_to_dictionary(blockchain_.get_block_by_height(height)))


@node.route('/balance', methods=['GET'])
def get_balance():
	global blockchain_

	address = request.args.get('addr')
	return json.dumps(blockchain_.get_balance_by_address(address))

@node.route('/hash', methods=['GET'])
def get_tx_by_hash():
	global blockchain_

	hash = request.args.get('hash')
	return jsonify(list_to_dictionary(blockchain_.get_tx_hash(hash)))


@node.route('/consensus', methods=['GET'])
def consensus():
	global blockchain_

	blockchain_.check_consensus()
	return jsonify('consensus works well')


@node.route('/transaction/pendings', methods=['GET'])
def get_pendings_txs():
	global blockchain_

	return arr_str_to_json(blockchain_.get_pending_txs())


@node.route('/transaction/pendings/length', methods=['GET'])
def get_len_pendings_txs():
	global blockchain_

	return jsonify(blockchain_.get_pending_txs_length())


@node.route('/chain', methods=['GET'])
def get_chain():
	global blockchain_

	return json.dumps(convert_list_to_dictionary())
	# return json.dumps(blockchain_.get_chain())


@node.route('/chain/length', methods=['GET'])
def get_chain_length():
	global blockchain_

	return jsonify({'chain_length': blockchain_.get_len_chain()})


@node.route('/block/last', methods=['GET'])
def get_last_block():
	global blockchain_

	return json.dumps(''.join(blockchain_.get_last_block()))


@node.route('/mine/change_mode', methods=['GET'])
def change_mine_mode():
	global blockchain_

	blockchain_.change_mine_status()
	if blockchain_.get__mine_status():
		mine()


@node.route('/mine/change_mode_get', methods=['GET'])
def change_mine_mode_get():
	global blockchain_

	return json.dumps(blockchain_.change_mine_status())


@node.route('/mine', methods=['GET'])
def mine():
	global blockchain_

	while True:
		while blockchain_.get__mine_status() is True:
			try:
				block_ = blockchain_.create_block(blockchain_.get__last_block_id() + 1,
												blockchain_.calculate_coinbase_tx("50"))
				block_.previous_hash = blockchain_.last_hash
				block_.json = json.dumps({
					"id": str(block_.get__index()),
					"prev_hash": block_.get__previous_hash(),
					"hash": block_.get__hash(),
					"nonce": str(block_.get__nonce()),
					"timestamp": str(block_.get__timestamp()),
					"merkle_root": block_.get__merkle_tree(),
					"transactions": block_.get__txs(),
				}, indent=4) + '\n'
				blockchain_.save_block_to_file(block_)
				blockchain_.save_block_to_blockchain(block_)
				blockchain_.remove_transactions()
				blockchain_.set__last_block(block_)
				blockchain_.set__last_hash(block_.hash)
				blockchain_.set__last_block_id(block_.index)
				print("i works well")
			except:
				return

@node.route('/_get_chain_length/', methods=['POST'])
def _get_chain_length():
	global blockchain_

	return get_chain_length()


def main():
	global blockchain_

	if not os.path.isfile(CONFIGURATION):
		print("{} does not exist ".format(CONFIGURATION))
		return False
	try:
		with open(CONFIGURATION) as file_handler:
			conf_dict = json.load(file_handler)
		host, port = conf_dict['host_ip'].split(':')[:2]
		blockchain_ = Blockchain()
		blockchain_.change_mine_status()  # TODO: uncomment me

		node_server = NodeServer(host=host, port=port)
		mine_process = MineProcess()
		node_server.start()
		mine_process.start()
		node_server.join()
		mine_process.join()
	except PermissionError:
		print("There are no permissions for opening ", CONFIGURATION)
	except json.decoder.JSONDecodeError:
		print("Bad json format in ", CONFIGURATION)
	except:
		print("Something gone wrong main !")


if __name__ == "__main__":
	try:
		main()
	except:
		print("server is closed")
