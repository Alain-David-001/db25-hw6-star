import os
import tempfile
import pytest
from engine.executor import execute_command
from storage.catalog import Catalog
from storage.file_manager import FileManager

def test_select_with_and_without_where():
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

        # SELECT without WHERE
        results_all = execute_command({"op": "SELECT", "table": "people"}, catalog, file_manager)
        assert len(results_all) == 3
        assert [1, "Alice"] in results_all
        assert [2, "Bob"] in results_all
        assert [3, "Alice"] in results_all

        # SELECT with WHERE
        results_filtered = execute_command({
            "op": "SELECT",
            "table": "people",
            "where": {"name": "Alice"}
        }, catalog, file_manager)
        assert len(results_filtered) == 2
        assert all(row[1] == "Alice" for row in results_filtered)

    finally:
        file_manager.close()
        os.remove(db_path)
        os.remove(cat_path)

def test_select_with_invalid_column_raises():
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

        # Try selecting with a non-existent column in WHERE
        with pytest.raises(KeyError, match="Column 'no_such_column' does not exist"):
            execute_command({
                "op": "SELECT",
                "table": "people",
                "where": {"no_such_column": "whatever"}
            }, catalog, file_manager)

    finally:
        file_manager.close()
        os.remove(db_path)
        os.remove(cat_path)
