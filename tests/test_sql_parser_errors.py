import pytest
from sql_parser.sql_parser import parse

@pytest.mark.parametrize("bad_sql", [
    "",  # empty
    "CREAT TABLE users (id INT)",  # misspelled CREATE
    "INSERT INTO users 1, 'Bob'",  # missing VALUES
    "UPDATE users SET name = 'Bob'",  # missing WHERE
    "DELETE FROM WHERE name = 'Bob'",  # missing table name
    "SELECT * users",  # missing FROM
    "UPDATE users name = 'Bob' WHERE id = 1",  # missing SET
    "CREATE TABLE users id INT, name STRING",  # missing parentheses
    "INSERT INTO users VALUES ()",  # empty tuple
])
def test_invalid_sql_raises(bad_sql):
    with pytest.raises((ValueError, AttributeError, SyntaxError, TypeError)):
        parse(bad_sql)
