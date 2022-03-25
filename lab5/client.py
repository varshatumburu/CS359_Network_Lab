# Client side architecture
import threading
import socket

# Connect to server
alias = input('Choose a username >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59001))


def client_receive():
    while True:
        try:
            # Respond with username when server asks
            message = client.recv(1024).decode()
            if(message == "alias?"):
                client.send(alias.encode())
            else:
                print(message)
        except:
            # Report error and close connection
            print("Error!")
            client.close()
            break


def client_send():
    while True:
        # Print and send message
        message = f'{alias}: {input("")}'
        client.send(message.encode())


# Start receiving client thread
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

# Start sending client thread
send_thread = threading.Thread(target=client_send)
send_thread.start()
