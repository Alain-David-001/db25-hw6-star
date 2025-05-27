class TupleSchema:
    def __init__(self, columns):
        # columns: list of (name, type) pairs, e.g., [('id', 'INT'), ('name', 'STRING')]
        self.columns = columns

    def serialize(self, values):
        # Convert tuple values to bytes
        # For now: INT = 4 bytes, FLOAT = 8 bytes, STRING = len-prefixed utf-8
        data = b''
        for (name, col_type), value in zip(self.columns, values):
            if col_type == 'INT':
                data += int(value).to_bytes(4, byteorder='little', signed=True)
            elif col_type == 'FLOAT':
                import struct
                data += struct.pack('<d', float(value))
            elif col_type == 'STRING':
                encoded = value.encode('utf-8')
                data += len(encoded).to_bytes(2, byteorder='little') + encoded
            else:
                raise ValueError(f"Unsupported column type: {col_type}")
        return data

    def deserialize(self, data):
        # Convert bytes back to tuple values
        values = []
        i = 0
        for name, col_type in self.columns:
            if col_type == 'INT':
                values.append(int.from_bytes(data[i:i+4], byteorder='little', signed=True))
                i += 4
            elif col_type == 'FLOAT':
                import struct
                values.append(struct.unpack('<d', data[i:i+8])[0])
                i += 8
            elif col_type == 'STRING':
                length = int.from_bytes(data[i:i+2], byteorder='little')
                i += 2
                values.append(data[i:i+length].decode('utf-8'))
                i += length
            else:
                raise ValueError(f"Unsupported column type: {col_type}")
        return values
