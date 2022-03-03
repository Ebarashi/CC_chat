import random


# Packet Loss Simulation class

def lose_packet(p):
    generated_num = random.uniform(0, 1.0)
    return generated_num < p

# testing

# yes = 0
# no = 0
# max_range = 10000000
# for i in range(0,max_range) :
# 	if (lose_packet(0.001) == True) :
# 		yes = yes + 1
# 	else :
# 		no = no + 1
# print ("Yes:\t", yes/max_range)
# print ("No:\t", no/max_range)
