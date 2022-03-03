import numpy as np


class Ack:
    def __init__(self, len, ackno):
        self.cksum = np.uint16(0)
        self.len = np.uint16(len)
        self.ackno = np.uint32(ackno)
