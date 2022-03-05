import numpy as np
import file_handler as hand
import checksum


class PacketGen:
    CHUNK_SIZE = 500

    def __init__(self, file_name=None):
        self.init_seqno = 1
        self.next_seqno = self.init_seqno
        if not file_name is None:
            self.file_name = file_name
            self.file_is_reg = 1
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

    def gen_packet_from_file(self):
        if self.file_is_reg == 0:
            return None
        data_bytes = self.f_handler.get_next_chunk()
        if not data_bytes:
            return None
        packet = Packet(checksum.gen_cksum(checksum.string_to_byte_arr(data_bytes)), len(data_bytes) + 12,
                        self.next_seqno, data_bytes)
        self.next_seqno = self.next_seqno + 1
        return packet

class Packet:
    def __init__(self, cksum, len, seqno, data):
        self.cksum = np.uint16(cksum)
        self.len = np.uint16(len)
        self.seqno = np.uint32(seqno)
        self.data = data



