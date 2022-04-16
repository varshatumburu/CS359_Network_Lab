# Client side architecture
import threading
import socket

# Connect to server
alias = input('Choose a username >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59002))

# Client handler


def client_receive():
    while True:
        try:
            # Respond with username when server asks
            message = client.recv(1024).decode()
            if(message == "alias?"):
                client.send(alias.encode())
            # Respond with disease if server asks for it
            elif(message == "disease?"):
                dis = input('Enter symptoms to check for medicine >>> ')
                client.send(dis.encode())
            # Otherwise print message on terminal
            else:
                print(message)
        except:
            # Report error and close connection
            print("Error!")
            client.close()
            break


# Start receiving client thread
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()
