# Server side architecture
import threading
import socket
import csv
import os

# Server address
host = '127.0.0.1'
port = 59002

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Client handler
def handle_client(client):
    while True:
        # Signals client to provide disease name
        message = "disease?"
        client.send(message.encode())

        # If input is given, then search for disease in the excel sheet
        try:
            disease = client.recv(1024).decode()
            print(f'Medicine required for {disease}')
            resp = ""

            # Open csv reader and parse through row values
            file = open("./data.csv", "r")
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                # print(row)
                if(row[0] == disease):
                    resp = row[1]
                    break

            if(resp == ""):
                out = disease + " unfound in records."
            else:
                out = "Try treating it with "+resp
            # Send response back to client
            client.send(out.encode())

        # Otherwise close client
        except:
            idx = clients.index(client)
            alias = users[idx]
            clients.remove(client)
            client.send(f'{alias} has left the chat!'.encode())
            client.close()
            users.remove(alias)
            break


clients = []
users = []
# Establish connection with client


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

        # Add to client list
        clients.append(client)
        users.append(alias)
        print(f'New client: {alias}')

        # Send confirmation message
        intro = "Welcome to your medical chatbot!"
        client.send(intro.encode())

        # Start new client thread
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
