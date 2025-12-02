def convert_bin_to_hex(instruction, length_bits):
    return hex(int(instruction, 2))[2:].zfill(length_bits // 4)

def convert_hex_to_bin(value, bits):
    return bin(int(value, 16))[2:].zfill(bits)

def convert_int_to_bin(value, bits):
    return bin(value)[2:].zfill(bits)