from engine.operations import insert_into_table, select_from_table, update_table, delete_from_table
from storage.tuple import TupleSchema
from storage.catalog import Catalog

def execute_command(command, catalog: Catalog, file_manager):
    op = command["op"]

    if op == "CREATE_TABLE":
        table = command["table"]
        columns = command["columns"]
        catalog.create_table(table, columns)

    elif op == "INSERT":
        table = command["table"]
        values = command["values"]
        schema = TupleSchema(catalog.get_schema(table))
        insert_into_table(table, values, schema, catalog, file_manager)

    elif op == "SELECT":
        table = command["table"]
        where = command.get("where", {})
        schema = TupleSchema(catalog.get_schema(table))
        return select_from_table(table, where, schema, catalog, file_manager)

    elif op == "UPDATE":
        table = command["table"]
        where = command.get("where", {})
        set_values = command.get("set", {})
        schema = TupleSchema(catalog.get_schema(table))
        update_table(table, where, set_values, schema, catalog, file_manager)

    elif op == "DELETE":
        table = command["table"]
        where = command.get("where", {})
        schema = TupleSchema(catalog.get_schema(table))
        delete_from_table(table, where, schema, catalog, file_manager)

    else:
        raise NotImplementedError(f"Unsupported command: {op}")
