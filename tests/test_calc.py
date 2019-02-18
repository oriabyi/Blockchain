import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../wallet_functions'))
import wallet

class WrongGenerPrivateKey(Exception):
	pass


class TestWalletFunctions(unittest.TestCase):
	def gener_private(self):
		for x in range(0, 100):
			if wallet.generPrivKey().upper() >= \
					"FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141":
				raise WrongGenerPrivateKey


	def gener_public_key(self):
		private_key = wallet.generPrivKey()
		public_key = wallet.get_public_key(private_key, True)
		self.assertNotEqual(public_key[:2], "04")

	# def

if __name__ == '__main__':
	unittest.main()