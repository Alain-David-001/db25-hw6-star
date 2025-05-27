from sql_parser.sql_parser import parse
from engine.executor import execute_command
from storage.catalog import Catalog
from storage.file_manager import FileManager

def main():
    catalog = Catalog("data/catalog.json")
    file_manager = FileManager("data/database.db")

    print("Welcome to db25-hw6-star!")
    print("Enter SQL commands ending with semicolon (;). Type 'exit;' to quit.")

    try:
        buffer = ""
        while True:
            line = input("> ").strip()
            if not line:
                continue
            buffer += " " + line
            if buffer.strip().endswith(";"):
                command_text = buffer.strip()
                buffer = ""
                if command_text.lower() == "exit;":
                    print("Goodbye!")
                    break
                try:
                    command = parse(command_text)
                    result = execute_command(command, catalog, file_manager)
                    if result is not None:
                        for row in result:
                            print(row)
                except Exception as e:
                    print(f"[Error] {e}")
    finally:
        file_manager.close()

if __name__ == "__main__":
    main()
