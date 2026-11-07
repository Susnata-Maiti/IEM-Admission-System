"""
Database module for IEM Admission System
Supports Dual-Engine:
- MongoDB Atlas Cloud Database (Primary when .env MONGODB_URI is available)
- SQLite Database (Local offline fallback)
"""

import os
import sqlite3
import hashlib
import secrets
from datetime import datetime
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    root_env = Path(__file__).resolve().parent.parent / ".env"
    if root_env.exists():
        load_dotenv(dotenv_path=root_env)
    else:
        load_dotenv()
except ImportError:
    pass

# Serverless / Vercel Environment Compatibility
import tempfile
IS_VERCEL = bool(os.getenv("VERCEL"))

if IS_VERCEL:
    base_tmp = tempfile.gettempdir()
    UPLOADS_DIR = os.path.join(base_tmp, "uploads")
    DB_FILE = os.path.join(base_tmp, "iem_admission.db")
    source_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iem_admission.db")
    if os.path.exists(source_db) and not os.path.exists(DB_FILE):
        import shutil
        try:
            shutil.copy2(source_db, DB_FILE)
        except Exception as e:
            print(f"[DATABASE] Notice: Could not copy initial SQLite db to temp: {e}")
else:
    UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iem_admission.db")

try:
    os.makedirs(UPLOADS_DIR, exist_ok=True)
except OSError:
    UPLOADS_DIR = os.path.join(tempfile.gettempdir(), "uploads")
    os.makedirs(UPLOADS_DIR, exist_ok=True)

# Detect MongoDB Atlas
DB_ENGINE = "sqlite"
mongo_client = None
mongo_db = None

MONGO_URI = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI")

if MONGO_URI:
    try:
        import pymongo
        mongo_client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=4000)
        # Verify connection
        mongo_client.admin.command('ping')
        mongo_db = mongo_client.get_default_database("iem_admission")
        DB_ENGINE = "mongodb"
        print(f"[DATABASE] Connected to MongoDB Atlas Cloud Cluster (Database: '{mongo_db.name}')")
    except Exception as e:
        print(f"[DATABASE] MongoDB Atlas connection note: {e}")
        print("[DATABASE] Falling back to local SQLite database.")
        DB_ENGINE = "sqlite"
        mongo_client = None
        mongo_db = None
else:
    print("[DATABASE] Running in SQLite Mode (iem_admission.db).")


def get_db_engine():
    return DB_ENGINE


def get_db_connection():
    """Returns a SQLite connection for backward compatibility or SQLite mode."""
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


def clean_doc(doc):
    """Formats MongoDB documents for JSON serialization."""
    if not doc:
        return None
    d = dict(doc)
    if "_id" in d:
        d["_id"] = str(d["_id"])
    return d


# --------------------------------------------------------------------------
# Database Initialization & Seeding
# --------------------------------------------------------------------------

def init_db():
    if DB_ENGINE == "mongodb":
        init_mongodb()
    else:
        init_sqlite()


def init_sqlite():
    conn = get_db_connection()
    cursor = conn.cursor()

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

    cursor.execute("SELECT COUNT(*) as count FROM users")
    if cursor.fetchone()["count"] == 0:
        seed_sqlite_data(cursor, conn)

    conn.close()


def init_mongodb():
    if mongo_db is None:
        return
    if mongo_db.users.count_documents({}) == 0:
        seed_mongo_data()


def get_seed_records():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sample_pdf_path = os.path.join(UPLOADS_DIR, "sample_document.pdf")
    if not os.path.exists(sample_pdf_path):
        with open(sample_pdf_path, "wb") as f:
            f.write(b"%PDF-1.4\n1 0 obj\n<< /Title (IEM Sample Application Document) /Author (Nexus Team) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF")

    admin_hash, admin_salt = hash_password("Admin@2026!")
    director_hash, director_salt = hash_password("Director@2026!")

    students = [
        ("Priya Sharma", "priya.sharma@example.com", "Student@2026!", "+91 98765 43210", "15 Mar 2007", "Kolkata, WB",
         85.5, "CBSE", 78.0, "CBSE", 2025, "B.Tech Computer Science & Engineering (CSE)", "IEM-2026-0847", "Submitted", "12 Aug 2026 10:15:00"),
        ("Rahul Banerjee", "rahul.banerjee@example.com", "Student@2026!", "+91 98765 12345", "10 Jan 2007", "Salt Lake, Kolkata",
         92.0, "ICSE", 89.5, "ISC", 2025, "B.Tech Electronics & Communication Engineering (ECE)", "IEM-2026-0848", "Accepted", "11 Aug 2026 09:30:00"),
        ("Swapnil Ghosh", "swapnil.g@example.com", "Student@2026!", "+91 98765 22233", "22 Jul 2006", "New Town, Kolkata",
         81.0, "WB", 76.5, "WB", 2025, "Bachelor of Business Administration (BBA)", "IEM-2026-0849", "Under Review", "11 Aug 2026 14:20:00"),
        ("Monojit Das", "monojit.das@example.com", "Student@2026!", "+91 98765 44455", "05 Sep 2006", "Howrah, WB",
         65.0, "CBSE", 62.0, "CBSE", 2025, "B.Tech Mechanical Engineering (ME)", "IEM-2026-0850", "Rejected", "12 Aug 2026 11:00:00"),
        ("Ritabrata Chatterjee", "ritabrata.c@example.com", "Student@2026!", "+91 98765 66677", "18 Feb 2005", "Burdwan, WB",
         88.5, "CBSE", 84.0, "CBSE", 2024, "Master of Business Administration (MBA)", "IEM-2026-0851", "Under Review", "12 Aug 2026 16:45:00"),
        ("Debadrita Ray", "debadrita.ray@example.com", "Student@2026!", "+91 98765 88899", "12 Dec 2006", "Siliguri, WB",
         90.0, "ICSE", 88.0, "ISC", 2025, "Bachelor of Computer Applications (BCA)", "IEM-2026-0852", "Accepted", "13 Aug 2026 12:10:00"),
    ]
    return now, sample_pdf_path, admin_hash, admin_salt, director_hash, director_salt, students


def seed_sqlite_data(cursor, conn):
    now, sample_pdf_path, a_hash, a_salt, d_hash, d_salt, students = get_seed_records()

    cursor.execute("""
    INSERT INTO users (name, email, password_hash, salt, role, created_at)
    VALUES (?, ?, ?, ?, 'admin', ?)
    """, ("IEM Admission Office", "admin@iem.edu.in", a_hash, a_salt, now))

    cursor.execute("""
    INSERT INTO users (name, email, password_hash, salt, role, created_at)
    VALUES (?, ?, ?, ?, 'director', ?)
    """, ("Dr. Satyajit Chakrabarti", "director@iem.edu.in", d_hash, d_salt, now))

    for name, email, pwd, phone, dob, addr, c10m, c10b, c12m, c12b, yr, crs, code, status, sub_date in students:
        s_hash, s_salt = hash_password(pwd)
        cursor.execute("""
        INSERT INTO users (name, email, password_hash, salt, role, created_at)
        VALUES (?, ?, ?, ?, 'student', ?)
        """, (name, email, s_hash, s_salt, now))
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

        cursor.execute("""
        INSERT INTO audit_logs (application_id, changed_by, old_status, new_status, remarks, timestamp)
        VALUES (?, ?, 'Draft', 'Submitted', 'Initial student application submission', ?)
        """, (app_id, "System / Applicant", sub_date))

        if status != "Submitted":
            cursor.execute("""
            INSERT INTO audit_logs (application_id, changed_by, old_status, new_status, remarks, timestamp)
            VALUES (?, ?, 'Submitted', ?, ?, ?)
            """, (app_id, "admin@iem.edu.in", status, f"Application marked as {status}", now))

    conn.commit()


def seed_mongo_data():
    now, sample_pdf_path, a_hash, a_salt, d_hash, d_salt, students = get_seed_records()

    mongo_db.users.insert_one({
        "id": 1,
        "name": "IEM Admission Office",
        "email": "admin@iem.edu.in",
        "password_hash": a_hash,
        "salt": a_salt,
        "role": "admin",
        "created_at": now
    })

    mongo_db.users.insert_one({
        "id": 2,
        "name": "Dr. Satyajit Chakrabarti",
        "email": "director@iem.edu.in",
        "password_hash": d_hash,
        "salt": d_salt,
        "role": "director",
        "created_at": now
    })

    user_counter = 3
    app_counter = 1

    for name, email, pwd, phone, dob, addr, c10m, c10b, c12m, c12b, yr, crs, code, status, sub_date in students:
        s_hash, s_salt = hash_password(pwd)
        mongo_db.users.insert_one({
            "id": user_counter,
            "name": name,
            "email": email,
            "password_hash": s_hash,
            "salt": s_salt,
            "role": "student",
            "created_at": now
        })

        audit_trail = [
            {
                "id": 1,
                "changed_by": "System / Applicant",
                "old_status": "Draft",
                "new_status": "Submitted",
                "remarks": "Initial student application submission",
                "timestamp": sub_date
            }
        ]
        if status != "Submitted":
            audit_trail.append({
                "id": 2,
                "changed_by": "admin@iem.edu.in",
                "old_status": "Submitted",
                "new_status": status,
                "remarks": f"Application marked as {status}",
                "timestamp": now
            })

        mongo_db.applications.insert_one({
            "id": app_counter,
            "app_code": code,
            "user_id": user_counter,
            "full_name": name,
            "dob": dob,
            "contact_number": phone,
            "address": addr,
            "class_10_marks": c10m,
            "class_10_board": c10b,
            "class_12_marks": c12m,
            "class_12_board": c12b,
            "passing_year": yr,
            "course": crs,
            "doc_filename": "sample_document.pdf",
            "doc_filepath": sample_pdf_path,
            "status": status,
            "remarks": "Initial review verified" if status != "Submitted" else None,
            "submitted_at": sub_date,
            "created_at": sub_date,
            "updated_at": now,
            "audit_trail": audit_trail
        })

        user_counter += 1
        app_counter += 1


# --------------------------------------------------------------------------
# Unified CRUD Operations (Abstraction Layer)
# --------------------------------------------------------------------------

def get_user_by_email(email: str):
    email = email.strip().lower()
    if DB_ENGINE == "mongodb":
        user = mongo_db.users.find_one({"email": email})
        return clean_doc(user)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, password_hash, salt, role FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


def get_user_by_id(user_id: int):
    if DB_ENGINE == "mongodb":
        user = mongo_db.users.find_one({"id": user_id})
        return clean_doc(user)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, role FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


def create_student_user(name: str, email: str, pwd_hash: str, salt: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = name.strip()
    email = email.strip().lower()

    if DB_ENGINE == "mongodb":
        # Get next auto-increment id
        last_user = mongo_db.users.find_one(sort=[("id", -1)])
        user_id = (last_user["id"] + 1) if last_user and "id" in last_user else 1

        mongo_db.users.insert_one({
            "id": user_id,
            "name": name,
            "email": email,
            "password_hash": pwd_hash,
            "salt": salt,
            "role": "student",
            "created_at": now
        })

        app_code = f"IEM-{datetime.now().year}-{str(user_id).zfill(4)}"
        last_app = mongo_db.applications.find_one(sort=[("id", -1)])
        app_id = (last_app["id"] + 1) if last_app and "id" in last_app else 1

        mongo_db.applications.insert_one({
            "id": app_id,
            "app_code": app_code,
            "user_id": user_id,
            "full_name": name,
            "dob": "",
            "contact_number": "",
            "address": "",
            "class_10_marks": 0.0,
            "class_10_board": "",
            "class_12_marks": 0.0,
            "class_12_board": "",
            "passing_year": 2025,
            "course": "",
            "doc_filename": None,
            "doc_filepath": None,
            "status": "Draft",
            "remarks": None,
            "submitted_at": None,
            "created_at": now,
            "updated_at": now,
            "audit_trail": []
        })
        return user_id, app_code
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (name, email, password_hash, salt, role, created_at)
        VALUES (?, ?, ?, ?, 'student', ?)
        """, (name, email, pwd_hash, salt, now))
        user_id = cursor.lastrowid

        app_code = f"IEM-{datetime.now().year}-{str(user_id).zfill(4)}"
        cursor.execute("""
        INSERT INTO applications (
            app_code, user_id, full_name, dob, contact_number, address,
            class_10_marks, class_10_board, class_12_marks, class_12_board,
            passing_year, course, status, created_at, updated_at
        ) VALUES (?, ?, ?, '', '', '', 0.0, '', 0.0, '', 2025, '', 'Draft', ?, ?)
        """, (app_code, user_id, name, now, now))
        conn.commit()
        conn.close()
        return user_id, app_code


def get_student_application_by_user(user_id: int):
    if DB_ENGINE == "mongodb":
        app = mongo_db.applications.find_one({"user_id": user_id})
        return clean_doc(app)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        app_dict = dict(row)
        cursor.execute("SELECT * FROM audit_logs WHERE application_id = ? ORDER BY id ASC", (app_dict["id"],))
        app_dict["audit_trail"] = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return app_dict


def save_application_draft(user_id: int, req_data: dict):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_vals = {
        "full_name": req_data["full_name"].strip(),
        "dob": req_data["dob"].strip(),
        "contact_number": req_data["contact_number"].strip(),
        "address": req_data["address"].strip(),
        "class_10_marks": req_data["class_10_marks"],
        "class_10_board": req_data["class_10_board"].strip(),
        "class_12_marks": req_data["class_12_marks"],
        "class_12_board": req_data["class_12_board"].strip(),
        "passing_year": req_data["passing_year"],
        "course": req_data["course"].strip(),
        "updated_at": now
    }

    if DB_ENGINE == "mongodb":
        mongo_db.applications.update_one({"user_id": user_id}, {"$set": update_vals})
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE applications SET
            full_name = ?, dob = ?, contact_number = ?, address = ?,
            class_10_marks = ?, class_10_board = ?, class_12_marks = ?, class_12_board = ?,
            passing_year = ?, course = ?, updated_at = ?
        WHERE user_id = ?
        """, (
            update_vals["full_name"], update_vals["dob"], update_vals["contact_number"], update_vals["address"],
            update_vals["class_10_marks"], update_vals["class_10_board"], update_vals["class_12_marks"], update_vals["class_12_board"],
            update_vals["passing_year"], update_vals["course"], update_vals["updated_at"], user_id
        ))
        conn.commit()
        conn.close()


def update_document_upload(user_id: int, filename: str, filepath: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if DB_ENGINE == "mongodb":
        mongo_db.applications.update_one(
            {"user_id": user_id},
            {"$set": {"doc_filename": filename, "doc_filepath": filepath, "updated_at": now}}
        )
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE applications SET doc_filename = ?, doc_filepath = ?, updated_at = ?
        WHERE user_id = ?
        """, (filename, filepath, now, user_id))
        conn.commit()
        conn.close()


def submit_student_application(user_id: int, user_email: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if DB_ENGINE == "mongodb":
        app = mongo_db.applications.find_one({"user_id": user_id})
        if not app:
            return False
        audit_entry = {
            "id": len(app.get("audit_trail", [])) + 1,
            "changed_by": user_email,
            "old_status": "Draft",
            "new_status": "Submitted",
            "remarks": "Initial student application submission",
            "timestamp": now
        }
        mongo_db.applications.update_one(
            {"user_id": user_id},
            {
                "$set": {"status": "Submitted", "submitted_at": now, "updated_at": now},
                "$push": {"audit_trail": audit_entry}
            }
        )
        return True
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM applications WHERE user_id = ?", (user_id,))
        app_row = cursor.fetchone()
        if not app_row:
            conn.close()
            return False

        cursor.execute("""
        UPDATE applications SET status = 'Submitted', submitted_at = ?, updated_at = ?
        WHERE user_id = ?
        """, (now, now, user_id))

        cursor.execute("""
        INSERT INTO audit_logs (application_id, changed_by, old_status, new_status, remarks, timestamp)
        VALUES (?, ?, 'Draft', 'Submitted', 'Initial student application submission', ?)
        """, (app_row["id"], user_email, now))

        conn.commit()
        conn.close()
        return True


def get_document_info(app_id: int):
    if DB_ENGINE == "mongodb":
        app = mongo_db.applications.find_one({"id": app_id}, {"user_id": 1, "doc_filename": 1, "doc_filepath": 1})
        return clean_doc(app)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, doc_filename, doc_filepath FROM applications WHERE id = ?", (app_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


def admin_list_applications(status: str = None, course: str = None, search: str = None):
    if DB_ENGINE == "mongodb":
        query = {"status": {"$ne": "Draft"}}
        if status and status.strip():
            query["status"] = status.strip()
        if course and course.strip():
            query["course"] = {"$regex": course.strip(), "$options": "i"}
        if search and search.strip():
            s = search.strip()
            query["$or"] = [
                {"full_name": {"$regex": s, "$options": "i"}},
                {"app_code": {"$regex": s, "$options": "i"}},
                {"contact_number": {"$regex": s, "$options": "i"}}
            ]
        cursor = mongo_db.applications.find(query).sort("id", -1)
        return [clean_doc(d) for d in cursor]
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM applications WHERE status != 'Draft'"
        params = []
        if status and status.strip():
            query += " AND status = ?"
            params.append(status.strip())
        if course and course.strip():
            query += " AND course LIKE ?"
            params.append(f"%{course.strip()}%")
        if search and search.strip():
            term = f"%{search.strip()}%"
            query += " AND (full_name LIKE ? OR app_code LIKE ? OR contact_number LIKE ?)"
            params.extend([term, term, term])
        query += " ORDER BY id DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]


def admin_get_application(app_id: int):
    if DB_ENGINE == "mongodb":
        app = mongo_db.applications.find_one({"id": app_id})
        return clean_doc(app)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        app_dict = dict(row)
        cursor.execute("SELECT * FROM audit_logs WHERE application_id = ? ORDER BY id ASC", (app_id,))
        app_dict["audit_trail"] = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return app_dict


def admin_update_status(app_id: int, new_status: str, remarks: str, changed_by: str, current_status: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    remarks = remarks.strip() if remarks else ""

    if DB_ENGINE == "mongodb":
        app = mongo_db.applications.find_one({"id": app_id})
        audit_id = len(app.get("audit_trail", [])) + 1 if app else 1
        audit_entry = {
            "id": audit_id,
            "changed_by": changed_by,
            "old_status": current_status,
            "new_status": new_status,
            "remarks": remarks,
            "timestamp": now
        }
        mongo_db.applications.update_one(
            {"id": app_id},
            {
                "$set": {"status": new_status, "remarks": remarks, "updated_at": now},
                "$push": {"audit_trail": audit_entry}
            }
        )
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE applications SET status = ?, remarks = ?, updated_at = ?
        WHERE id = ?
        """, (new_status, remarks, now, app_id))

        cursor.execute("""
        INSERT INTO audit_logs (application_id, changed_by, old_status, new_status, remarks, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (app_id, changed_by, current_status, new_status, remarks, now))

        conn.commit()
        conn.close()


def admin_get_metrics():
    if DB_ENGINE == "mongodb":
        total = mongo_db.applications.count_documents({"status": {"$ne": "Draft"}})
        
        status_counts = {}
        for s in ["Submitted", "Under Review", "Accepted", "Rejected"]:
            status_counts[s] = mongo_db.applications.count_documents({"status": s})

        # By department/course aggregation
        pipeline = [
            {"$match": {"status": {"$ne": "Draft"}}},
            {"$group": {"_id": "$course", "count": {"$sum": 1}}}
        ]
        dept_counts = {item["_id"]: item["count"] for item in mongo_db.applications.aggregate(pipeline) if item["_id"]}

        return {
            "total": total,
            "submitted": status_counts.get("Submitted", 0),
            "under_review": status_counts.get("Under Review", 0),
            "accepted": status_counts.get("Accepted", 0),
            "rejected": status_counts.get("Rejected", 0),
            "by_department": dept_counts
        }
    else:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as total FROM applications WHERE status != 'Draft'")
        total = cursor.fetchone()["total"]

        cursor.execute("SELECT status, COUNT(*) as count FROM applications WHERE status != 'Draft' GROUP BY status")
        status_counts = {r["status"]: r["count"] for r in cursor.fetchall()}

        cursor.execute("SELECT course, COUNT(*) as count FROM applications WHERE status != 'Draft' GROUP BY course")
        dept_counts = {r["course"]: r["count"] for r in cursor.fetchall()}

        conn.close()

        return {
            "total": total,
            "submitted": status_counts.get("Submitted", 0),
            "under_review": status_counts.get("Under Review", 0),
            "accepted": status_counts.get("Accepted", 0),
            "rejected": status_counts.get("Rejected", 0),
            "by_department": dept_counts
        }


def admin_get_export_records(status: str = None, course: str = None):
    if DB_ENGINE == "mongodb":
        query = {"status": {"$ne": "Draft"}}
        if status and status.strip():
            query["status"] = status.strip()
        if course and course.strip():
            query["course"] = {"$regex": course.strip(), "$options": "i"}
        apps = mongo_db.applications.find(query).sort("id", -1)
        return [clean_doc(a) for a in apps]
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT app_code, full_name, dob, contact_number, course, class_10_marks, class_12_marks, status, submitted_at, remarks FROM applications WHERE status != 'Draft'"
        params = []
        if status and status.strip():
            query += " AND status = ?"
            params.append(status.strip())
        if course and course.strip():
            query += " AND course LIKE ?"
            params.append(f"%{course.strip()}%")
        query += " ORDER BY id DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]


if __name__ == "__main__":
    init_db()
    print(f"Database initialized in {DB_ENGINE.upper()} mode.")
