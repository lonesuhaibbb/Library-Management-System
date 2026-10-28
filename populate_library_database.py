import sqlite3
from pathlib import Path

# Run this file from your Library-Management-System folder.
# It keeps existing records and skips students/books that already exist.

DB_PATH = Path(__file__).with_name("library.db")

students = [
    ("Manzoor Ahmad Lone", "25166112001"),
    ("Sadees Ishtiyaq Qadri", "25166112002"),
    ("Mariyah Binti Tariq", "25166112003"),
    ("Mohammad Aaman Latif", "25166112004"),
    ("Yafis Hussain Khan", "25166112005"),
    ("Syed Anoosh Idrees Andrabi", "25166112006"),
    ("Yasin Nazir Teli", "25166112007"),
    ("Ibrahim", "25166112008"),
    ("Mohammad Huzaf Gujree", "25166112009"),
    ("Mir Mohammad Eemaan", "25166112010"),
    ("Tahseen Yaqoob", "25166112011"),
    ("Kafeel Abas", "25166112012"),
    ("Faraz Tahir Raina", "25166112013"),
    ("Misbah Fayaz", "25166112014"),
    ("Saasha", "25166112015"),
    ("Sehreen Nabi", "25166112016"),
    ("Sehreen Jeelani Kakroo", "25166112017"),
    ("Payam Bilal Paray", "25166112018"),
    ("Anayat Zahoor", "25166112019"),
    ("Sahil Gulzar", "25166112020"),
    ("Syed Faiq Rufaie", "25166112021"),
    ("Musa Habib Hafiz", "25166112022"),
    ("Mohammad Husaif Lone", "25166112023"),
    ("Suhaib Mohammad Kharas Baba", "25166112024"),
    ("Aarif Mushtaq", "25166112025"),
    ("Muhammad Faraz Ud Din Bafanda", "25166112026"),
    ("Abrar Javaid peer", "25166112027"),
    ("Hameem Farooq", "25166112028"),
    ("Suhaib Nazir", "25166112029"),
    ("Saad Sheikh", "25166112030"),
    ("Syed Uzair Chesti", "25166112031"),
    ("Osama Bin Asrar", "25166112032"),
    ("Mohammad Musaib Khan", "25166112033"),
    ("Syed Tufail Andrabi", "25166112034"),
    ("Haroon Hamid Dar", "25166112035"),
    ("Zayeem Zahoor", "25166112036"),
]

# 20 commonly used undergraduate books per subject area.
# ISBNs are synthetic inventory identifiers for this demo database, not publisher ISBNs.
books = [
    # CSE (20)
    ("CSE001", "Introduction to Algorithms", "Thomas H. Cormen et al.", "CSE", 4),
    ("CSE002", "Data Structures and Algorithms in C++", "Michael T. Goodrich et al.", "CSE", 4),
    ("CSE003", "The C Programming Language", "Brian W. Kernighan and Dennis M. Ritchie", "CSE", 3),
    ("CSE004", "Let Us C", "Yashavant Kanetkar", "CSE", 4),
    ("CSE005", "Operating System Concepts", "Abraham Silberschatz, Peter B. Galvin and Greg Gagne", "CSE", 3),
    ("CSE006", "Modern Operating Systems", "Andrew S. Tanenbaum and Herbert Bos", "CSE", 3),
    ("CSE007", "Computer Networks", "Andrew S. Tanenbaum and David J. Wetherall", "CSE", 4),
    ("CSE008", "Data Communications and Networking", "Behrouz A. Forouzan", "CSE", 3),
    ("CSE009", "Database System Concepts", "Abraham Silberschatz, Henry F. Korth and S. Sudarshan", "CSE", 4),
    ("CSE010", "Fundamentals of Database Systems", "Ramez Elmasri and Shamkant B. Navathe", "CSE", 3),
    ("CSE011", "Computer Organization and Design", "David A. Patterson and John L. Hennessy", "CSE", 3),
    ("CSE012", "Computer System Architecture", "M. Morris Mano", "CSE", 3),
    ("CSE013", "Discrete Mathematics and Its Applications", "Kenneth H. Rosen", "CSE", 3),
    ("CSE014", "Artificial Intelligence: A Modern Approach", "Stuart Russell and Peter Norvig", "CSE", 2),
    ("CSE015", "Pattern Recognition and Machine Learning", "Christopher M. Bishop", "CSE", 2),
    ("CSE016", "Deep Learning", "Ian Goodfellow, Yoshua Bengio and Aaron Courville", "CSE", 2),
    ("CSE017", "Software Engineering", "Ian Sommerville", "CSE", 3),
    ("CSE018", "Compilers: Principles, Techniques, and Tools", "Alfred V. Aho et al.", "CSE", 2),
    ("CSE019", "Theory of Computation", "Michael Sipser", "CSE", 2),
    ("CSE020", "Python Crash Course", "Eric Matthes", "CSE", 4),

    # IMBA / business and management (20)
    ("IMBA001", "Principles of Management", "Harold Koontz and Heinz Weihrich", "IMBA", 3),
    ("IMBA002", "Management", "Stephen P. Robbins and Mary Coulter", "IMBA", 3),
    ("IMBA003", "Organizational Behavior", "Stephen P. Robbins and Timothy A. Judge", "IMBA", 3),
    ("IMBA004", "Marketing Management", "Philip Kotler and Kevin Lane Keller", "IMBA", 3),
    ("IMBA005", "Fundamentals of Marketing", "William J. Stanton et al.", "IMBA", 3),
    ("IMBA006", "Financial Management", "Eugene F. Brigham and Joel F. Houston", "IMBA", 3),
    ("IMBA007", "Fundamentals of Financial Management", "James C. Van Horne and John M. Wachowicz Jr.", "IMBA", 3),
    ("IMBA008", "Managerial Accounting", "Ray H. Garrison, Eric W. Noreen and Peter C. Brewer", "IMBA", 3),
    ("IMBA009", "Accounting: Text and Cases", "Robert N. Anthony and James S. Reece", "IMBA", 2),
    ("IMBA010", "Business Statistics", "J. K. Sharma", "IMBA", 3),
    ("IMBA011", "Statistics for Management", "Richard I. Levin and David S. Rubin", "IMBA", 3),
    ("IMBA012", "Business Economics", "H. L. Ahuja", "IMBA", 3),
    ("IMBA013", "Managerial Economics", "William F. Samuelson and Stephen G. Marks", "IMBA", 2),
    ("IMBA014", "Business Communication", "Raman and Singh", "IMBA", 3),
    ("IMBA015", "Human Resource Management", "Gary Dessler", "IMBA", 3),
    ("IMBA016", "Operations Management", "William J. Stevenson", "IMBA", 3),
    ("IMBA017", "Research Methodology", "C. R. Kothari and Gaurav Garg", "IMBA", 3),
    ("IMBA018", "Entrepreneurship: Successfully Launching New Ventures", "Bruce R. Barringer and R. Duane Ireland", "IMBA", 2),
    ("IMBA019", "Strategic Management", "Fred R. David and Forest R. David", "IMBA", 2),
    ("IMBA020", "Essentials of Supply Chain Management", "Michael H. Hugos", "IMBA", 2),

    # Botany (20)
    ("BOT001", "Botany: An Introduction to Plant Biology", "James D. Mauseth", "Botany", 3),
    ("BOT002", "Raven Biology of Plants", "Ray F. Evert and Susan E. Eichhorn", "Botany", 3),
    ("BOT003", "Plant Physiology and Development", "Lincoln Taiz et al.", "Botany", 3),
    ("BOT004", "Plant Physiology", "S. N. Pandey and B. K. Sinha", "Botany", 3),
    ("BOT005", "Plant Anatomy", "Katherine Esau", "Botany", 2),
    ("BOT006", "Anatomy of Seed Plants", "Katherine Esau", "Botany", 2),
    ("BOT007", "Plant Taxonomy", "O. P. Sharma", "Botany", 3),
    ("BOT008", "Taxonomy of Angiosperms", "V. N. Naik", "Botany", 2),
    ("BOT009", "The Diversity of Fungi", "George C. Ainsworth", "Botany", 2),
    ("BOT010", "Introductory Mycology", "C. J. Alexopoulos, C. W. Mims and M. Blackwell", "Botany", 2),
    ("BOT011", "Introductory Phycology", "H. D. Kumar", "Botany", 2),
    ("BOT012", "Cryptogamic Botany, Volume I", "Gilbert M. Smith", "Botany", 2),
    ("BOT013", "Cryptogamic Botany, Volume II", "Gilbert M. Smith", "Botany", 2),
    ("BOT014", "Plant Pathology", "George N. Agrios", "Botany", 3),
    ("BOT015", "Genetics: A Conceptual Approach", "Benjamin A. Pierce", "Botany", 3),
    ("BOT016", "Cell Biology", "Gerald Karp", "Botany", 3),
    ("BOT017", "Ecology: The Economy of Nature", "Robert E. Ricklefs and Rick Relyea", "Botany", 2),
    ("BOT018", "Fundamentals of Ecology", "Eugene P. Odum and Gary W. Barrett", "Botany", 2),
    ("BOT019", "Economic Botany", "B. P. Pandey", "Botany", 3),
    ("BOT020", "Practical Botany", "B. P. Pandey", "Botany", 3),
]

def quote_identifier(identifier):
    return '"' + identifier.replace('"', '""') + '"'

def pick_column(columns, candidates):
    lower_map = {c.lower(): c for c in columns}
    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]
    return None

def insert_rows(conn, table, rows, mapping, unique_columns):
    cur = conn.cursor()
    existing = {r[1] for r in cur.execute(f"PRAGMA table_info({quote_identifier(table)})").fetchall()}
    selected = [(key, col) for key, col in mapping.items() if col and col in existing]
    if not selected:
        print(f"Skipped {table}: no matching columns found.")
        return 0
    inserted = 0
    for row in rows:
        values = dict(row)
        where_cols = [mapping[k] for k in unique_columns if mapping.get(k) in existing]
        where_keys = [k for k in unique_columns if mapping.get(k) in existing]
        if where_cols:
            where = " AND ".join(f"{quote_identifier(c)} = ?" for c in where_cols)
            params = [values[k] for k in where_keys]
            if cur.execute(f"SELECT 1 FROM {quote_identifier(table)} WHERE {where} LIMIT 1", params).fetchone():
                continue
        cols = [col for _, col in selected]
        vals = [values[key] for key, _ in selected]
        sql = f"INSERT INTO {quote_identifier(table)} ({', '.join(quote_identifier(c) for c in cols)}) VALUES ({', '.join('?' for _ in cols)})"
        try:
            cur.execute(sql, vals)
            inserted += 1
        except sqlite3.IntegrityError as exc:
            print(f"Skipped a row in {table} due to a database constraint: {exc}")
    return inserted

def main():
    if not DB_PATH.exists():
        print(f"Could not find {DB_PATH}. Put this script beside library.db and run it again.")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        student_table = next((t for t in ("students", "student") if t in tables), None)
        book_table = next((t for t in ("books", "book") if t in tables), None)
        if not student_table or not book_table:
            print("Could not find the expected students and books tables.")
            print("Tables found:", ", ".join(sorted(tables)))
            return

        student_cols = [r[1] for r in conn.execute(f"PRAGMA table_info({quote_identifier(student_table)})")]
        book_cols = [r[1] for r in conn.execute(f"PRAGMA table_info({quote_identifier(book_table)})")]

        student_mapping = {
            "student_id": pick_column(student_cols, ["student_id", "enrollment_no", "enrollment_number", "id"]),
            "name": pick_column(student_cols, ["name", "student_name", "full_name"]),
            "department": pick_column(student_cols, ["department", "course", "programme", "program"]),
            "phone": pick_column(student_cols, ["phone", "phone_number", "mobile"]),
            "email": pick_column(student_cols, ["email", "email_address"]),
        }
        book_mapping = {
            "isbn": pick_column(book_cols, ["isbn", "book_id", "id"]),
            "title": pick_column(book_cols, ["title", "book_title", "name"]),
            "author": pick_column(book_cols, ["author", "authors"]),
            "category": pick_column(book_cols, ["category", "department", "subject", "course"]),
            "quantity": pick_column(book_cols, ["quantity", "copies", "total_copies", "book_copies"]),
        }

        student_rows = [
            {"student_id": sid, "name": name, "department": "", "phone": "", "email": ""}
            for name, sid in students
        ]
        book_rows = [
            {"isbn": isbn, "title": title, "author": author, "category": category, "quantity": quantity}
            for isbn, title, author, category, quantity in books
        ]

        added_students = insert_rows(conn, student_table, student_rows, student_mapping, ["student_id"])
        added_books = insert_rows(conn, book_table, book_rows, book_mapping, ["isbn", "title"])
        conn.commit()
        print(f"Database updated successfully: {added_students} students added and {added_books} books added.")
        print("Student IDs are the enrollment numbers from the supplied list.")
        print("Book categories: CSE (20), IMBA (20), Botany (20).")
        print("Existing records were kept; matching records were skipped.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
