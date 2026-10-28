# Library Management System

A web-based system for managing library books, students, and borrowing activity,
built with Python, Streamlit, and SQLite.

## Features

- Manager login
- Dashboard with live statistics (copies, titles, students, issued, returned, overdue)
- Add, search, update, and delete books
- Register, search, update, and delete students
- Issue books to students and record returns
- Overdue tracking with an estimated fine (₹5 per day)
- Reports with charts (copies by category, issued vs returned) and full borrowing history

## Technology Used

- Python 3
- Streamlit (user interface)
- SQLite (database, created automatically as `library.db`)
- pandas and Plotly (tables and charts)
- Git and GitHub

## Project Structure

| File | Purpose |
| --- | --- |
| `main.py` | Streamlit user interface (all pages) |
| `database.py` | All database logic (tables, queries, issue/return rules) |
| `test_database.py` | Automated tests for `database.py` |
| `requirements.txt` | Python dependencies |

## How to Run

```bash
pip install -r requirements.txt
streamlit run main.py
```

Then open http://localhost:8501 and sign in.

Demo login: **admin** / **library123**
(Change these in `main.py`, or set the `LIBRARY_ADMIN_USER` and
`LIBRARY_ADMIN_PASSWORD` environment variables.)

## How Book Copies Work

The *Available Copies* number on a book is how many copies are on the shelf right now.
Issuing a book lowers it by one and returning a book raises it by one. On the dashboard,
*Book Copies* is the total the library owns (on the shelf plus currently issued).

## Running the Tests

```bash
python test_database.py
```

The tests use a temporary database, so your real data is never touched.

## Project Team

Developed by a team of 7 students.
