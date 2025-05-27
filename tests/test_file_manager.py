import os
import tempfile
from storage.file_manager import FileManager, PAGE_SIZE

def test_allocate_and_write_read_page():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name

    try:
        fm = FileManager(path)

        # Allocate a new page
        page_id = fm.allocate_page()
        assert page_id == 0

        # Write to it
        data = b'A' * PAGE_SIZE
        fm.write_page(page_id, data)

        # Read it back
        result = fm.read_page(page_id)
        assert result == data

        # Write and read another page
        page_id2 = fm.allocate_page()
        fm.write_page(page_id2, b'B' * PAGE_SIZE)
        assert fm.read_page(page_id2) == b'B' * PAGE_SIZE

        fm.close()
    finally:
        os.remove(path)
