import os
import sys
import ecdsa
import base58
import hashlib
import binascii
from codecs import decode
sys.path.append(os.path.join(os.path.dirname(__file__), '../wallet_functions'))
from wallet import createWallet, compressPublicKey


def checkLetter(string, letter):
	return True if string.find(letter) >= 0 else False

def check_availiability_address(primorAdress):
	if len(primorAdress) == 0:
		return False
	if type(primorAdress) == bytes:
		address = primorAdress.decode("utf-8")
	else:
		address = primorAdress
	if checkLetter(address, 'O') or checkLetter(address, 'I') \
		or checkLetter(address, 'l') or checkLetter(address, '0'):
		return False
	if address[0] != '1' and \
		address[0] != '3' and \
		address[0] != 'n' and \
		address[0] != 'm' and \
		address[0:3] != "bc1":  # check 'n' and 'm' for testnet
		return False
	decodeAdress = binascii.hexlify(base58.b58decode(address))
	checksum = decodeAdress[-8:].decode("utf-8")
	hashAdress = hashlib.new('sha256', binascii.unhexlify(decodeAdress[:-8])).hexdigest()
	hashAdress = hashlib.new('sha256', binascii.unhexlify(hashAdress)).hexdigest()
	if hashAdress[:8] != checksum:
		return False
	else:
		return True


def check_ratio_public_and_address(public_key, sender_address, compress=False):
	created_wallet = createWallet(public_key)
	if compress is True:
		public_key = compressPublicKey(public_key.encode("utf-8"))
		created_wallet = createWallet(public_key).decode("utf-8")
	if created_wallet != sender_address:
		return False
	return True


def check_validity_signature(signedMessage, primevalMessage, ver_key):
	try:
		if type(primevalMessage) == str:
			primevalMessage = primevalMessage.encode("utf-8")
		result = ver_key.verify(bytes.fromhex(signedMessage), primevalMessage)
		return result
	except ecdsa.BadSignatureError:
		return False

def sign_message(private_key, message):
	sk = ecdsa.SigningKey.from_string(decode(private_key, "hex"), curve=ecdsa.SECP256k1)
	vk = sk.verifying_key
	signed_msg = sk.sign(message)
	assert vk.verify(signed_msg, message)  # TODO: comment this
	return signed_msg.hex(), vk

def validate_signature(tx, pub_key):
	try:
		vk = ecdsa.VerifyingKey.from_string(decode(pub_key[2:], 'hex'), curve=ecdsa.SECP256k1)
		tx.hash_calculate()
	except:
		return False
	if not vk.verify(tx.get__sign(), bytes(tx.get_hash(), 'utf-8')):  # True
		return False
	return True

def verif_signature(pub_key, concat, sign):
	result = False
	try:
		concat = concat.decode("utf-8")
		sign = bytes.fromhex(sign)
		vk = ecdsa.VerifyingKey.from_string(decode(pub_key, 'hex'), curve=ecdsa.SECP256k1)
		hash = hashlib.sha256(bytes(concat.encode("utf-8"))).hexdigest()
		result = vk.verify(sign, bytes(hash, "utf-8"))
	except:
		print("Got problem with verification of signature")
	return result
