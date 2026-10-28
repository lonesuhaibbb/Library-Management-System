<div align="center">

A web-based system for managing library books, students, and borrowing activity,
built with Python, Streamlit, and SQLite.
<img src="assets/logo.svg" alt="Library Management System logo" width="160" />

# 📚 Library Management System

- Manager login
- Dashboard with live statistics (copies, titles, students, issued, returned, overdue)
- Add, search, update, and delete books
- Register, search, update, and delete students
- Issue books to students and record returns
- Overdue tracking with an estimated fine (₹5 per day)
- Reports with charts (copies by category, issued vs returned) and full borrowing history

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Status](https://img.shields.io/badge/status-active-success)
![Team](https://img.shields.io/badge/team-7%20students-blueviolet)

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

</div>

Developed by a team of 7 students.
---

## 📖 About

The **Library Management System** replaces paper registers and scattered spreadsheets with one simple program. Librarians can keep the book catalogue up to date, manage members, and track every book that is issued or returned, all from a single place.

It was built as a team project by a group of 7 students.

## ✨ Features

| | Feature | Description |
|---|---|---|
| 📕 | **Book management** | Add new books and view the full catalogue |
| 🔍 | **Search** | Quickly find books in the collection |
| ✏️ | **Update & delete** | Edit or remove book records |
| 👥 | **Member management** | Register and manage library members |
| 🔄 | **Issue & return** | Issue books to members and record returns |

## 🛠️ Tech Stack

- **Language:** Python
- **Version control:** Git & GitHub

## 🚀 Getting Started

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/lonesuhaibbb/Library-Management-System.git

# 2. Move into the project folder
cd Library-Management-System

# 3. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 4. Install dependencies (if a requirements.txt exists)
pip install -r requirements.txt
```

### Run the app

```bash
python main.py
```

> 💡 Replace `main.py` with the actual entry file of your project.

## 🧭 Usage

Once the program is running, you can:

1. **Add a book**: enter its title, author and other details.
2. **Search for a book**: look it up by title or author.
3. **Register a member**: add a new library member.
4. **Issue a book**: assign an available book to a member.
5. **Return a book**: mark an issued book as returned.
6. **Update or delete** any book record when needed.

## 📁 Project Structure

```
Library-Management-System/
├── assets/
│   └── logo.svg
├── main.py            # Entry point
├── README.md
└── ...
```

> Update this tree to match your actual files and folders.

## 👨‍💻 Team

Developed by a team of 7 students.

| Name | GitHub |
|---|---|
| Haider Hamid | [@haidrerDroid](https://github.com/haidrerDroid) |
| Lone Suhaib | [@lonesuhaibbb](https://github.com/lonesuhaibbb) |
| Sayed Shakir | [@shakirsyed819](https://github.com/shakirsyed819) |
| Daniaa Khan | [@daniaa12](https://github.com/daniaa12) |
| Haroon Hamid | [@haroonhamiddar](https://github.com/haroonhamiddar) |
| Zayeem Zahoor | [@zayeemzahoor18-netizen](https://github.com/zayeemzahoor18-netizen) |
| Sahil Gulzar | [@sahilmalik3401-cmd](https://github.com/sahilmalik3401-cmd) |

## 🗺️ Roadmap

- [x] Add, view, update and delete books
- [x] Search books
- [x] Member management
- [x] Issue and return books
- [ ] Due dates and fine calculation
- [ ] Persistent storage (database)
- [ ] Graphical user interface
- [ ] Reports and statistics

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Open a Pull Request



<div align="center">

Made with ❤️ by students · ⭐ Star this repo if you found it useful!

</div>
