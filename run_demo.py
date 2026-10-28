from datetime import date, timedelta
from database import connect_db

connection = connect_db()

try:
    rows = connection.execute("""
        SELECT transaction_id, issue_date
        FROM transactions
        WHERE status = 'Returned'
        AND return_date IS NULL
    """).fetchall()

    updated = 0

    for row in rows:
        issue_date = date.fromisoformat(row["issue_date"])
        return_date = issue_date + timedelta(days=7)

        connection.execute("""
            UPDATE transactions
            SET return_date = ?
            WHERE transaction_id = ?
        """, (
            return_date.isoformat(),
            row["transaction_id"]
        ))

        updated += 1

    connection.commit()
    print(f"Successfully filled {updated} missing return dates.")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()