from sql_parser.sql_parser import parse

def test_create_table():
    sql = "CREATE TABLE users (id INT, name STRING);"
    expected = {
        "op": "CREATE_TABLE",
        "table": "users",
        "columns": [("id", "INT"), ("name", "STRING")]
    }
    assert parse(sql) == expected

def test_insert():
    sql = "INSERT INTO users VALUES (1, 'Alice');"
    expected = {
        "op": "INSERT",
        "table": "users",
        "values": [1, "Alice"]
    }
    assert parse(sql) == expected

def test_select_all():
    sql = "SELECT * FROM users;"
    expected = {
        "op": "SELECT",
        "table": "users",
        "where": {}
    }
    assert parse(sql) == expected

def test_select_where():
    sql = "SELECT * FROM users WHERE id = 1;"
    expected = {
        "op": "SELECT",
        "table": "users",
        "where": {"id": 1}
    }
    assert parse(sql) == expected

def test_update():
    sql = "UPDATE users SET name = 'Bob' WHERE id = 1;"
    expected = {
        "op": "UPDATE",
        "table": "users",
        "set": {"name": "Bob"},
        "where": {"id": 1}
    }
    assert parse(sql) == expected

def test_delete():
    sql = "DELETE FROM users WHERE name = 'Bob';"
    expected = {
        "op": "DELETE",
        "table": "users",
        "where": {"name": "Bob"}
    }
    assert parse(sql) == expected
