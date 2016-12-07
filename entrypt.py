"""
XOR Encryption is simple yet powerful 
technique to encrypt and decrypt any string

"""

def encryptDecrypt(input):
	Salt = ['K', 'E', 'R', 'T'] # can be any chars 
	output = []
	for i in range(len(input)):
		output.append(chr(ord(input[i]) ^ ord(Salt[i % len(Salt)])))
	return ''.join(output)


def main():
	input_string = "himanshugautam.net"
	encrypt = encryptDecrypt(input_string)
	print "Encrypted form\t",encrypt
	decrypt = encryptDecrypt(encrypt)
	print "Decrypted form\t",decrypt
if __name__ == '__main__':
	main()