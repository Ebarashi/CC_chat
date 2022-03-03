import math


# Hello = "He" "ll" "o"
# ABCD = "AB" "CD"


def string_to_byte_arr(s):
    binary_s = ' '.join(format(ord(x), 'b').zfill(8) for x in s)  # convert each string to a binary byte in place
    byte_array = binary_s.split()  # split the binary bytes string into a array
    return byte_array


# 16-bit internet checksum using array of bytes
def gen_cksum(byte_array):
    byte_array_pairs = [None] * (math.ceil(len(byte_array) / 2))
    j = 0
    for i in range(0, len(byte_array), 2):
        if (i + 1) < len(byte_array):
            byte_array_pairs[j] = byte_array[i] + byte_array[i + 1]
        else:
            byte_array_pairs[j] = byte_array[i] + "00000000"
        j = j + 1
    # now each two consecutive binary bytes were concatenated into one 16-bit binary string

    total_sum = 0  # initially
    for i in range(0, len(byte_array_pairs)):  # for each 16-bit binary string
        _16_bit_str = int(byte_array_pairs[i], 2)
        total_sum = total_sum + _16_bit_str  # add the string to the total_sum
        if total_sum > 65535:  # if a carry occurs (total_sum is now 17-bits long)
            # truncate the single bit in the carry and add it to the sum (wrap it)
            total_sum = total_sum - 65536
            total_sum = total_sum + 1
    total_sum = total_sum ^ 65535  # perform 1-compliment to the total_sum using xor
    return total_sum

# print (gen_cksum(string_to_byte_arr("Hello")))
# print (gen_cksum(string_to_byte_arr("\x48\x65\x6C\x6C\x6F")))
