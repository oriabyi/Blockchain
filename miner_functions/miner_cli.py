import json
from cmd import Cmd
import requests

class NodesInfo:
	def __init__(self):
		self.node_ip = ""
		self.nodes_ip = []


nodes_info = NodesInfo()


class MinerCLI(Cmd):
	prompt = "miner_cli: "

	def __init__(self):
		Cmd.__init__(self)

	def check_state_of_server(self, node):
		try:
			if node != '':
				url = node
				requests.get(url=url, json=[''])
				return True, ""
			return False, "No enough data"
		except requests.exceptions.ConnectionError:
			return False, "Connection error"
		except requests.exceptions.MissingSchema:
			return False, "Incorrect data"

	def add_new(self, arg):
		nodes_info.nodes_ip.append(arg)
		nodes_info.node_ip = arg

	def delete_note(self, arg):
		if nodes_info.node_ip == arg:
			nodes_info.node_ip = nodes_info.nodes_ip[len(nodes_info.nodes_ip) - 1]
		nodes_info.nodes_ip.remove(arg)

	def check_before_start(self):
		ip = nodes_info.node_ip
		status = self.check_state_of_server(ip)
		if status[0] is False:
			print("At this moment server is unvailable")
		return status[0]

	def do_st(self, line):
		self.add_new('http://127.0.0.1:5000')

	def do_getchainlen(self, line):
		if self.check_before_start() is True:
			url = nodes_info.node_ip + '/chain/length'
			# print(str(requests.get(url=url, json=['']).json()))
			print("{0}".format(str(requests.get(url=url, json=['']).json())))

	def do_getchain(self, line):
		if self.check_before_start() is True:
			url = nodes_info.node_ip + '/chain'
			# print(str(requests.get(url=url, json=['']).json()))
			print("{0}".format(str(requests.get(url=url, json=['']).json())))

	def do_mine(self, line):
		if self.check_before_start() is True:
			url = nodes_info.node_ip + '/mine'
			requests.get(url=url, json=[''])
			# try:
			# 	answer = answer.json()
			# 	print("{0:<30}\n{1}".format(nodes_info.node_ip, str(answer)))
			# except json.decoder.JSONDecodeError:
			# 	print("mained well but json.decoder.JSONDecodeError")

	def do_changeminemode(self, line):
		if self.check_before_start() is True:
			url = nodes_info.node_ip + '/mine/change_mode'
			requests.get(url=url, json=[''])

	def do_getminemode(self, line):
		if self.check_before_start() is True:
			url = nodes_info.node_ip + '/mine/change_mode_get'
			print(str(requests.get(url=url, json=['']).json()))


	def do_addnode(self, line):
		result, message = self.check_state_of_server(line)
		if result or message == "Connection error":
			nodes_info.nodes_ip.append(line[:line.rfind('/')])
			nodes_info.node_ip = line
			print("Address has been added")
		else:
			print(message)

	def do_getlastblock(self, line):
		if self.check_before_start() is True:
			url = nodes_info.node_ip + '/chain'
			print("{0:<30}\t{1}".format(nodes_info.node_ip, str(requests.get(url=url, json=['']).json())))
			# print(str(requests.get(url=url, json=['']).json()))

	def do_getblockbyheight(self, line):
		if self.check_before_start() is True:
			url = nodes_info.node_ip + '/block' + "?height=" + line
			print("{0:<30}\t{1}".format(nodes_info.node_ip, str(requests.get(url=url, json=['']).json())))
			# print(str(requests.get(url=url, json=['']).json()))

	def do_getbalance(self, line):
		if self.check_before_start() is True:
			if len(line) < 26:
				print("The address is invalid")
				return False
			if self.check_before_start() is True:
				url = nodes_info.node_ip + '/balance' + "?addr=" + line
				print("{0:<30}\t{1}".format(nodes_info.node_ip, str(requests.get(url=url, json=['']).json())))
				# print(str(requests.get(url=url, json=['']).json()))

	def do_checknodeschainlength(self, line):
		if nodes_info.node_ip == "":
			print("There are no nodes")
		else:
			for node_ip_ in nodes_info.nodes_ip:
				print("{0:<30}".format(node_ip_), end="\t")
				status_ip = self.check_state_of_server(node_ip_)
				nodes_info.node_ip = node_ip_
				if status_ip[0]:
					self.do_getchainlen(node_ip_)
				else:
					print(status_ip[1])

	def do_checknodesip(self, line):
		if nodes_info.node_ip == "":
			print("There are no nodes")
		else:
			for node_ip_ in nodes_info.nodes_ip:
				print("{0:<30}".format(node_ip_), end="\t")
				print(str(self.check_state_of_server(node_ip_)[0]))

	def do_exit(self, line):
		return True

	def do_EOF(self, line):
		return True

	def emptyline(self):
		self.do_help(str())

	def default(self, line):
		self.do_help(str())

def main():
	try:
		MinerCLI().cmdloop()
	except KeyboardInterrupt:
		print("\nProgram was closed")
	# except:
	# 	print("Something gone wrong __main__ !")


if __name__ == '__main__':
	main()
