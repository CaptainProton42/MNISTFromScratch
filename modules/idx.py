######################
#       idx.py       #
#--------------------#
#   Open idx files.  #
######################

import numpy as np
import struct

class file:
    def __init__(self, dtype, datashape=np.array([], dtype=">u4")):
        self.dtype = dtype
        self.datashape = np.array(datashape, dtype=">u4")
        self.empty = True

    def append(self, data):
        if self.empty:
            self.body = np.array(data, dtype=self.dtype)
            self.empty = False
        else:
            self.body = np.append(self.body, data, axis=0)

def write(path, idx_obj):
    idx_file = open(path, "wb+")

    dtype = 0
    fmt = ''
    if (idx_obj.dtype == ">u1"):
        dtype = 8
        fmt ='>B'
    elif (idx_obj.dtype == ">i1"):
        dtype = 9
        fmt ='>b'
    elif (idx_obj.dtype == ">i2"):
        dtype = 11
        fmt ='>h'
    elif (idx_obj.dtype == ">i4"):
        dtype = 12
        fmt='>i'
    elif (idx_obj.dtype == ">f4"):
        dtype = 13
        fmt='>f'
    elif (idx_obj.dtype == ">f8"):
        dtype = 14
        fmt='>d'
    else:
        raise ValueError('Unknown datatype. Note that only big-endian datatypes are allowed.')

    dims = len(idx_obj.datashape) + 1
    shape = np.array([len(idx_obj.body)], dtype=">u4")
    shape = np.append(shape, idx_obj.datashape, axis=0)

    bytes_written = 0

    magic_number = bytes([0,
                          0, 
                          dtype,
                          dims])

    bytes_written += idx_file.write(magic_number)

    for i in range(dims):
        bytes_written += idx_file.write(struct.pack(">I", shape[i]))

    for index in idx_obj.body:
        for element in np.nditer(index):
            bytes_written += idx_file.write(struct.pack(fmt, element))

    expected_bytes_written = 4 + dims * 4 + idx_obj.body.size * idx_obj.body.itemsize

    if not bytes_written == expected_bytes_written:
        print("Error writing to file! (%i, %i)" % (bytes_written, expected_bytes_written))

def read(path):
    idx_file = open(path, "rb")
    magic_number = idx_file.read(4) # first 4 bytes

    # Magic number:
    # Bytes 0-1: always 0
    # Byte 2: datatype
    # Byte 3: dimensions of data
    
    dims = magic_number[3]

    dtype = 0
    if (magic_number[2] == 8):
        dtype = ">u1"
    elif (magic_number[2] == 9):
        dtype = ">i1"
    elif (magic_number[2] == 11):
        dtype = ">i2"
    elif (magic_number[2] == 12):
        dtype = ">i4"
    elif (magic_number[2] == 13):
        dtype = ">f4"
    elif (magic_number[2] == 14):
        dtype = ">f8" 
    else:
        raise ValueError('Unknown datatype. Note that only big-endian datatypes are allowed.')

    shape = np.fromfile(idx_file, dtype=">u4", count=dims)

    data_arr = np.fromfile(idx_file, dtype=dtype)
    data_arr = np.reshape(data_arr, shape)

    idx_obj = file(dtype=dtype, datashape=shape[1:])
    idx_obj.body = data_arr
    return idx_obj