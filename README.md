# db25-hw6-star

A simple file-based DBMS project built for the Spring 2025 Databases course (DB25).  
This system supports basic SQL-like operations over multiple named tables with typed columns, tuple storage, and page-level organization.

> **HW6\*** — Bonus multiplier: **5**

---

## 📌 Features

- Supports multiple named tables
- Typed columns (`STRING`, `INT`, `FLOAT`, etc.)
- Operations:
  - `CREATE TABLE`
  - `INSERT`
  - `SELECT ... WHERE ...`
  - `UPDATE`
  - `DELETE`
- All data persisted to disk across structured pages/files
- Tuple storage using **slotted page** approach
- No indexing — uses full scans with exact-match filtering

---

## 📁 Project Structure

```
db25-hw6-star/
├── main.py                 # Entry point (CLI / REPL)
├── storage/
│   ├── file_manager.py     # File read/write logic
│   ├── page.py             # Page structure & serialization
│   ├── tuple.py            # Tuple layout and encoding
│   └── catalog.py          # Table schemas and metadata
├── parser/
│   └── sql_parser.py       # Simple SQL-like parser
├── engine/
│   ├── executor.py         # Executes parsed commands
│   └── operations.py       # SELECT/INSERT/UPDATE/DELETE logic
├── data/
│   └── database.db         # Data file (created at runtime)
└── README.md
```

---

## 🔧 How to Run

```bash
git clone https://github.com/Alain-David-001/db25-hw6-star.git
cd db25-hw6-star
python main.py
```

This starts a basic REPL interface for running commands like:

```sql
CREATE TABLE users (id INT, name STRING);
INSERT INTO users VALUES (1, 'Alice');
SELECT * FROM users WHERE id = 1;
```

---

## 📚 Related Topics

To fully understand the implementation, review these lecture topics:

- **Lecture 8** – Tuple layout, slotted pages
- **Lecture 9–10** – Typed column storage, page design
- **Lecture 7** – Heap files, page directories
- **Lecture 11** – Buffer management ideas (optional)
- **Lecture 4–5** – SQL basics

---

## 🧠 Notes

- All filtering uses **exact matches only**.
- The data file grows over time; no compaction yet.
- The parser is minimal — only basic valid syntax is supported.

---

## 🧑‍💻 Author

Alain David Escarrá García
2nd-year Software, Data, and Technology student @ Constructor University

---

## 📅 Deadline

**May 28, 2025**
