# 📚 Student Grade Tracker

A beginner-friendly Python + SQLite project that manages student records and grades.

## 🛠 Tech Stack
- **Python 3** — core logic and menu interface
- **SQLite3** — built-in database (no install needed!)

## ▶️ How to Run in VS Code

1. Open the project folder in VS Code
2. Open the terminal (`Ctrl + `` ` ``)
3. Run the app:

```bash
python grade_tracker.py
```

> ✅ No pip installs required — `sqlite3` comes built into Python!

---

## 💡 Features

| Feature | Description |
|--------|-------------|
| Add Student | Store name + email |
| View Students | List all students |
| Delete Student | Remove student + their grades |
| Add Grade | Record a subject grade (0–100) |
| View Grades | See all grades + average for a student |
| Top Students | Ranked leaderboard by average grade |

---

## 🗃 Database Schema

```sql
students (id, name, email)
grades   (id, student_id, subject, grade)
```

- `grades.db` is auto-created on first run
- Uses a foreign key relationship between tables

---

## 📁 Project Structure

```
grade_tracker/
├── grade_tracker.py   ← main app
├── grades.db          ← auto-created SQLite database
└── README.md
```

---

## 🧠 Skills Demonstrated

- Python functions and modules
- SQLite3 CRUD operations (Create, Read, Update, Delete)
- SQL JOINs and aggregate functions (AVG, GROUP BY)
- Input validation and error handling
- CLI menu interface
