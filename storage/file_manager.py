import os

PAGE_SIZE = 4096

class FileManager:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.fd = open(db_path, 'r+b') if os.path.exists(db_path) else open(db_path, 'w+b')  # This opens for read/write without forced append behavior.

    def close(self):
        self.fd.close()

    def read_page(self, page_id):
        self.fd.seek(page_id * PAGE_SIZE)
        return self.fd.read(PAGE_SIZE)

    def write_page(self, page_id, data):
        if len(data) != PAGE_SIZE:
            raise ValueError("Page data must be exactly 4096 bytes")
        self.fd.seek(page_id * PAGE_SIZE)
        self.fd.write(data)
        self.fd.flush()

    def allocate_page(self):
        self.fd.seek(0, os.SEEK_END)
        end = self.fd.tell()
        new_page_id = end // PAGE_SIZE
        self.fd.write(b'\x00' * PAGE_SIZE)  # zero-filled new page
        self.fd.flush()
        return new_page_id
