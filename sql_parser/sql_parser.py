import re

def parse(sql: str) -> dict:
    sql = sql.strip().rstrip(";").strip()
    sql_upper = sql.upper()

    if sql_upper.startswith("CREATE TABLE"):
        return _parse_create(sql)
    elif sql_upper.startswith("INSERT INTO"):
        return _parse_insert(sql)
    elif sql_upper.startswith("SELECT"):
        return _parse_select(sql)
    elif sql_upper.startswith("UPDATE"):
        return _parse_update(sql)
    elif sql_upper.startswith("DELETE FROM"):
        return _parse_delete(sql)
    else:
        raise ValueError("Unsupported SQL command")

def _parse_create(sql):
    match = re.match(r"CREATE TABLE (\w+)\s*\((.+)\)", sql, re.IGNORECASE)
    table, cols = match.groups()
    columns = []
    for part in cols.split(","):
        name, typ = part.strip().split()
        columns.append((name, typ.upper()))
    return {"op": "CREATE_TABLE", "table": table, "columns": columns}

def _parse_insert(sql):
    match = re.match(r"INSERT INTO (\w+)\s*VALUES\s*\((.+)\)", sql, re.IGNORECASE)
    table, values = match.groups()
    parsed_values = [eval(val.strip()) for val in values.split(",")]
    return {"op": "INSERT", "table": table, "values": parsed_values}

def _parse_select(sql):
    where = {}
    match = re.match(r"SELECT \* FROM (\w+)(?: WHERE (.+))?", sql, re.IGNORECASE)
    table, where_clause = match.groups()
    if where_clause:
        k, v = map(str.strip, where_clause.split("="))
        where[k] = eval(v)
    return {"op": "SELECT", "table": table, "where": where}

def _parse_update(sql):
    match = re.match(r"UPDATE (\w+)\s+SET (.+?) WHERE (.+)", sql, re.IGNORECASE)
    table, set_clause, where_clause = match.groups()
    set_part = {}
    for assign in set_clause.split(","):
        k, v = map(str.strip, assign.split("="))
        set_part[k] = eval(v)
    k, v = map(str.strip, where_clause.split("="))
    where = {k: eval(v)}
    return {"op": "UPDATE", "table": table, "set": set_part, "where": where}

def _parse_delete(sql):
    match = re.match(r"DELETE FROM (\w+)\s+WHERE (.+)", sql, re.IGNORECASE)
    table, where_clause = match.groups()
    k, v = map(str.strip, where_clause.split("="))
    where = {k: eval(v)}
    return {"op": "DELETE", "table": table, "where": where}
