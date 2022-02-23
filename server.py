import socket
import threading

HOST = '127.0.0.1'
PORT = 6666

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
names = []


def send_all(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            send_all(message)
        except:
            ind = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[ind]
            names.remove(name)
            break


def recieve():
    while True:
        client, address = server.accept()
        client.send("NAME".encode('utf-8'))
        name = client.recv(1024).decode('utf-8')

        names.append(name)
        clients.append(client)

        send_all(f"{name} connect to the server\n".encode('utf-8'))
        client.send("connect".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


recieve()
