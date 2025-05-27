import os
import tempfile
from engine.executor import execute_command
from storage.catalog import Catalog
from storage.file_manager import FileManager
from storage.tuple import TupleSchema
from storage.page import Page, PAGE_SIZE

def test_create_and_insert():
    with tempfile.NamedTemporaryFile(delete=False) as tmp_db, tempfile.NamedTemporaryFile(delete=False) as tmp_cat:
        db_path = tmp_db.name
        cat_path = tmp_cat.name

    try:
        catalog = Catalog(catalog_file=cat_path)
        file_manager = FileManager(db_path)

        # Create table
        create_cmd = {
            "op": "CREATE_TABLE",
            "table": "users",
            "columns": [("id", "INT"), ("name", "STRING")]
        }
        execute_command(create_cmd, catalog, file_manager)

        # Insert row
        insert_cmd = {
            "op": "INSERT",
            "table": "users",
            "values": [1, "Alice"]
        }
        execute_command(insert_cmd, catalog, file_manager)

        # Check catalog and file
        pages = catalog.get_pages("users")
        assert len(pages) == 1

        page_id = pages[0]
        raw = file_manager.read_page(page_id)
        page = Page()
        page.load(raw)

        schema = TupleSchema(catalog.get_schema("users"))
        result = page.get_tuple(0, schema)

        assert result == [1, "Alice"]

    finally:
        file_manager.close()
        os.remove(db_path)
        os.remove(cat_path)
