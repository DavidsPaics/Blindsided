import pygame, time, logging

def rleEncode(data):
    if not data:
        return ""
    
    if any(char.isdigit() for char in data):
        raise ValueError("Input string must not contain numbers.")

    encoded = []
    count = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded.append(f"{count}{data[i - 1]}")
            count = 1

    encoded.append(f"{count}{data[-1]}")
    return "".join(encoded)

def clamp(mi, x, mx):
    return min(mx, max(x, mi))

def mapValue(value, in_min, in_max, out_min, out_max):
    """
    Maps a value from one range to another.
    
    :param value: The input value to map.
    :param in_min: The lower bound of the input range.
    :param in_max: The upper bound of the input range.
    :param out_min: The lower bound of the output range.
    :param out_max: The upper bound of the output range.
    :return: The mapped value.
    """
    return out_min + ((value - in_min) * (out_max - out_min) / (in_max - in_min))

def rleDecode(encoded):
    if not encoded:
        return ""

    decoded = []
    count = ""

    for char in encoded:
        if char.isdigit():
            count += char
        else:
            decoded.append(char * int(count))
            count = ""

    return "".join(decoded)

def compressMapFile(path):
    with open(path) as f:
        data = f.load()
    with open(path.split(".")[:-1]+"-compressed.txt", "w+") as f:
        f.write("C\n")
        for line in data:
            f.write(rleEncode(line))
    
