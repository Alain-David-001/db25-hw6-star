import json
import os

class Catalog:
    def __init__(self, catalog_file="data/catalog.json"):
        self.catalog_file = catalog_file
        if os.path.exists(catalog_file) and os.path.getsize(catalog_file) > 0:
            with open(catalog_file, 'r') as f:
                self.tables = json.load(f)
        else:
            self.tables = {}

    def save(self):
        with open(self.catalog_file, 'w') as f:
            json.dump(self.tables, f, indent=2)

    def create_table(self, table_name, columns):
        if table_name in self.tables:
            raise Exception(f"Table '{table_name}' already exists.")
        self.tables[table_name] = {
            "columns": columns,  # list of (name, type)
            "pages": []          # will store page IDs
        }
        self.save()

    def get_schema(self, table_name):
        table = self.tables.get(table_name)
        if not table:
            raise Exception(f"Table '{table_name}' not found.")
        return [tuple(col) for col in table["columns"]]

    def add_page(self, table_name, page_id):
        if table_name not in self.tables:
            raise Exception(f"Table '{table_name}' not found.")
        self.tables[table_name]["pages"].append(page_id)
        self.save()

    def get_pages(self, table_name):
        table = self.tables.get(table_name)
        if not table:
            raise Exception(f"Table '{table_name}' not found.")
        return table["pages"]
