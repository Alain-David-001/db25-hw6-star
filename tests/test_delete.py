import os
import tempfile
from engine.executor import execute_command
from storage.catalog import Catalog
from storage.file_manager import FileManager

def test_delete_with_where():
    with tempfile.NamedTemporaryFile(delete=False) as tmp_db, tempfile.NamedTemporaryFile(delete=False) as tmp_cat:
        db_path = tmp_db.name
        cat_path = tmp_cat.name

    try:
        catalog = Catalog(catalog_file=cat_path)
        file_manager = FileManager(db_path)

        execute_command({
            "op": "CREATE_TABLE",
            "table": "people",
            "columns": [("id", "INT"), ("name", "STRING")]
        }, catalog, file_manager)

        execute_command({"op": "INSERT", "table": "people", "values": [1, "Alice"]}, catalog, file_manager)
        execute_command({"op": "INSERT", "table": "people", "values": [2, "Bob"]}, catalog, file_manager)
        execute_command({"op": "INSERT", "table": "people", "values": [3, "Alice"]}, catalog, file_manager)

        # Delete one row
        execute_command({
            "op": "DELETE",
            "table": "people",
            "where": {"id": 2}
        }, catalog, file_manager)

        # Validate Bob is gone, others remain
        results = execute_command({"op": "SELECT", "table": "people"}, catalog, file_manager)
        assert [2, "Bob"] not in results
        assert [1, "Alice"] in results
        assert [3, "Alice"] in results

        # Delete all rows
        execute_command({
            "op": "DELETE",
            "table": "people",
            "where": {"name": "Alice"}
        }, catalog, file_manager)

        results = execute_command({"op": "SELECT", "table": "people"}, catalog, file_manager)
        assert results == []

    finally:
        file_manager.close()
        os.remove(db_path)
        os.remove(cat_path)
