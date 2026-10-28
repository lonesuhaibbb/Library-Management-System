import os
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from database import (
    create_tables, add_book, get_books, update_book, delete_book,
    add_student, get_students, update_student, delete_student,
    issue_book, return_book, get_transactions, get_dashboard_stats
)

# set_page_config must be the first Streamlit command in the script
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_tables()

st.markdown("""
<style>
.stApp { background: #F5F7FB; }
[data-testid="stSidebar"] { background: #14213D; }
[data-testid="stSidebar"] * { color: #FFFFFF; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding: 5px 0; }
h1, h2, h3 { color: #14213D; }
[data-testid="stMetric"] {
    background: #FFFFFF; padding: 18px; border-radius: 12px;
    border: 1px solid #E5EAF2; box-shadow: 0 2px 8px rgba(20,33,61,.05);
}
.stButton > button, .stFormSubmitButton > button {
    background: #2563EB; color: white; border: 0; border-radius: 8px;
    font-weight: 600; min-height: 40px;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: #1D4ED8; color: white; border: 0;
}
div[data-testid="stDataFrame"] { background: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Demo credentials for this local college project. Change them before sharing
# (or set the LIBRARY_ADMIN_USER / LIBRARY_ADMIN_PASSWORD environment variables).
ADMIN_USERNAME = os.getenv("LIBRARY_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("LIBRARY_ADMIN_PASSWORD", "library123")

FINE_PER_DAY = 5  # rupees

CATEGORIES = [
    "Computer Science", "Artificial Intelligence", "Mathematics",
    "Science", "Literature", "History", "Other"
]
DEPARTMENTS = [
    "AI & Data Science", "Computer Science", "Information Technology",
    "Mathematics", "Other"
]

BOOK_LABELS = {
    "isbn": "ISBN", "title": "Title", "author": "Author",
    "category": "Category", "quantity": "Available Copies",
}
STUDENT_LABELS = {
    "student_id": "Student ID", "name": "Name", "department": "Department",
    "phone": "Phone", "email": "Email",
}
TRANSACTION_LABELS = {
    "transaction_id": "Transaction ID", "student_id": "Student ID",
    "student_name": "Student", "isbn": "ISBN", "book_title": "Book",
    "issue_date": "Issued On", "due_date": "Due Date",
    "return_date": "Returned On", "status": "Status",
}

# ------------------------------------------------------------------ login --

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    left, center, right = st.columns([1, 1.2, 1])
    with center:
        st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align:center;font-size:48px'>📚</div>"
            "<h1 style='text-align:center'>Library Management</h1>"
            "<p style='text-align:center;color:#64748B'>Manager sign-in</p>",
            unsafe_allow_html=True
        )
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_clicked = st.form_submit_button("Sign in", width="stretch")
        if login_clicked:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect username or password.")
    st.stop()

# ------------------------------------------------------------- navigation --

pages = [
    "Dashboard", "Manage Books", "Manage Students",
    "Issue Books", "Return Books", "Reports"
]
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Dashboard"


def go_to(page_name):
    # Runs as a button callback, i.e. BEFORE the sidebar radio is drawn.
    # Changing a widget's session_state key after the widget exists raises
    # an error, which is what the old Quick Access buttons did.
    st.session_state.selected_page = page_name


with st.sidebar:
    st.markdown("## 📚 Library Admin")
    st.caption("Management workspace")
    page = st.radio("Navigation", pages, key="selected_page")
    st.divider()
    st.caption("Library Management System")
    if st.button("Log out", width="stretch"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------------------------------------------------------- helpers --


def rows_to_df(rows):
    """Turn database rows into a DataFrame (empty DataFrame if no rows)."""
    return pd.DataFrame([dict(row) for row in rows])


def clean(value):
    """None / NaN -> empty string, so text boxes never receive NaN."""
    return "" if pd.isna(value) else str(value)


def show_message(result):
    success, message = result
    if success:
        st.success(message)
    else:
        st.error(message)


def flash(result):
    """Remember a message so it survives the st.rerun() that follows."""
    st.session_state["flash"] = result


def show_flash():
    result = st.session_state.pop("flash", None)
    if result:
        show_message(result)


# ------------------------------------------------------------- dashboard ---

if page == "Dashboard":
    stats = get_dashboard_stats()
    st.title("📚 Library Dashboard")
    st.write("Welcome back, Library Manager!")

    st.markdown("""
    <div style="background:linear-gradient(120deg,#14213D,#2563EB);
        padding:26px;border-radius:15px;color:white;margin-bottom:20px">
        <h2 style="color:white;margin:0">Your Library, All in One Place</h2>
        <p style="color:#E5EDFF;margin-bottom:0">
        Manage books, students, and borrowing activity from one dashboard.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric(
        "📚 Book Copies", stats["book_copies"],
        help=f'{stats["available_copies"]} on the shelf + {stats["issued"]} currently issued'
    )
    c2.metric("📖 Book Titles", stats["book_titles"])
    c3.metric("🎓 Registered Students", stats["students"])
    c4, c5, c6 = st.columns(3)
    c4.metric("📤 Currently Issued", stats["issued"])
    c5.metric("✅ Returned", stats["returned"])
    c6.metric("⏰ Overdue", stats["overdue"])

    st.divider()
    st.subheader("Quick Access")
    q1, q2, q3 = st.columns(3)
    q1.button("📚 Manage Books", width="stretch",
              on_click=go_to, args=("Manage Books",))
    q2.button("🎓 Manage Students", width="stretch",
              on_click=go_to, args=("Manage Students",))
    q3.button("📤 Issue a Book", width="stretch",
              on_click=go_to, args=("Issue Books",))

# ---------------------------------------------------------- manage books ---

elif page == "Manage Books":
    st.title("📖 Manage Books")
    st.write("Add, search, update, and remove books from your collection.")
    show_flash()

    with st.expander("➕ Add a New Book", expanded=True):
        with st.form("add_book_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            title = c1.text_input("Book Title")
            author = c2.text_input("Author")
            isbn = c1.text_input("ISBN")
            category = c2.selectbox("Category", CATEGORIES)
            quantity = st.number_input("Number of copies", min_value=1, value=1, step=1)
            submitted = st.form_submit_button("Add Book")
        if submitted:
            if title.strip() and author.strip() and isbn.strip():
                show_message(add_book(
                    isbn.strip(), title.strip(), author.strip(), category, int(quantity)
                ))
            else:
                st.error("Please enter the title, author, and ISBN.")

    st.divider()
    st.subheader("Book Collection")
    book_df = rows_to_df(get_books())

    if book_df.empty:
        st.info("No books have been added yet.")
    else:
        search = st.text_input("🔍 Search by title, author, ISBN, or category")
        if search:
            # regex=False so characters like ( + * in the search box don't crash
            mask = book_df.astype(str).apply(
                lambda col: col.str.contains(search, case=False, na=False, regex=False)
            ).any(axis=1)
            shown_books = book_df[mask]
        else:
            shown_books = book_df
        st.dataframe(
            shown_books.rename(columns=BOOK_LABELS),
            width="stretch", hide_index=True
        )

        titles = dict(zip(book_df["isbn"], book_df["title"]))
        isbn_label = lambda i: f"{i} — {titles[i]}"

        with st.expander("✏️ Update a Book"):
            st.caption(
                "Available copies = copies currently on the shelf "
                "(issuing a book lowers it, returning raises it)."
            )
            selected_isbn = st.selectbox(
                "Choose book to update", book_df["isbn"].tolist(),
                format_func=isbn_label, key="update_book_isbn"
            )
            selected = book_df[book_df["isbn"] == selected_isbn].iloc[0]
            with st.form("update_book_form"):
                new_title = st.text_input(
                    "Title", value=selected["title"], key=f"u_title_{selected_isbn}")
                new_author = st.text_input(
                    "Author", value=selected["author"], key=f"u_author_{selected_isbn}")
                current_category = selected["category"]
                category_index = (
                    CATEGORIES.index(current_category)
                    if current_category in CATEGORIES else len(CATEGORIES) - 1
                )
                new_category = st.selectbox(
                    "Category", CATEGORIES, index=category_index,
                    key=f"u_cat_{selected_isbn}")
                new_quantity = st.number_input(
                    "Available copies", min_value=0, value=int(selected["quantity"]),
                    step=1, key=f"u_qty_{selected_isbn}")
                update_clicked = st.form_submit_button("Save Changes")
            if update_clicked:
                if new_title.strip() and new_author.strip():
                    flash(update_book(
                        selected_isbn, new_title.strip(), new_author.strip(),
                        new_category, int(new_quantity)
                    ))
                    st.rerun()
                else:
                    st.error("Title and author cannot be empty.")

        with st.expander("🗑️ Delete a Book"):
            st.warning("Books with borrowing history cannot be deleted. Set copies to 0 to retire one.")
            # A form with clear_on_submit un-ticks the confirmation box after each delete
            with st.form("delete_book_form", clear_on_submit=True):
                delete_isbn = st.selectbox(
                    "Choose book to delete", book_df["isbn"].tolist(),
                    format_func=isbn_label
                )
                confirm_delete = st.checkbox("I confirm that I want to delete this book.")
                delete_clicked = st.form_submit_button("Delete Selected Book")
            if delete_clicked:
                if confirm_delete:
                    flash(delete_book(delete_isbn))
                    st.rerun()
                else:
                    st.warning("Please tick the confirmation box first.")

# ------------------------------------------------------- manage students ---

elif page == "Manage Students":
    st.title("🎓 Manage Students")
    st.write("Register students and maintain their details.")
    show_flash()

    with st.expander("➕ Register a Student", expanded=True):
        with st.form("add_student_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            student_id = c1.text_input("Student ID")
            name = c2.text_input("Full Name")
            department = c1.selectbox("Department", DEPARTMENTS)
            phone = c2.text_input("Phone (optional)")
            email = st.text_input("Email (optional)")
            student_submit = st.form_submit_button("Register Student")
        if student_submit:
            if student_id.strip() and name.strip():
                show_message(add_student(
                    student_id.strip(), name.strip(), department,
                    phone.strip(), email.strip()
                ))
            else:
                st.error("Student ID and name are required.")

    st.divider()
    st.subheader("Registered Students")
    student_df = rows_to_df(get_students())

    if student_df.empty:
        st.info("No students have been registered yet.")
    else:
        student_search = st.text_input("🔍 Search students by ID, name, department, phone, or email")
        shown_students = student_df
        if student_search:
            mask = student_df.astype(str).apply(
                lambda col: col.str.contains(
                    student_search, case=False, na=False, regex=False)
            ).any(axis=1)
            shown_students = student_df[mask]
        st.dataframe(
            shown_students.fillna("").rename(columns=STUDENT_LABELS),
            width="stretch", hide_index=True
        )

        names = dict(zip(student_df["student_id"], student_df["name"]))
        student_label = lambda s: f"{s} — {names[s]}"

        with st.expander("✏️ Update Student Details"):
            chosen_student = st.selectbox(
                "Choose student", student_df["student_id"].tolist(),
                format_func=student_label, key="update_student_id"
            )
            student = student_df[student_df["student_id"] == chosen_student].iloc[0]
            with st.form("update_student_form"):
                edit_name = st.text_input(
                    "Full Name", value=student["name"], key=f"s_name_{chosen_student}")
                old_dept = student["department"]
                dept_index = (
                    DEPARTMENTS.index(old_dept)
                    if old_dept in DEPARTMENTS else len(DEPARTMENTS) - 1
                )
                edit_dept = st.selectbox(
                    "Department", DEPARTMENTS, index=dept_index,
                    key=f"s_dept_{chosen_student}")
                edit_phone = st.text_input(
                    "Phone", value=clean(student["phone"]), key=f"s_phone_{chosen_student}")
                edit_email = st.text_input(
                    "Email", value=clean(student["email"]), key=f"s_email_{chosen_student}")
                student_update = st.form_submit_button("Save Student Changes")
            if student_update:
                if edit_name.strip():
                    flash(update_student(
                        chosen_student, edit_name.strip(), edit_dept,
                        edit_phone.strip(), edit_email.strip()
                    ))
                    st.rerun()
                else:
                    st.error("Name cannot be empty.")

        with st.expander("🗑️ Delete a Student"):
            st.warning("Students with borrowing history cannot be deleted.")
            with st.form("delete_student_form", clear_on_submit=True):
                delete_student_id = st.selectbox(
                    "Choose student to delete", student_df["student_id"].tolist(),
                    format_func=student_label
                )
                confirm_student_delete = st.checkbox(
                    "I confirm that I want to delete this student."
                )
                delete_student_clicked = st.form_submit_button("Delete Selected Student")
            if delete_student_clicked:
                if confirm_student_delete:
                    flash(delete_student(delete_student_id))
                    st.rerun()
                else:
                    st.warning("Please tick the confirmation box first.")

# ----------------------------------------------------------- issue books ---

elif page == "Issue Books":
    st.title("📤 Issue Books")
    st.write("Issue available books to registered students.")
    show_flash()

    student_rows = get_students()
    all_books = get_books()
    book_rows = [r for r in all_books if r["quantity"] > 0]  # only books on the shelf

    if not student_rows:
        st.warning("Register at least one student before issuing a book.")
    elif not all_books:
        st.warning("Add at least one book before issuing a book.")
    elif not book_rows:
        st.warning("All copies are currently issued. Nothing is available right now.")
    else:
        student_options = {
            f'{r["student_id"]} — {r["name"]}': r["student_id"] for r in student_rows
        }
        book_options = {
            f'{r["isbn"]} — {r["title"]} (available: {r["quantity"]})': r["isbn"]
            for r in book_rows
        }
        with st.form("issue_book_form", clear_on_submit=True):
            student_label = st.selectbox("Student", list(student_options.keys()))
            book_label = st.selectbox("Book", list(book_options.keys()))
            issue_day = st.date_input("Issue Date", value=date.today())
            due_day = st.date_input("Due Date", value=date.today() + timedelta(days=14))
            issue_submit = st.form_submit_button("Issue Book")
        if issue_submit:
            flash(issue_book(
                student_options[student_label],
                book_options[book_label],
                issue_day.isoformat(),
                due_day.isoformat()
            ))
            st.rerun()

    st.divider()
    st.subheader("Currently Issued Books")
    active = rows_to_df(get_transactions("Issued"))
    if active.empty:
        st.info("There are no currently issued books.")
    else:
        today_text = date.today().isoformat()
        active["Overdue"] = active["due_date"].apply(
            lambda d: "Yes" if d < today_text else "No"
        )
        st.dataframe(
            active.drop(columns=["return_date", "status"]).rename(columns=TRANSACTION_LABELS),
            width="stretch", hide_index=True
        )

# --------------------------------------------------------- return books ----

elif page == "Return Books":
    st.title("📥 Return Books")
    st.write("Record returned books and check overdue charges.")
    show_flash()

    active_rows = get_transactions("Issued")
    active_df = rows_to_df(active_rows)

    if active_df.empty:
        st.info("There are no books waiting to be returned.")
    else:
        labels = {
            f'#{r["transaction_id"]} — {r["book_title"]} / {r["student_name"]} (due {r["due_date"]})':
            int(r["transaction_id"])
            for r in active_rows
        }
        with st.form("return_book_form"):
            selected_label = st.selectbox("Select issue record", list(labels.keys()))
            return_day = st.date_input("Return Date", value=date.today())
            return_submit = st.form_submit_button("Confirm Return")
        if return_submit:
            # database.return_book() also checks the return date against the issue date
            flash(return_book(labels[selected_label], return_day.isoformat()))
            st.rerun()

    st.divider()
    st.subheader("Overdue Charge Guide")
    st.write(f"This project calculates a suggested fine of ₹{FINE_PER_DAY} per day after the due date.")
    if not active_df.empty:
        today = date.today()
        overdue_df = active_df.copy()
        overdue_df["Days Overdue"] = overdue_df["due_date"].apply(
            lambda d: max((today - date.fromisoformat(d)).days, 0)
        )
        overdue_df["Estimated Fine (₹)"] = overdue_df["Days Overdue"] * FINE_PER_DAY
        overdue_only = overdue_df[overdue_df["Days Overdue"] > 0]
        if overdue_only.empty:
            st.success("There are no overdue books today.")
        else:
            st.dataframe(
                overdue_only[[
                    "transaction_id", "student_id", "student_name", "book_title",
                    "due_date", "Days Overdue", "Estimated Fine (₹)"
                ]].rename(columns=TRANSACTION_LABELS),
                width="stretch",
                hide_index=True
            )

# ---------------------------------------------------------------- reports --

elif page == "Reports":
    st.title("📊 Reports & Analytics")
    st.write("Live summaries based on the records in your database.")
    stats = get_dashboard_stats()
    a, b, c, d = st.columns(4)
    a.metric("Book Titles", stats["book_titles"])
    b.metric("Book Copies", stats["book_copies"])
    c.metric("Students", stats["students"])
    d.metric("Books Issued Now", stats["issued"])

    book_df = rows_to_df(get_books())
    if not book_df.empty:
        st.subheader("Books by Category")
        category_df = book_df.groupby("category", as_index=False)["quantity"].sum()
        category_df.columns = ["Category", "Copies"]
        fig = px.bar(
            category_df, x="Category", y="Copies", color="Category",
            title="Available Copies by Category"
        )
        fig.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Add books to see the category chart.")

    transaction_df = rows_to_df(get_transactions())
    if not transaction_df.empty:
        st.subheader("Borrowing History")
        st.dataframe(
            transaction_df.fillna("").rename(columns=TRANSACTION_LABELS),
            width="stretch", hide_index=True
        )
        status_counts = transaction_df["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig2 = px.pie(status_counts, names="Status", values="Count", title="Issued vs Returned")
        st.plotly_chart(fig2, width="stretch")
    else:
        st.info("No borrowing transactions exist yet.")
