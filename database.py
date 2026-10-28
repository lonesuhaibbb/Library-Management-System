import os
import sqlite3


# Always use the database that sits next to this file, no matter which folder
# the app is launched from (otherwise a new empty library.db can be created).
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")


def connect_db():
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    # Lets us read columns by name: row["title"] instead of row[1]
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = connect_db()
    cursor = connection.cursor()

    # NOTE: `quantity` is the number of copies currently AVAILABLE on the shelf.
    # It goes down when a book is issued and up when it is returned.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            isbn TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1
                CHECK (quantity >= 0)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            isbn TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT NOT NULL DEFAULT 'Issued'
                CHECK (status IN ('Issued', 'Returned')),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (isbn) REFERENCES books(isbn)
        )
    """)

    connection.commit()
    connection.close()


# ---------------------------------------------------------------- books ----

def add_book(isbn, title, author, category, quantity):
    connection = connect_db()

    try:
        connection.execute("""
            INSERT INTO books (isbn, title, author, category, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (isbn, title, author, category, quantity))

        connection.commit()
        return True, "Book added successfully!"

    except sqlite3.IntegrityError:
        return False, "A book with this ISBN already exists."

    finally:
        connection.close()


def get_books():
    connection = connect_db()

    try:
        return connection.execute("""
            SELECT isbn, title, author, category, quantity
            FROM books
            ORDER BY title
        """).fetchall()

    finally:
        connection.close()


def update_book(isbn, title, author, category, quantity):
    connection = connect_db()

    try:
        cursor = connection.execute("""
            UPDATE books
            SET title = ?, author = ?, category = ?, quantity = ?
            WHERE isbn = ?
        """, (title, author, category, quantity, isbn))

        connection.commit()
        return cursor.rowcount > 0, (
            "Book updated successfully!"
            if cursor.rowcount > 0 else "Book not found."
        )

    finally:
        connection.close()


def delete_book(isbn):
    connection = connect_db()

    try:
        cursor = connection.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        connection.commit()

        if cursor.rowcount == 0:
            return False, "Book not found."
        return True, "Book deleted successfully!"

    except sqlite3.IntegrityError:
        return False, "Cannot delete this book because it has transaction records."

    finally:
        connection.close()


# ------------------------------------------------------------- students ----

def add_student(student_id, name, department, phone="", email=""):
    connection = connect_db()

    try:
        connection.execute("""
            INSERT INTO students (student_id, name, department, phone, email)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, name, department, phone, email))

        connection.commit()
        return True, "Student registered successfully!"

    except sqlite3.IntegrityError:
        return False, "This student ID already exists."

    finally:
        connection.close()


def get_students():
    connection = connect_db()

    try:
        return connection.execute("""
            SELECT student_id, name, department, phone, email
            FROM students
            ORDER BY name
        """).fetchall()

    finally:
        connection.close()


def update_student(student_id, name, department, phone="", email=""):
    connection = connect_db()

    try:
        cursor = connection.execute("""
            UPDATE students
            SET name = ?, department = ?, phone = ?, email = ?
            WHERE student_id = ?
        """, (name, department, phone, email, student_id))

        connection.commit()
        return cursor.rowcount > 0, (
            "Student updated successfully!"
            if cursor.rowcount > 0 else "Student not found."
        )

    finally:
        connection.close()


def delete_student(student_id):
    connection = connect_db()

    try:
        cursor = connection.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )
        connection.commit()

        if cursor.rowcount == 0:
            return False, "Student not found."
        return True, "Student deleted successfully!"

    except sqlite3.IntegrityError:
        return False, "Cannot delete this student because transaction records exist."

    finally:
        connection.close()


# --------------------------------------------------------- transactions ----

def issue_book(student_id, isbn, issue_date, due_date):
    connection = connect_db()

    try:
        student = connection.execute(
            "SELECT student_id FROM students WHERE student_id = ?",
            (student_id,)
        ).fetchone()

        book = connection.execute(
            "SELECT quantity FROM books WHERE isbn = ?",
            (isbn,)
        ).fetchone()

        if not student:
            return False, "Student not found."

        if not book:
            return False, "Book not found."

        if book["quantity"] <= 0:
            return False, "No copies of this book are available."

        if due_date < issue_date:
            return False, "Due date cannot be before the issue date."

        connection.execute("""
            INSERT INTO transactions
                (student_id, isbn, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, 'Issued')
        """, (student_id, isbn, issue_date, due_date))

        connection.execute("""
            UPDATE books SET quantity = quantity - 1
            WHERE isbn = ?
        """, (isbn,))

        connection.commit()
        return True, "Book issued successfully!"

    finally:
        connection.close()


def return_book(transaction_id, return_date):
    connection = connect_db()

    try:
        transaction = connection.execute("""
            SELECT isbn, status, issue_date
            FROM transactions
            WHERE transaction_id = ?
        """, (transaction_id,)).fetchone()

        if not transaction:
            return False, "Transaction not found."

        if transaction["status"] == "Returned":
            return False, "This book has already been returned."

        if return_date < transaction["issue_date"]:
            return False, "Return date cannot be earlier than the issue date."

        connection.execute("""
            UPDATE transactions
            SET return_date = ?, status = 'Returned'
            WHERE transaction_id = ?
        """, (return_date, transaction_id))

        connection.execute("""
            UPDATE books SET quantity = quantity + 1
            WHERE isbn = ?
        """, (transaction["isbn"],))

        connection.commit()
        return True, "Book returned successfully!"

    finally:
        connection.close()


def get_transactions(status=None):
    """All transactions, newest first. Pass status='Issued' or 'Returned'
    to filter. Column names match what main.py expects."""
    connection = connect_db()

    try:
        query = """
            SELECT t.transaction_id, t.student_id, s.name AS student_name,
                   t.isbn, b.title AS book_title, t.issue_date, t.due_date,
                   t.return_date, t.status
            FROM transactions t
            JOIN students s ON t.student_id = s.student_id
            JOIN books b ON t.isbn = b.isbn
        """
        params = ()

        if status:
            query += " WHERE t.status = ?"
            params = (status,)

        query += " ORDER BY t.transaction_id DESC"
        return connection.execute(query, params).fetchall()

    finally:
        connection.close()


# ------------------------------------------------------------ dashboard ----

def get_dashboard_stats():
    connection = connect_db()

    try:
        book_titles = connection.execute(
            "SELECT COUNT(*) FROM books"
        ).fetchone()[0]

        # `quantity` only counts copies that are on the shelf right now.
        available_copies = connection.execute(
            "SELECT COALESCE(SUM(quantity), 0) FROM books"
        ).fetchone()[0]

        total_students = connection.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        books_issued = connection.execute("""
            SELECT COUNT(*) FROM transactions
            WHERE status = 'Issued'
        """).fetchone()[0]

        books_returned = connection.execute("""
            SELECT COUNT(*) FROM transactions
            WHERE status = 'Returned'
        """).fetchone()[0]

        overdue_books = connection.execute("""
            SELECT COUNT(*) FROM transactions
            WHERE status = 'Issued'
              AND due_date < date('now', 'localtime')
        """).fetchone()[0]

        return {
            # every physical copy the library owns = on shelf + out on loan
            "book_copies": available_copies + books_issued,
            "available_copies": available_copies,
            "book_titles": book_titles,
            "students": total_students,
            "issued": books_issued,
            "returned": books_returned,
            "overdue": overdue_books,
        }

    finally:
        connection.close()

def add_demo_transactions():
    import random
    from datetime import date, timedelta

    connection = connect_db()

    try:
        students = connection.execute(
            "SELECT student_id FROM students"
        ).fetchall()

        if not students:
            return "No students found."

        today = date.today()
        added = 0
        random.seed(42)

        for i in range(18):
            books = connection.execute("""
                SELECT isbn, quantity
                FROM books
                WHERE quantity > 0
            """).fetchall()

            if not books:
                break

            student = random.choice(students)
            book = random.choice(books)

            issue_date = today - timedelta(
                days=random.randint(1, 50)
            )
            due_date = issue_date + timedelta(days=14)

            status = "Returned" if i % 3 == 0 else "Issued"

            return_date = None
            if status == "Returned":
                return_date = issue_date + timedelta(
                    days=random.randint(1, 13)
                )

            connection.execute("""
                INSERT INTO transactions
                    (student_id, isbn, issue_date, due_date,
                     return_date, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                student["student_id"],
                book["isbn"],
                issue_date.isoformat(),
                due_date.isoformat(),
                return_date.isoformat() if return_date else None,
                status
            ))

            connection.execute("""
                UPDATE books
                SET quantity = quantity - 1
                WHERE isbn = ?
            """, (book["isbn"],))

            if status == "Returned":
                connection.execute("""
                    UPDATE books
                    SET quantity = quantity + 1
                    WHERE isbn = ?
                """, (book["isbn"],))

            added += 1

        connection.commit()
        return f"Successfully added {added} demo transactions!"

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
