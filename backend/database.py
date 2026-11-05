"""
Database module for IEM Admission System
Handles SQLite connection, schema creation, and seeding of initial demo data.
"""

import sqlite3
import os
import hashlib
import secrets
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iem_admission.db")
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

os.makedirs(UPLOADS_DIR, exist_ok=True)


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Generates a salted cryptographic hash using PBKDF2-HMAC-SHA256 (NFR-02)."""
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return key.hex(), salt


def verify_password(password: str, salt: str, password_hash: str) -> bool:
    new_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(new_hash, password_hash)


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('student', 'admin', 'director')),
        created_at TEXT NOT NULL
    );
    """)

    # Applications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_code TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        dob TEXT NOT NULL,
        contact_number TEXT NOT NULL,
        address TEXT NOT NULL,
        class_10_marks REAL NOT NULL,
        class_10_board TEXT NOT NULL,
        class_12_marks REAL NOT NULL,
        class_12_board TEXT NOT NULL,
        passing_year INTEGER NOT NULL,
        course TEXT NOT NULL,
        doc_filename TEXT,
        doc_filepath TEXT,
        status TEXT NOT NULL CHECK(status IN ('Draft', 'Submitted', 'Under Review', 'Accepted', 'Rejected')),
        remarks TEXT,
        submitted_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    # Audit Trail table (FR-13)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id INTEGER NOT NULL,
        changed_by TEXT NOT NULL,
        old_status TEXT NOT NULL,
        new_status TEXT NOT NULL,
        remarks TEXT,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (application_id) REFERENCES applications (id)
    );
    """)

    conn.commit()

    # Seed initial users & demo applications if table is empty
    cursor.execute("SELECT COUNT(*) as count FROM users")
    if cursor.fetchone()["count"] == 0:
        seed_data(cursor, conn)

    conn.close()


def seed_data(cursor, conn):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Sample PDF create for demo
    sample_pdf_path = os.path.join(UPLOADS_DIR, "sample_document.pdf")
    if not os.path.exists(sample_pdf_path):
        with open(sample_pdf_path, "wb") as f:
            f.write(b"%PDF-1.4\n1 0 obj\n<< /Title (IEM Sample Application Document) /Author (Nexus Team) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF")

    # 1. Admin
    admin_hash, admin_salt = hash_password("Admin@2026!")
    cursor.execute("""
    INSERT INTO users (name, email, password_hash, salt, role, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, ("IEM Admission Office", "admin@iem.edu.in", admin_hash, admin_salt, "admin", now))

    # 2. Director (Executive Sponsor Dr. Satyajit Chakrabarti)
    director_hash, director_salt = hash_password("Director@2026!")
    cursor.execute("""
    INSERT INTO users (name, email, password_hash, salt, role, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, ("Dr. Satyajit Chakrabarti", "director@iem.edu.in", director_hash, director_salt, "director", now))

    # 3. Demo Students
    students = [
        ("Priya Sharma", "priya.sharma@example.com", "Student@2026!", "+91 98765 43210", "15 Mar 2007", "Kolkata, WB",
         85.5, "CBSE", 78.0, "CBSE", 2025, "B.Tech CSE", "IEM-2026-0847", "Submitted", "12 Aug 2026 10:15:00"),
        ("Rahul Banerjee", "rahul.banerjee@example.com", "Student@2026!", "+91 98765 12345", "10 Jan 2007", "Salt Lake, Kolkata",
         92.0, "ICSE", 89.5, "ISC", 2025, "B.Tech ECE", "IEM-2026-0848", "Accepted", "11 Aug 2026 09:30:00"),
        ("Swapnil Ghosh", "swapnil.g@example.com", "Student@2026!", "+91 98765 22233", "22 Jul 2006", "New Town, Kolkata",
         81.0, "WB", 76.5, "WB", 2025, "BBA", "IEM-2026-0849", "Under Review", "11 Aug 2026 14:20:00"),
        ("Monojit Das", "monojit.das@example.com", "Student@2026!", "+91 98765 44455", "05 Sep 2006", "Howrah, WB",
         65.0, "CBSE", 62.0, "CBSE", 2025, "B.Tech Mechanical", "IEM-2026-0850", "Rejected", "12 Aug 2026 11:00:00"),
        ("Ritabrata Chatterjee", "ritabrata.c@example.com", "Student@2026!", "+91 98765 66677", "18 Feb 2005", "Burdwan, WB",
         88.5, "CBSE", 84.0, "CBSE", 2024, "MBA", "IEM-2026-0851", "Under Review", "12 Aug 2026 16:45:00"),
        ("Debadrita Ray", "debadrita.ray@example.com", "Student@2026!", "+91 98765 88899", "12 Dec 2006", "Siliguri, WB",
         90.0, "ICSE", 88.0, "ISC", 2025, "BCA", "IEM-2026-0852", "Accepted", "13 Aug 2026 12:10:00"),
    ]

    for name, email, pwd, phone, dob, addr, c10m, c10b, c12m, c12b, yr, crs, code, status, sub_date in students:
        s_hash, s_salt = hash_password(pwd)
        cursor.execute("""
        INSERT INTO users (name, email, password_hash, salt, role, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, s_hash, s_salt, "student", now))
        user_id = cursor.lastrowid

        cursor.execute("""
        INSERT INTO applications (
            app_code, user_id, full_name, dob, contact_number, address,
            class_10_marks, class_10_board, class_12_marks, class_12_board,
            passing_year, course, doc_filename, doc_filepath, status,
            remarks, submitted_at, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            code, user_id, name, dob, phone, addr,
            c10m, c10b, c12m, c12b, yr, crs,
            "sample_document.pdf", sample_pdf_path, status,
            "Initial review verified" if status != "Submitted" else None,
            sub_date, sub_date, now
        ))
        app_id = cursor.lastrowid

        # Insert audit trail entry
        cursor.execute("""
        INSERT INTO audit_logs (application_id, changed_by, old_status, new_status, remarks, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (app_id, "System / Applicant", "Draft", "Submitted", "Application submitted online", sub_date))

        if status != "Submitted":
            cursor.execute("""
            INSERT INTO audit_logs (application_id, changed_by, old_status, new_status, remarks, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (app_id, "admin@iem.edu.in", "Submitted", status, f"Application marked as {status}", now))

    conn.commit()


if __name__ == "__main__":
    init_db()
    print("Database initialized and seeded successfully.")
