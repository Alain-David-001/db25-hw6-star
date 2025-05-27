# db25-hw6-star

A fully functional, persistent, file-based DBMS built for the Spring 2025 Databases course (DB25).  
It supports typed columns, basic SQL commands, slotted-page storage, and a command-line REPL interface.

> **HW6\*** — Bonus multiplier: **5**

---

## 📌 Features

- Multiple named tables with typed columns (`STRING`, `INT`, `FLOAT`)
- SQL-like operations:
  - `CREATE TABLE`
  - `INSERT INTO ... VALUES`
  - `SELECT * FROM ... WHERE`
  - `UPDATE ... SET ... WHERE`
  - `DELETE FROM ... WHERE`
- Persistent catalog and data files across runs
- Slotted-page layout with logical deletion and in-place or relocated updates
- No indexing — uses full scans with exact-match filtering
- Minimal SQL parser to convert SQL strings into executable commands
- REPL interface with multi-line input and error handling

---

## 📁 Project Structure

```
db25-hw6-star/
├── main.py                 # Entry point with REPL
├── storage/                # Core storage logic
│   ├── catalog.py
│   ├── file_manager.py
│   ├── page.py
│   └── tuple.py
├── engine/                 # Command execution logic
│   ├── executor.py
│   └── operations.py
├── sql_parser/             # SQL-to-dict parser
│   ├── __init__.py
│   └── sql_parser.py
├── tests/                  # pytest-based test suite
│   ├── test_*.py
├── data/                   # Auto-created during runtime
│   ├── catalog.json
│   └── database.db
├── .gitignore
└── README.md
```

---

## 🔧 How to Run

```bash
git clone https://github.com/Alain-David-001/db25-hw6-star.git
cd db25-hw6-star
python main.py
```

---

## ▶️ Example Usage

Here’s an example REPL session demonstrating all core features:

```sql
Welcome to db25-hw6-star!
Enter SQL commands ending with semicolon (;). Type 'exit;' to quit.
> CREATE TABLE users (id INT, name STRING);
> INSERT INTO users VALUES (1, 'Alice');
> INSERT INTO users VALUES (2, 'Bob');
> INSERT INTO users VALUES (3, 'Alice');
> SELECT * FROM users;
[1, 'Alice']
[2, 'Bob']
[3, 'Alice']
> SELECT * FROM users WHERE name = 'Alice';
[1, 'Alice']
[3, 'Alice']
> UPDATE users SET name = 'Alicia' WHERE id = 1;
> SELECT * FROM users;
[2, 'Bob']
[3, 'Alice']
[1, 'Alicia']
> DELETE FROM users WHERE name = 'Alice';
> SELECT * FROM users;
[2, 'Bob']
[1, 'Alicia']
> exit;
Goodbye!
```

All data is persisted to disk — restarting the program will keep your tables and data intact.

---

## 🧪 Testing

Run all test cases using:

```bash
pytest
```

Covers all core features, full workflows, and error handling.

---

## 🧠 Notes

- Uses slotted pages with logical deletes (`slot = -1`)
- Updates that grow a tuple may reinsert it elsewhere
- Parser supports basic syntax (e.g., no subqueries or joins)
- No automatic vacuuming or page compaction (yet)

---

## 🧑‍💻 Author

**Alain David Escarrá García**  
2nd-year Software, Data, and Technology student  
Constructor University, Spring 2025

