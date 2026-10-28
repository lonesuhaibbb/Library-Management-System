"""Automated tests for database.py

Run from the project folder with either:
    python test_database.py
    python -m unittest -v

Every test uses a temporary database, so your real library.db is never touched.
"""
import os
import sqlite3
import tempfile
import unittest

import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db = database.DB_NAME
        database.DB_NAME = os.path.join(self.temp_dir.name, "test_library.db")
        database.create_tables()

        database.add_book("111", "Python Basics", "A. Author", "Computer Science", 2)
        database.add_student("S1", "Asha Khan", "Computer Science")

    def tearDown(self):
        database.DB_NAME = self.original_db
        self.temp_dir.cleanup()

    def quantity(self, isbn):
        return next(b["quantity"] for b in database.get_books() if b["isbn"] == isbn)

    def test_tables_are_created(self):
        connection = sqlite3.connect(database.DB_NAME)
        tables = {row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'")}
        connection.close()
        self.assertTrue({"books", "students", "transactions"} <= tables)

    def test_duplicate_isbn_is_rejected(self):
        ok, _ = database.add_book("111", "Another", "B. Author", "Other", 1)
        self.assertFalse(ok)

    def test_issue_and_return_update_stock(self):
        ok, _ = database.issue_book("S1", "111", "2026-01-01", "2026-01-15")
        self.assertTrue(ok)
        self.assertEqual(self.quantity("111"), 1)

        transaction_id = database.get_transactions("Issued")[0]["transaction_id"]
        ok, _ = database.return_book(transaction_id, "2026-01-10")
        self.assertTrue(ok)
        self.assertEqual(self.quantity("111"), 2)

    def test_cannot_issue_when_no_copies_left(self):
        database.issue_book("S1", "111", "2026-01-01", "2026-01-15")
        database.issue_book("S1", "111", "2026-01-01", "2026-01-15")
        ok, message = database.issue_book("S1", "111", "2026-01-01", "2026-01-15")
        self.assertFalse(ok)
        self.assertIn("available", message)

    def test_due_date_cannot_be_before_issue_date(self):
        ok, _ = database.issue_book("S1", "111", "2026-01-10", "2026-01-01")
        self.assertFalse(ok)

    def test_return_date_cannot_be_before_issue_date(self):
        database.issue_book("S1", "111", "2026-01-10", "2026-01-24")
        transaction_id = database.get_transactions("Issued")[0]["transaction_id"]
        ok, _ = database.return_book(transaction_id, "2026-01-01")
        self.assertFalse(ok)

    def test_book_cannot_be_returned_twice(self):
        database.issue_book("S1", "111", "2026-01-01", "2026-01-15")
        transaction_id = database.get_transactions("Issued")[0]["transaction_id"]
        database.return_book(transaction_id, "2026-01-05")
        ok, _ = database.return_book(transaction_id, "2026-01-06")
        self.assertFalse(ok)
        self.assertEqual(self.quantity("111"), 2)

    def test_cannot_delete_book_or_student_with_history(self):
        database.issue_book("S1", "111", "2026-01-01", "2026-01-15")
        self.assertFalse(database.delete_book("111")[0])
        self.assertFalse(database.delete_student("S1")[0])

    def test_get_transactions_filter_and_columns(self):
        database.issue_book("S1", "111", "2026-01-01", "2026-01-15")
        row = database.get_transactions("Issued")[0]
        self.assertEqual(row["student_name"], "Asha Khan")
        self.assertEqual(row["book_title"], "Python Basics")
        self.assertEqual(database.get_transactions("Returned"), [])

    def test_dashboard_stats(self):
        database.add_book("222", "Algebra", "C. Author", "Mathematics", 3)
        database.issue_book("S1", "111", "2020-01-01", "2020-01-15")  # long overdue

        stats = database.get_dashboard_stats()
        self.assertEqual(stats["book_titles"], 2)       # 2 different books
        self.assertEqual(stats["book_copies"], 5)       # 2 + 3 owned in total
        self.assertEqual(stats["available_copies"], 4)  # one is out on loan
        self.assertEqual(stats["students"], 1)
        self.assertEqual(stats["issued"], 1)
        self.assertEqual(stats["returned"], 0)
        self.assertEqual(stats["overdue"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
