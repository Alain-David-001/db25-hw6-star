from storage.page import Page
from storage.file_manager import PAGE_SIZE

def insert_into_table(table_name, values, schema, catalog, file_manager):
    pages = catalog.get_pages(table_name)
    tuple_data = schema.serialize(values)

    for page_id in pages:
        raw = file_manager.read_page(page_id)
        page = Page()
        page.load(raw)
        try:
            page.insert_tuple(tuple_data)
            file_manager.write_page(page_id, page.serialize())
            return
        except MemoryError:
            continue

    # No space, allocate new page
    new_page_id = file_manager.allocate_page()
    page = Page()
    page.insert_tuple(tuple_data)
    file_manager.write_page(new_page_id, page.serialize())
    catalog.add_page(table_name, new_page_id)

def select_from_table(table_name, where, schema, catalog, file_manager):
    results = []
    pages = catalog.get_pages(table_name)

    for page_id in pages:
        raw = file_manager.read_page(page_id)
        page = Page()
        page.load(raw)

        for i in range(len(page.slots)):
            tup = page.get_tuple(i, schema)
            if _matches_where(tup, schema, where):
                results.append(tup)

    return results

def _matches_where(tup, schema, where):
    if not where:
        return True
    column_names = [col[0] for col in schema.columns]
    for key, val in where.items():
        if key not in column_names:
            raise KeyError(f"Column '{key}' does not exist in table schema.")
        idx = column_names.index(key)
        if tup[idx] != val:
            return False
    return True
