# client.py
# Varsha Tumburu (1901CS69)
import socket
from os import path

# Server address
SERVER_PORT = 8080
SERVER_IP = '127.0.0.1'

# Function to open text file, returns file pointer 
def open_file(filename):
	fpath = path.realpath(filename)
	# Open file in write mode 
	if(path.exists(fpath)):
		f = open(fpath, "w")
		return f
	else:
		print("\033[0;35mERROR: Could not open the required file!! \033[0m\n")
		return None


def main():
	# Create datagram socket 
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_addr = (SERVER_IP, SERVER_PORT)
	print("\
	Connection is successfully established !!\n\
	\033[0;32m\n\
	*************************************\n\
	*                                   *\n\
	*      WELCOME TO THE CLIENT        *\n\
	*                                   *\n\
	*      ALL STARTUP PROCESSES        *\n\
	*      SUCCESSFULLY EXECUTED        *\n\
	*                                   *\n\
	*************************************\n\
	\033[0m\n\
	Sending request to server ...\n\n")

	status = 1
	outfile = "output.txt"
	# Run client as long as no error occurs and wait for responses from server 
	while True:
		# Take filename from user 
		file = input("Enter the file name (or 0 to exit): ")
		if(file == '0'):
			print("Client terminating...")
			sock.close()
			return 0

		# Send filename to server
		sock.sendto(file.encode(), server_addr)

		# Receive greeting from server 
		resp, addr = sock.recvfrom(1024)
		resp = resp.decode()

		# If proper greeting is received then open output file
		# otherwise print error and close socket
		if(resp == 'START'):
			print("SUCCESS!\n")
			fout = open_file(outfile)
			status = 1
		elif(resp == "FILE_NOT_FOUND"):
			print("\033[1;31mFile Not Found\033[0m\n")
			sock.close()
			return 0
		elif(resp == "WRONG_FILE_FORMAT"):
			print("\033[1;31mWrong File Format\033[0m\n")
			sock.close()
			return 0
		else:
			print("\033[1;31mReturn value not Recognised\033[0m\n\n")
			return 0

		# Receive contents from server until end signal is given ('FINISH')
		count = 0
		while(status):
			# Request for word{count}
			count += 1
			msg = "WORD"+str(count)
			print("Request for  \033[0;31m%s\033[0m" % (msg))
			sock.sendto(msg.encode(), server_addr)

			# Receive word from server 
			word, addr = sock.recvfrom(1024)
			word = word.decode()
			print("Received \033[0;32m%s\033[0m\n\n" % (word))

			# If end signal is given, break out of loop before writing into file 
			if(word == 'FINISH'):
				fout.close()
				print("Output Written in file \033[0;31moutput.txt\033[0m\n")
				status = 0
				break

			# Write word into output file 
			word = word + "\n"
			fout.write(word)

	# Close socket
	socket.close(sock)
	return 0

if __name__=="__main__":
	main()
