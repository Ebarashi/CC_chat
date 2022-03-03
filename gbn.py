from pack import Packet
import socket
import threading


class RDTProtocols:

    def __init__(self, server):
        self.server = server
        print('Initiating RDTP')

    def go_back_n(self, server, server_socket, client_address, window_size=5):
        pkt_list = server.pkt_list
        server_socket.settimeout(5)
        flag = False
        i = 0
        lost_pkts = server.get_lost_packets(len(pkt_list), server.probability, server.random_seed)
        print(lost_pkts)
        while i < len(pkt_list):
            current_pkt = pkt_list[i:window_size + i]
            if window_size + i > len(pkt_list):
                current_pkt = pkt_list[i:]
            for pkt in current_pkt:
                send = True
                if pkt.seqno in lost_pkts:
                    send = False
                    lost_pkts.remove(pkt.seqno)
                if send:
                    print('Sending packet # ', pkt.seqno)
                    pkd_packet = pkt.pack(type='bytes')
                    server_socket.sendto(pkd_packet, client_address)
                if flag is True and not send:
                    flag = False
                    break
            for pkt in current_pkt:
                try:
                    ack = server_socket.recv(6000)
                    unpkd_ack = Packet(pkd_data=ack, type='ack')
                    if unpkd_ack.checksum == pkt.checksum:
                        i += 1
                        print('Ack# ' + str(unpkd_ack.seqno) + ' received')
                    else:
                        flag = True
                        break
                except socket.timeout as e:
                    send = True
                    print('Ack # ' + str(pkt.seqno) + ' ack has timed out....resending packet')
                    break
