import pack as pac_gen
import pickle
import pack_loss
import random
import pickle

import socket
import threading
import os

BUF_SIZE = 4096

HOST = '10.100.102.13'
# '10.0.0.4'
# HOST = '10.0.0.5'
PORT = 6666
PORT_UDP = 7777

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT_UDP))

server.listen()
print("Server is listening for connections")
print("IP\t: ", HOST)
print("PORT\t: ", PORT_UDP, PORT)

clients = []
names = []


class StopAndWait:
    BUF_SIZE = 4096  # max size of received packet (ACK)

    def __init__(self, file_name, t_sock, rec_addr, time_out, p_loss):
        #  self.fileNAme=os.getcwd()+"/server_files/"+file_name
        self.socket = t_sock
        self.dest = rec_addr
        self.time_out = time_out
        self.p_loss = p_loss
        self.time_out_sock = time_out * 100  # Socket timeout is 10 times the packet timeout
        self.gen = pac_gen.PacketGen(file_name)
        self.timer = None
        self.socket.settimeout(self.time_out_sock)

    def send(self):
        packet = self.gen.gen_packet_from_file()
        while packet:
            print("Sending: packet ", packet.seqno)
            if not pack_loss.lose_packet(self.p_loss):
                self.socket.sendto(pickle.dumps(packet), self.dest)
            self.timer = threading.Timer(self.time_out, timer_handler, args=(self, packet,))
            self.timer.start()

            # wait for ACK or abort after a long period of time
            while 1:
                ack = None
                addr = None
                try:
                    print("\tWaiting For ACK: packet ", packet.seqno)
                    ack, addr = self.socket.recvfrom(self.BUF_SIZE)
                except socket.timeout:
                    print("Error: 10 retransmissions of packet have occured yet no ACKs were received. Aborting.")
                    self.timer.cancel()
                    return None

                if addr == self.dest and pickle.loads(ack).ackno == packet.seqno:  # correct ACK received
                    print("\tACK received for packet ", packet.seqno)
                    self.timer.cancel()
                    packet = self.gen.gen_packet_from_file()  # update the packet
                    break
                else:
                    print("\tWrong ACK or Wrong sender")
        print("File has been transferred successfully, sending close packet")
        end = self.gen.gen_close_packet()
        self.socket.sendto(pickle.dumps(end), self.dest)


def timer_handler(self, packet):
    # retransmit packet to the same client
    print("\tTimeout: retransmitting packet ", packet.seqno)
    if not pack_loss.lose_packet(self.p_loss):
        self.socket.sendto(pickle.dumps(packet), self.dest)
    self.timer.cancel()
    self.timer = threading.Timer(self.time_out, timer_handler, args=(self, packet,))
    self.timer.start()


def send_all(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
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
            elif message == 'serverFiles':
                x = "server files:+" + os.listdir(os.getcwd() + '/server_files').__repr__()  # 'c/../server_files'
                client.send(x.encode('utf-8'))
            elif 'private' == header:
                name, private_m = (message.split('+')[1], message.split('+')[2])
                name = name[0:len(name) - 1:]
                try:
                    ind = names.index(name)
                    to_client = clients[ind]
                    client.send(f"private to {name}{private_m[13 + len(names[clients.index(client)])::]}".encode())
                    to_client.send(private_m.encode("utf-8"))
                except (socket.error, ValueError, IndexError):
                    client.send(f"server: wrong name\n".encode('utf-8'))
            else:
                send_all(message.encode('utf-8'))
        except socket.error:
            try:
                ind = clients.index(client)
                clients.remove(client)
                client.close()
                message1 = f"{names[ind]} left\n"
                send_all(message1.encode('utf-8'))
                name = names[ind]
                names.remove(name)
            except:
                client.close()


def handler(packet, rec_addr, SERVER_IP, TIMEOUT, P_LOSS):
    print("Received packet from host ", rec_addr)
    print("Acquiring new vacant socket")
    # acquire a vacant socket
    # t_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # t_sock.bind((SERVER_IP, 0))
    # t_port = t_sock.getsockname()[1]
    # print("New socket created on port ", t_port)
    # t_sock.sendto(pickle.dumps(t_port), rec_addr)

    ser = StopAndWait(packet.data, sock, rec_addr, TIMEOUT, P_LOSS)
    # ser = StopAndWait(packet.data, t_sock, rec_addr, TIMEOUT, P_LOSS)
    ser.send()

    print("Done sending, destroying connection")
    # t_sock.close()
    # t_sock.shutdown(1)


def recieve():
    while True:
        client, address = server.accept()
        client.send("name".encode('utf-8'))
        name = client.recv(1024).decode('utf-8')

        send_all(f"{name} connected to the server\n".encode('utf-8'))

        names.append(str(name))
        clients.append(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        i = 0
        packet, rec_addr = sock.recvfrom(BUF_SIZE)
        p = pickle.loads(packet)

        t = threading.Thread(target=handler, args=(p, rec_addr, HOST, 2, 0.1,))
        t.setName(str(i))
        i = i + 1
        t.start()


recieve()

# sock.close()
