import os
import tempfile
from engine.executor import execute_command
from storage.catalog import Catalog
from storage.file_manager import FileManager

def test_full_flow():
    with tempfile.NamedTemporaryFile(delete=False) as tmp_db, tempfile.NamedTemporaryFile(delete=False) as tmp_cat:
        db_path = tmp_db.name
        cat_path = tmp_cat.name

    try:
        catalog = Catalog(catalog_file=cat_path)
        file_manager = FileManager(db_path)

        # CREATE TABLE
        execute_command({
            "op": "CREATE_TABLE",
            "table": "users",
            "columns": [("id", "INT"), ("name", "STRING")]
        }, catalog, file_manager)

        # INSERT
        for i, name in [(1, "Alice"), (2, "Bob"), (3, "Charlie"), (4, "Alice")]:
            execute_command({"op": "INSERT", "table": "users", "values": [i, name]}, catalog, file_manager)

        # SELECT ALL
        all_rows = execute_command({"op": "SELECT", "table": "users"}, catalog, file_manager)
        assert len(all_rows) == 4

        # SELECT WHERE
        alices = execute_command({
            "op": "SELECT",
            "table": "users",
            "where": {"name": "Alice"}
        }, catalog, file_manager)
        assert len(alices) == 2

        # UPDATE
        execute_command({
            "op": "UPDATE",
            "table": "users",
            "where": {"id": 3},
            "set": {"name": "Carlos"}
        }, catalog, file_manager)

        results = execute_command({
            "op": "SELECT",
            "table": "users",
            "where": {"id": 3}
        }, catalog, file_manager)
        assert results == [[3, "Carlos"]]

        # DELETE
        execute_command({
            "op": "DELETE",
            "table": "users",
            "where": {"name": "Alice"}
        }, catalog, file_manager)

        remaining = execute_command({"op": "SELECT", "table": "users"}, catalog, file_manager)
        assert [1, "Alice"] not in remaining
        assert [4, "Alice"] not in remaining
        assert [2, "Bob"] in remaining
        assert [3, "Carlos"] in remaining

    finally:
        file_manager.close()
        os.remove(db_path)
        os.remove(cat_path)
