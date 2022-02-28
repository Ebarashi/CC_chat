import socket
import threading

HOST = '10.9.3.159'
# HOST = '10.0.0.5'
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
            message = client.recv(1024).decode('utf-8')
            if 'left' in message:
                print('fed')
                send_all(message.encode('utf-8'))
                ind = clients.index(client)
                clients.remove(client)
                client.close()
                names.pop(ind)
            elif message == 'online':
                x = "list" + names.__repr__()
                client.send(x.encode('utf-8'))
            else:
                send_all(message.encode('utf-8'))
        except:
            break
            # ind = clients.index(client)
            # clients.remove(client)
            # client.close()
            # name = names[ind]
            # names.remove(name)


def recieve():
    while True:
        client, address = server.accept()
        client.send("NAME".encode('utf-8'))
        name = client.recv(1024).decode('utf-8')

        names.append(name)
        clients.append(client)
        print(client)

        send_all(f"{name} connect to the server\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


recieve()

