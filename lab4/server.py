# server.py
# Varsha Tumburu (1901CS69)
import socket 
from os import path
import time

# fix IP address and port number of server
UDP_PORT = 8080
UDP_IP = '127.0.0.1'

# function to open text file, returns file pointer 
def open_file(filename):
	fpath = path.realpath(filename)
	print(fpath)
	if not path.exists(fpath):
		print("\033[1;36mRequested File Not Found\033[0m\n\n")
		return None
	else:
		print("Resource requested found at location:", fpath)
	f=open(fpath, "r")
	return f 

def main():
	# initialize UDP socket and bind it to address 
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_IP, UDP_PORT))

	print("\
    Connection is successfully established !!\n\
    \033[0;34m\n\
    *************************************\n\
    *                                   *\n\
    *       WELCOME TO THE SERVER       *\n\
    *                                   *\n\
    *      ALL STARTUP PROCESSES        *\n\
    *      SUCCESSFULLY EXECUTED        *\n\
    *                                   *\n\
    *************************************\n\
    \033[0m\n\
    Waiting for client request ...\n\n")

	# Run server as long as no error occurs and wait for requests from client 
	reqcount=0  # Keeps track of number of requests
	while True: 
		# Take file name from client  
		data, addr = sock.recvfrom(1024)
		data = data.decode()
		reqcount+=1

		print("\033[0;36mRequest No.%s\033[0m"%str(reqcount))
		if data:
			print("File name:", data)
			file_name = data.strip()
		fp = open_file(file_name) # Open particular file 

		# If None is returned and no file exists, then terminate server 
		if not fp:
			err_msg = "FILE_NOT_FOUND"
			print("\033[1;31mFile Not Found\033[0m\n")
			sock.sendto(err_msg.encode(), addr)
			time.sleep(1)
			sock.close()
			return 0
		# If file exists, store all words in array
		else:
			words=[]
			for line in fp:
				lw=line.split()
				words.extend(lw)
			
			# Only continue if first word is START, otherwise terminate with WRONG_FILE_FORMAT error
			if(words[0]=='START'):
				sock.sendto(words[0].encode(), addr)  # Send "START" to client 
			else:
				err_msg="WRONG_FILE_FORMAT"
				print("\033[1;31mWrong File Format\033[0m\n")
				sock.sendto(err_msg.encode(), addr)
				time.sleep(1)
				sock.close()
				return 0
	
		print("\033[1;35mGreeting Received\033[0m")

		# For all words following START, a request will be sent from client. 
		# Once request is received, send word to client to write in output file.
		for w in words[1:]:
			# Receive request from client 
			msg, addr = sock.recvfrom(1024)
			msg=msg.decode()
			assert msg[0:4]=='WORD', "Request format wrong"  # Assert if request is in the form WORD1, WORD2, etc 
			
			# Send word to client
			sock.sendto(w.encode(), addr)

			# Break if finishing command is found, "FINISH" in our case 
			if(w == 'FINISH'):
				print("\033[1;35mGoodbye\033[0m\n")
				break

	# Close socket 
	sock.close()
	return 0

if __name__=="__main__":
	main()
