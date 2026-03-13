"""
Student Grade Tracker
=====================
A simple Python + SQLite project for managing student grades.
Built with: Python 3, SQLite3 (no extra installs needed!)
"""

import sqlite3

def connect():
    """Connect to SQLite database (creates file if it doesn't exist)."""
    return sqlite3.connect("grades.db")


def setup_database():
    """Create tables if they don't already exist."""
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT    NOT NULL,
            email   TEXT    UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER NOT NULL,
            subject     TEXT    NOT NULL,
            grade       REAL    NOT NULL CHECK(grade >= 0 AND grade <= 100),
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database ready.\n")


def add_student(name, email):
    """Insert a new student into the database."""
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        print(f"✅ Student '{name}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"⚠️  Email '{email}' already exists. Please use a different email.")
    finally:
        conn.close()


def view_students():
    """Display all students."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM students ORDER BY name")
    students = cursor.fetchall()
    conn.close()

    if not students:
        print("No students found.")
        return

    print(f"\n{'ID':<5} {'Name':<20} {'Email'}")
    print("-" * 45)
    for sid, name, email in students:
        print(f"{sid:<5} {name:<20} {email}")
    print()


def delete_student(student_id):
    """Delete a student and their grades."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    if deleted:
        print(f"✅ Student ID {student_id} deleted.")
    else:
        print(f"⚠️  No student found with ID {student_id}.")


def add_grade(student_id, subject, grade):
    """Add a grade for a student."""
    conn = connect()
    cursor = conn.cursor()

    # Check student exists
    cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if not student:
        print(f"⚠️  No student found with ID {student_id}.")
        conn.close()
        return

    try:
        cursor.execute(
            "INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)",
            (student_id, subject, grade)
        )
        conn.commit()
        print(f"✅ Grade {grade} added for {student[0]} in {subject}.")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def view_grades(student_id):
    """View all grades for a specific student with their average."""
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if not student:
        print(f"⚠️  No student found with ID {student_id}.")
        conn.close()
        return

    cursor.execute("""
        SELECT subject, grade
        FROM grades
        WHERE student_id = ?
        ORDER BY subject
    """, (student_id,))
    grades = cursor.fetchall()

    cursor.execute("""
        SELECT ROUND(AVG(grade), 2)
        FROM grades
        WHERE student_id = ?
    """, (student_id,))
    avg = cursor.fetchone()[0]

    conn.close()

    print(f"\n📋 Grades for: {student[0]}")
    print("-" * 30)

    if not grades:
        print("No grades recorded.")
    else:
        for subject, grade in grades:
            print(f"  {subject:<20} {grade}")
        print("-" * 30)
        print(f"  {'Average':<20} {avg}")
    print()


def top_students():
    """Show top students ranked by average grade."""
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.name, ROUND(AVG(g.grade), 2) AS avg_grade
        FROM students s
        JOIN grades g ON s.id = g.student_id
        GROUP BY s.id
        ORDER BY avg_grade DESC
    """)
    results = cursor.fetchall()
    conn.close()

    if not results:
        print("No grade data available yet.")
        return

    print(f"\n🏆 Top Students by Average Grade")
    print(f"{'Rank':<6} {'Name':<20} {'Average'}")
    print("-" * 35)
    for rank, (name, avg) in enumerate(results, 1):
        print(f"{rank:<6} {name:<20} {avg}")
    print()


def print_menu():
    print("\n========== GRADE TRACKER ==========")
    print("1. Add student")
    print("2. View all students")
    print("3. Delete student")
    print("4. Add grade")
    print("5. View student grades")
    print("6. View top students")
    print("0. Exit")
    print("====================================")


def main():
    setup_database()
    print("Welcome to the Student Grade Tracker!")

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name  = input("  Student name:  ").strip()
            email = input("  Student email: ").strip()
            if name and email:
                add_student(name, email)
            else:
                print("⚠️  Name and email cannot be empty.")

        elif choice == "2":
            view_students()

        elif choice == "3":
            view_students()
            try:
                sid = int(input("  Enter student ID to delete: "))
                delete_student(sid)
            except ValueError:
                print("⚠️  Please enter a valid number.")

        elif choice == "4":
            view_students()
            try:
                sid     = int(input("  Enter student ID: "))
                subject = input("  Subject name:    ").strip()
                grade   = float(input("  Grade (0-100):   "))
                if subject:
                    add_grade(sid, subject, grade)
                else:
                    print("⚠️  Subject cannot be empty.")
            except ValueError:
                print("⚠️  Please enter valid numbers for ID and grade.")

        elif choice == "5":
            view_students()
            try:
                sid = int(input("  Enter student ID: "))
                view_grades(sid)
            except ValueError:
                print("⚠️  Please enter a valid number.")

        elif choice == "6":
            top_students()

        elif choice == "0":
            print("👋 Goodbye!")
            break

        else:
            print("⚠️  Invalid option. Please try again.")


if __name__ == "__main__":
    main()
