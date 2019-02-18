import os
import sys
import ecdsa
import base58
import codecs
import hashlib
import unittest
import binascii
sys.path.append(os.path.join(os.path.dirname(__file__), '../wallet_functions'))
import wallet
import wallet_cli

count_tests = 10


class TestWalletFunctions(unittest.TestCase):

	def test_generation_pk(self):
		for counter in range(0, count_tests):
			self.assertLess(wallet.generPrivKey().upper(),
							"FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141")

	def test_gener_public_key(self):
		# uncompressed
		for counter in range(0, count_tests):
			self.assertEqual(wallet.get_public_key(wallet.generPrivKey(), False)[:2], "04")
		# compressed
		for counter in range(0, count_tests):
			random_public_key = wallet.get_public_key(wallet.generPrivKey())[:2]
			if random_public_key != "03":
				self.assertEqual(random_public_key, "02")

	def test_create_wallet_address(self):
		for counter in range(0, count_tests):
			address = wallet.createWallet(wallet.get_public_key(wallet.generPrivKey())).decode("utf-8")
			self.assertGreater(len(address), 0)
			self.assertNotRegex(address, 'O')
			self.assertNotRegex(address, 'I')
			self.assertNotRegex(address, 'l')
			self.assertNotRegex(address, '0')
			decode_address = binascii.hexlify(base58.b58decode(address))
			checksum = decode_address[-8:].decode("utf-8")
			hash_address = hashlib.new('sha256', binascii.unhexlify(decode_address[:-8])).hexdigest()
			hash_address = hashlib.new('sha256', binascii.unhexlify(hash_address)).hexdigest()
			self.assertEqual(hash_address[:8], checksum)

	def test_wif_convert(self):
		for counter in range(0, count_tests):
			def_private_key = wallet.generPrivKey()
			wif = wallet.private_key_to_wif(def_private_key)
			private_from_wif = wallet.wif_to_private(wif)
			self.assertEqual(def_private_key, private_from_wif[:-2])

	def test_sign_message(self):
		for counter in range(0, count_tests):
			private_key = wallet.generPrivKey()
			public_key = wallet.get_public_key(private_key, False)
			message = wallet.generPrivKey()
			signed_message = wallet_cli.signMessage(private_key, message)[0]
			sign = bytes.fromhex(signed_message)
			vk = ecdsa.VerifyingKey.from_string(codecs.decode(public_key[2:], 'hex'), curve=ecdsa.SECP256k1)
			result = vk.verify(sign, bytes(message, "utf-8"))
			self.assertTrue(result)


if __name__ == '__main__':
	unittest.main()