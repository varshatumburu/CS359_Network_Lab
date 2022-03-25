# Server side architecture 
from pydoc import cli
import threading 
import socket

# Server address 
host = '127.0.0.1'
port = 59001

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients=[]
aliases=[]

# Function to send message to all clients 
def broadcast(message):
	for client in clients:
		client.send(message.encode())

#  Function to handle clients' connection 
def handle_client(client):
	while True:
		# If message is received 
		try:
			message = client.recv(1024).decode()
			broadcast(message)
		# Else close client 
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			alias = aliases[index]
			broadcast(f'{alias} has left the chatroom!'.encode('utf-8'))
			aliases.remove(alias)
			break

#  Main function to receive the clients connection
def receive():
	while True:
		print('Server is running and listening...')

		# Accept a client
		client, address = server.accept()
		print(f'Connection is established with {str(address)}')

		# Ask for username 
		greet = 'alias?'
		client.send(greet.encode())
		alias = client.recv(1024).decode()

		# Add to clients list 
		aliases.append(alias)
		clients.append(client)
		print(f'New client: {alias}')

		# Broadcast to all users 
		broadcast(f'{alias} has connected to the chatroom')

		# Send confirmation to client 
		confirm = 'You are now connected!'
		client.send(confirm.encode())

		# Start new thread
		thread = threading.Thread(target=handle_client, args=(client,))
		thread.start()

if __name__=="__main__":
	receive()
