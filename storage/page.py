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
        if offset == -1:
            raise ValueError("Attempted to access deleted slot.")
        # Find length: use next slot or page end
        next_offset = self.slots[slot_idx - 1] if slot_idx > 0 else PAGE_SIZE
        tuple_data = self.data[offset:next_offset]
        return schema.deserialize(tuple_data)

    def serialize(self):
        # Build metadata (number of slots and free offset)
        meta = bytearray()
        meta += len(self.slots).to_bytes(4, 'little')
        meta += self.free_offset.to_bytes(4, 'little')

        # Build slot directory
        slot_dir = bytearray()
        for offset in self.slots:
            slot_dir += offset.to_bytes(4, 'little', signed=True)  # use signed=True to allow -1

        # Extract the tuple area (actual serialized data)
        tuple_area = self.data[self.free_offset:]

        # Assemble full page
        full_page = bytearray(PAGE_SIZE)
        full_page[0:len(meta)] = meta
        full_page[len(meta):len(meta) + len(slot_dir)] = slot_dir
        full_page[self.free_offset:] = tuple_area

        return full_page

    def load(self, raw):
        self.slots = []
        num_slots = int.from_bytes(raw[0:4], 'little')
        self.free_offset = int.from_bytes(raw[4:8], 'little')
        for i in range(num_slots):
            off = int.from_bytes(raw[8+i*4:12+i*4], 'little', signed=True)
            self.slots.append(off)
        self.data = bytearray(raw)
