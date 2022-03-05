import random


# Packet Loss Simulation class

def lose_packet(p):
    generated_num = random.uniform(0, 1.0)
    return generated_num < p
