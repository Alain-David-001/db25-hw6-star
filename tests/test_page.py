from storage.tuple import TupleSchema
from storage.page import Page

schema = TupleSchema([
    ('id', 'INT'),
    ('score', 'FLOAT'),
    ('name', 'STRING')
])

tuples = [
    (1, 98.6, 'Alice'),
    (2, 85.2, 'Bob'),
    (3, 72.0, 'Charlie')
]

def test_insert_and_retrieve():
    page = Page()
    for t in tuples:
        page.insert_tuple(schema.serialize(t))
    for i, expected in enumerate(tuples):
        actual = page.get_tuple(i, schema)
        assert actual == list(expected)

def test_serialization_roundtrip():
    page = Page()
    for t in tuples:
        page.insert_tuple(schema.serialize(t))
    raw = page.serialize()
    new_page = Page()
    new_page.load(raw)
    for i, expected in enumerate(tuples):
        actual = new_page.get_tuple(i, schema)
        assert actual == list(expected)
