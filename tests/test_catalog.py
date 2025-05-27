import os
import tempfile
from storage.catalog import Catalog

def test_create_and_load_catalog():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name

    try:
        # Create catalog
        cat = Catalog(catalog_file=path)
        assert cat.tables == {}

        # Create table
        columns = [('id', 'INT'), ('name', 'STRING')]
        cat.create_table("users", columns)

        # Add page
        cat.add_page("users", 0)
        cat.add_page("users", 1)

        # Check schema and pages
        assert cat.get_schema("users") == columns
        assert cat.get_pages("users") == [0, 1]

        # Reload and verify persistence
        cat2 = Catalog(catalog_file=path)
        assert cat2.get_schema("users") == columns
        assert cat2.get_pages("users") == [0, 1]

    finally:
        os.remove(path)
