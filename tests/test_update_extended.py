import os
import tempfile
from engine.executor import execute_command
from storage.catalog import Catalog
from storage.file_manager import FileManager
import pytest

def test_update_reallocates_in_same_page():
    with tempfile.NamedTemporaryFile(delete=False) as tmp_db, tempfile.NamedTemporaryFile(delete=False) as tmp_cat:
        db_path = tmp_db.name
        cat_path = tmp_cat.name

    try:
        catalog = Catalog(catalog_file=cat_path)
        file_manager = FileManager(db_path)

        execute_command({
            "op": "CREATE_TABLE",
            "table": "test",
            "columns": [("id", "INT"), ("desc", "STRING")]
        }, catalog, file_manager)

        execute_command({"op": "INSERT", "table": "test", "values": [1, "abc"]}, catalog, file_manager)

        # Update with larger string (should cause tuple to move within same page)
        execute_command({
            "op": "UPDATE",
            "table": "test",
            "where": {"id": 1},
            "set": {"desc": "abcdefghij"}  # longer than "abc"
        }, catalog, file_manager)

        results = execute_command({"op": "SELECT", "table": "test"}, catalog, file_manager)
        assert results == [[1, "abcdefghij"]]

    finally:
        file_manager.close()
        os.remove(db_path)
        os.remove(cat_path)

def test_update_requires_new_page():
    with tempfile.NamedTemporaryFile(delete=False) as tmp_db, tempfile.NamedTemporaryFile(delete=False) as tmp_cat:
        db_path = tmp_db.name
        cat_path = tmp_cat.name

    try:
        catalog = Catalog(catalog_file=cat_path)
        file_manager = FileManager(db_path)

        execute_command({
            "op": "CREATE_TABLE",
            "table": "test",
            "columns": [("id", "INT"), ("desc", "STRING")]
        }, catalog, file_manager)

        # Fill a page almost completely
        for i in range(25):  # each tuple is small
            execute_command({"op": "INSERT", "table": "test", "values": [i, "x" * 10]}, catalog, file_manager)

        # This update should cause tuple to move to a new page
        execute_command({
            "op": "UPDATE",
            "table": "test",
            "where": {"id": 0},
            "set": {"desc": "y" * 400}  # very long value
        }, catalog, file_manager)

        results = execute_command({"op": "SELECT", "table": "test", "where": {"id": 0}}, catalog, file_manager)
        assert results == [[0, "y" * 400]]

    finally:
        file_manager.close()
        os.remove(db_path)
        os.remove(cat_path)
