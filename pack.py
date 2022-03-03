import struct
import numpy as np
import file_handler as hand
import random
import sys
import checksum


class PacketGen:
    CHUNK_SIZE = 500

    def __init__(self, file_name=None):
        self.init_seqno = 1  # ((random.randint(0,sys.maxsize)%100)+1) # randomly generated sequence number
        self.next_seqno = self.init_seqno
        if not file_name is None:
            self.file_name = file_name
            self.file_is_reg = 1  # boolean that indicates sys.maxsizethat a file was assigned to this PacketGenerator
            self.f_handler = hand.File_handler(self.file_name, self.CHUNK_SIZE)
        else:
            self.file_is_reg = 0

    def gen_packet(self, data_string):
        packet = Packet(checksum.gen_cksum(checksum.string_to_byte_arr(data_string)),
                        (len(data_string) * 8 + 12), self.next_seqno, data_string)
        self.next_seqno = self.next_seqno + 1
        return packet

    def gen_close_packet(self):
        packet = Packet(0, 12, 0, "")
        return packet

    def gen_packet_from_file(self):  # returns None if file was not registered to the PacketGen at the construction time
        # check by "if <return> is not None : <file was registered at construction time> "
        if self.file_is_reg == 0:
            return None
        data_bytes = self.f_handler.get_next_chunk()
        if not data_bytes:
            return None
        packet = Packet(checksum.gen_cksum(checksum.string_to_byte_arr(data_bytes)), len(data_bytes) + 12,
                        self.next_seqno, data_bytes)
        self.next_seqno = self.next_seqno + 1
        return packet


# gen = PacketGen("/tmp/server/test.txt")
# packet = gen.gen_packet_from_file()
# if packet is not None :
# 	print (packet.len)
# 	print (packet.cksum)
# else :
# 	print ("error: file not specified")
# packet = gen.gen_packet_from_file()
# if packet is not None :
# 	print (packet.len)
# else :
# 	print ("error: file not specified")
class Packet:
    def __init__(self, cksum, len, seqno, data):
        self.cksum = np.uint16(cksum)
        self.len = np.uint16(len)
        self.seqno = np.uint32(seqno)
        self.data = data


# def __init__(self, pkd_data=None, seqno=0, data='', type='bytes', chk_sum=0):
#     if pkd_data and type is not 'ack':
#         var, data = self.unpack(pkd_data)
#         self.checksum = var[0]
#         self.length = var[1]
#         self.seqno = var[2]
#         if type == 'str':
#             self.data = data.decode()
#         else:
#             self.data = data
#     elif type == 'ack':
#         if pkd_data:
#             var = self.unpack(pkd_data, type=type)
#             self.checksum = var[0]
#             self.seqno = var[1]
#         else:
#             self.seqno = seqno
#             self.checksum = chk_sum
#     else:
#         self.length = len(data) + 8
#         self.seqno = seqno
#         self.data = data
#         self.checksum = calc_checksum(data, type=type)
#
# def unpack(self, data, type='bytes'):
#     if type == 'ack':
#         return struct.unpack('HH', data)
#     else:
#         size = struct.calcsize('HHI')
#         return struct.unpack('HHI', data[:size]), data[size:]
#
# def pack(self, type='bytes'):
#     if type == 'ack':
#         return struct.pack('HH', self.checksum, self.seqno)
#     if type == 'str':
#         encoded_data = self.data.encode()
#     else:
#         encoded_data = self.data
#     str_len = len(encoded_data)
#     fmt = 'HHI%ds' % str_len
#     packed_packet = struct.pack(fmt, self.checksum, self.length, self.seqno, encoded_data)
#     return packed_packet

def calc_checksum(data, type='str'):
    encoded_data = data
    if type is not 'bytes':
        encoded_data = data.encode()
    i = 0
    checksum = 0
    while i < len(encoded_data):
        short1 = 0
        short1 = encoded_data[i]
        if (i + 1) < len(encoded_data):
            short1 += (encoded_data[i + 1] << 8)
        checksum += short1
        if (checksum & 0x10000) > 0:
            checksum = (checksum + 1) & 0xFFFF
        i += 2
    return ~checksum & 0xFFFF
