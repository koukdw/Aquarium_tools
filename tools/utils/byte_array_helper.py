import struct

class ByteArrayHelper:
    def __init__(self):
        self.data = bytearray()
        self.offset = 0

    # Data management methods
    def set_data(self, new_data):
        self.data = bytearray(new_data)
        self.offset = 0

    def get_data(self):
        return bytes(self.data)

    # Navigation methods
    def seek(self, offset, whence=0):
        if whence == 0:  # absolute
            self.offset = offset
        elif whence == 1:  # relative
            self.offset += offset
        elif whence == 2:  # relative to the end
            self.offset = len(self.data) + offset

    def tell(self):
        return self.offset

    # Read methods
    def read(self, size):
        result = self.data[self.offset:self.offset + size]
        self.offset += size
        return result

    def read_u8(self):
        result = self.data[self.offset]
        self.offset += 1
        return result

    def read_i8(self):
        result = struct.unpack_from('<b', self.data, self.offset)[0]
        self.offset += 1
        return result

    def read_u16(self):
        result = struct.unpack_from('<H', self.data, self.offset)[0]
        self.offset += 2
        return result

    def read_i16(self):
        result = struct.unpack_from('<h', self.data, self.offset)[0]
        self.offset += 2
        return result

    def read_u32(self):
        result = struct.unpack_from('<I', self.data, self.offset)[0]
        self.offset += 4
        return result

    def read_i32(self):
        result = struct.unpack_from('<i', self.data, self.offset)[0]
        self.offset += 4
        return result

    def read_u64(self):
        result = struct.unpack_from('<Q', self.data, self.offset)[0]
        self.offset += 8
        return result

    def read_i64(self):
        result = struct.unpack_from('<q', self.data, self.offset)[0]
        self.offset += 8
        return result

    def read_len_prefixed_nt_str(self, encoding='utf-8'):
        length = self.read_u32() - 1
        result = self.read(length).decode(encoding)
        self.offset += 1  # skip null terminator
        return result

    def read_nt_str(self, encoding='utf-8'):
        end = self.data.index(b'\x00', self.offset)
        result = self.data[self.offset:end].decode(encoding)
        self.offset = end + 1  # skip null terminator
        return result

    # Write methods
    def write_u8(self, value):
        self.data.extend(struct.pack('<B', value))

    def write_i8(self, value):
        self.data.extend(struct.pack('<b', value))

    def write_u16(self, value):
        self.data.extend(struct.pack('<H', value))

    def write_i16(self, value):
        self.data.extend(struct.pack('<h', value))

    def write_u32(self, value):
        self.data.extend(struct.pack('<I', value))

    def write_i32(self, value):
        self.data.extend(struct.pack('<i', value))

    def write_u64(self, value):
        self.data.extend(struct.pack('<Q', value))

    def write_i64(self, value):
        self.data.extend(struct.pack('<q', value))

    def write_len_prefixed_nt_str(self, value, encoding='utf-8'):
        encoded = value.encode(encoding)
        length = len(encoded) + 1  # Include null terminator in length
        self.write_u32(length)
        self.data.extend(encoded)
        self.data.extend(b'\x00')  # Null terminator

    def write_nt_str(self, value, encoding='utf-8'):
        encoded = value.encode(encoding)
        self.data.extend(encoded)
        self.data.extend(b'\x00')  # Null terminator