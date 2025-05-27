import os
import tempfile
from engine.executor import execute_command
from storage.catalog import Catalog
from storage.file_manager import FileManager

def test_update_with_where():
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
        execute_command({"op": "INSERT", "table": "people", "values": [2, "Bonifacio"]}, catalog, file_manager)

        # Update Bonifacio's name to Charlie
        execute_command({
            "op": "UPDATE",
            "table": "people",
            "where": {"id": 2},
            "set": {"name": "Charlie"}
        }, catalog, file_manager)

        # Confirm update
        results = execute_command({"op": "SELECT", "table": "people"}, catalog, file_manager)
        assert [2, "Charlie"] in results
        assert [2, "Bonifacio"] not in results

    finally:
        file_manager.close()
        os.remove(db_path)
        os.remove(cat_path)
