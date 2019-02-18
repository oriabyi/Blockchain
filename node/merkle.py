from hashlib import sha256


def merkle_root(trans):
	x = 0
	blocks = list()
	while x != len(trans):
		print(blocks.append(sha256(trans[x].encode('utf-8')).hexdigest()))
		x += 1
	while len(blocks) != 1:
		if len(blocks) % 2 != 0:
			blocks.append(blocks[len(blocks) - 1])
		x = 0
		size = len(blocks)
		while x < size:
			blocks.append(sha256((blocks[x] + blocks[x + 1]).encode('utf-8')).hexdigest())
			x += 2
		blocks = blocks[size:]
	return blocks[0]
