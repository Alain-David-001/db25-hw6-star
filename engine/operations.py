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
