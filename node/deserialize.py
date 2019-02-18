import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../wallet_functions'))
from concat_tx import RAW_TX

class DeserializeRW:
	def __init__(self):
		self.txid = ""
		self.vout = ""
		self.value = ""
		self.version = ""
		self.sequence = ""
		self.lock_time = ""
		self.script_sig = ""
		self.input_count = ""
		self.output_count = ""
		self.script_pub_key = ""
		self.script_sig_size = ""
		self.script_pub_key_size = ""

	def deserialize(self, line):
		self.version = line[:8]
		self.input_count = line[8:10]
		self.txid = line[10:74]
		self.vout = line[74:82]
		self.script_sig_size = line[82:84]
		self.script_sig, position = self.get_script(line, int(self.script_sig_size, 16))
		self.sequence = line[position : position + 8]
		self.output_count = line[position + 8 : position : 10]
		self.value = line[position + 10 : position + 26]
		self.script_pub_key_size = line[position + 26 : position + 28]
		self.script_pub_key, position = self.get_script(line, int(self.script_pub_key_size, 16), position + 28)
		self.lock_time = line[position:]

	def get_script(self, line, len, start=84):
		result = ""
		len = 2 * len + start
		counter = start
		while counter < len:
			result += line[counter]
			counter += 1
		return result, len



# def main():
# 	line = "01000000017967a5185e907a25225574544c31f7b059c1a191d65b53dcc1554d339c4f9efc010000006a47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a825ffffffff014baf2100000000001976a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac00000000"
# 	DeserializeRW().deserialize(line)
#
# if __name__ == '__main__':
# 	main()