import socket
import threading
import server_files

HOST = '10.0.0.4'
# '10.0.0.4'
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
            print(message)
            header = message.split('+')[0]
            # if 'left' == header:
            #     send_all(message.split('+')[1].encode('utf-8'))
            #     ind = clients.index(client)
            #     clients.remove(client)
            #     client.close()
            #     names.pop(ind)
            if message == 'online':
                x = "users+" + names.__repr__()
                client.send(x.encode('utf-8'))
            if message == 'severFiles':
                #more code needed
                x = "server files:+" + names.__repr__()
                client.send(x.encode('utf-8'))
            elif 'private' == header:
                name, private_m = (message.split('+')[1], message.split('+')[2])
                name = name[0:len(name)-1:]
                try:
                    ind = names.index(name)
                    to_client = clients[ind]
                    client.send(f"private to {name}{private_m[13 + len(names[clients.index(client)])::]}".encode())
                    to_client.send(private_m.encode("utf-8"))
                except (socket.error, ValueError,IndexError):
                    client.send(f"server: wrong name".encode('utf-8'))
            else:
                send_all(message.encode('utf-8'))
        except socket.error:
            try:
                ind = clients.index(client)
                clients.remove(client)
                client.close()
                message1 = f"{names[ind]} left"
                send_all(message1.encode('utf-8'))
                name = names[ind]
                names.remove(name)
            except:
                client.close()


def recieve():
    while True:
        client, address = server.accept()
        client.send("NAME".encode('utf-8'))
        name = client.recv(1024).decode('utf-8')

        send_all(f"{name} connected to the server\n".encode('utf-8'))

        names.append(str(name))
        clients.append(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


recieve()
