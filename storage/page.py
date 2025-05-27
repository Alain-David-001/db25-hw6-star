PAGE_SIZE = 4096  # bytes

class Page:
    def __init__(self):
        self.data = bytearray(PAGE_SIZE)
        self.slots = []
        self.free_offset = PAGE_SIZE  # start from the end

    def insert_tuple(self, tuple_bytes):
        tuple_len = len(tuple_bytes)
        if self.free_offset - tuple_len < (len(self.slots) + 1) * 4 + 8:
            raise MemoryError("Not enough space in page")

        self.free_offset -= tuple_len
        self.data[self.free_offset:self.free_offset + tuple_len] = tuple_bytes
        self.slots.append(self.free_offset)

    def get_tuple(self, slot_idx, schema):
        offset = self.slots[slot_idx]
        # Find length: use next slot or page end
        next_offset = self.slots[slot_idx - 1] if slot_idx > 0 else PAGE_SIZE
        tuple_data = self.data[offset:next_offset]
        return schema.deserialize(tuple_data)

    def serialize(self):
        # Header: [num_slots (4), free_offset (4)]
        out = bytearray()
        out += len(self.slots).to_bytes(4, 'little')
        out += self.free_offset.to_bytes(4, 'little')
        for offset in self.slots:
            out += offset.to_bytes(4, 'little')
        out += self.data[self.free_offset:]
        return out

    def load(self, raw):
        self.slots = []
        num_slots = int.from_bytes(raw[0:4], 'little')
        self.free_offset = int.from_bytes(raw[4:8], 'little')
        for i in range(num_slots):
            off = int.from_bytes(raw[8+i*4:12+i*4], 'little')
            self.slots.append(off)
        self.data[self.free_offset:] = raw[8 + 4*num_slots:]
