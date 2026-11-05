"""
FastAPI Main Application for IEM Admission System
Integrates all SRS Functional Requirements (FR-01 to FR-20),
NFR constraints, RBAC, document storage, and static frontend hosting.
"""

import os
import shutil
import io
import csv
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse

from database import init_db, get_db_connection, hash_password, verify_password, UPLOADS_DIR
from auth import (
    validate_password_strength,
    create_access_token,
    get_current_user,
    require_roles,
)
from models import RegisterRequest, LoginRequest, ApplicationDraftRequest, StatusUpdateRequest
from workflow import validate_status_transition, VALID_STATUSES

PREDEFINED_COURSES = [
    "B.Tech Computer Science & Engineering (CSE)",
    "B.Tech Electronics & Communication Engineering (ECE)",
    "B.Tech Information Technology (IT)",
    "B.Tech Electrical Engineering (EE)",
    "B.Tech Mechanical Engineering (ME)",
    "Bachelor of Computer Applications (BCA)",
    "Bachelor of Business Administration (BBA)",
    "Master of Business Administration (MBA)"
]

# Initialize Database on startup
init_db()

app = FastAPI(
    title="IEM Admission System API",
    description="Backend API for IEM Admission System (PCCCS504 SWE Lab)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")


# --------------------------------------------------------------------------
# Authentication Endpoints (FR-01, FR-02, FR-14, NFR-02)
# --------------------------------------------------------------------------

@app.post("/api/auth/register")
def register(req: RegisterRequest):
    """FR-01: Register new student account with validation and salted password hash."""
    is_valid, msg = validate_password_strength(req.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ?", (req.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    pwd_hash, salt = hash_password(req.password)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO users (name, email, password_hash, salt, role, created_at)
    VALUES (?, ?, ?, ?, 'student', ?)
    """, (req.name.strip(), req.email.strip(), pwd_hash, salt, now))
    user_id = cursor.lastrowid

    # Create empty draft application record
    app_code = f"IEM-{datetime.now().year}-{str(user_id).zfill(4)}"
    cursor.execute("""
    INSERT INTO applications (
        app_code, user_id, full_name, dob, contact_number, address,
        class_10_marks, class_10_board, class_12_marks, class_12_board,
        passing_year, course, status, created_at, updated_at
    ) VALUES (?, ?, ?, '', '', '', 0.0, '', 0.0, '', 2025, '', 'Draft', ?, ?)
    """, (app_code, user_id, req.name.strip(), now, now))

    conn.commit()
    conn.close()

    token = create_access_token(user_id, req.email, "student", req.name)
    return {
        "message": "Registration successful",
        "token": token,
        "user": {"id": user_id, "name": req.name, "email": req.email, "role": "student"}
    }


@app.post("/api/auth/login")
def login(req: LoginRequest):
    """FR-02, FR-14: Authenticate student, administrator, or director."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, password_hash, salt, role FROM users WHERE email = ?", (req.email.strip().lower(),))
    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(req.password, user["salt"], user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token(user["id"], user["email"], user["role"], user["name"])
    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }


@app.get("/api/auth/me")
def get_me(user: dict = Depends(get_current_user)):
    return {"user": user}


@app.get("/api/courses")
def get_courses():
    """FR-04, NFR-03: Predefined list of courses."""
    return {"courses": PREDEFINED_COURSES}


# --------------------------------------------------------------------------
# Student Application Endpoints (FR-03, FR-04, FR-05, FR-06, FR-08, FR-09, FR-10, FR-11)
# --------------------------------------------------------------------------

@app.get("/api/student/application")
def get_student_application(user: dict = Depends(require_roles(["student"]))):
    """FR-10, FR-11: Fetch current student's application."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications WHERE user_id = ?", (user["user_id"],))
    app_row = cursor.fetchone()

    if not app_row:
        conn.close()
        raise HTTPException(status_code=404, detail="No application record found.")

    app_dict = dict(app_row)

    # Fetch audit logs
    cursor.execute("SELECT * FROM audit_logs WHERE application_id = ? ORDER BY id ASC", (app_dict["id"],))
    logs = [dict(r) for r in cursor.fetchall()]
    app_dict["audit_trail"] = logs

    conn.close()
    return {"application": app_dict}


@app.post("/api/student/application/save")
def save_application_draft(req: ApplicationDraftRequest, user: dict = Depends(require_roles(["student"]))):
    """FR-03, FR-04, FR-09: Save application draft details (locked if already submitted)."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, status FROM applications WHERE user_id = ?", (user["user_id"],))
    app_row = cursor.fetchone()

    if not app_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Application record not found.")

    if app_row["status"] != "Draft":
        conn.close()
        # FR-09: Prevent editing after submission
        raise HTTPException(status_code=403, detail="Application is already submitted and locked against further edits.")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE applications SET
        full_name = ?,
        dob = ?,
        contact_number = ?,
        address = ?,
        class_10_marks = ?,
        class_10_board = ?,
        class_12_marks = ?,
        class_12_board = ?,
        passing_year = ?,
        course = ?,
        updated_at = ?
    WHERE user_id = ?
    """, (
        req.full_name.strip(),
        req.dob.strip(),
        req.contact_number.strip(),
        req.address.strip(),
        req.class_10_marks,
        req.class_10_board.strip(),
        req.class_12_marks,
        req.class_12_board.strip(),
        req.passing_year,
        req.course.strip(),
        now,
        user["user_id"]
    ))
    conn.commit()
    conn.close()

    return {"message": "Application draft saved successfully."}


@app.post("/api/student/application/upload")
async def upload_document(file: UploadFile = File(...), user: dict = Depends(require_roles(["student"]))):
    """FR-05, FR-06, FR-09, NFR-04: Upload supporting PDF document (up to 5MB)."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, status FROM applications WHERE user_id = ?", (user["user_id"],))
    app_row = cursor.fetchone()

    if not app_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Application record not found.")

    if app_row["status"] != "Draft":
        conn.close()
        raise HTTPException(status_code=403, detail="Application is locked. Cannot upload new documents after submission.")

    # Validate file type
    if not (file.filename.lower().endswith(".pdf") or file.content_type == "application/pdf"):
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF documents are accepted.")

    # Read content & validate file size (5MB max)
    content = await file.read()
    max_size = 5 * 1024 * 1024  # 5MB
    if len(content) > max_size:
        conn.close()
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")

    # Save to uploads folder
    safe_name = f"user_{user['user_id']}_{int(datetime.now().timestamp())}_{file.filename}"
    filepath = os.path.join(UPLOADS_DIR, safe_name)
    with open(filepath, "wb") as f:
        f.write(content)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE applications SET
        doc_filename = ?,
        doc_filepath = ?,
        updated_at = ?
    WHERE user_id = ?
    """, (file.filename, filepath, now, user["user_id"]))

    conn.commit()
    conn.close()

    return {"message": "Document uploaded successfully", "filename": file.filename}


@app.post("/api/student/application/submit")
def submit_application(user: dict = Depends(require_roles(["student"]))):
    """FR-08, FR-09: Review & Submit application. Sets status to 'Submitted' and locks."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications WHERE user_id = ?", (user["user_id"],))
    app_row = cursor.fetchone()

    if not app_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Application record not found.")

    if app_row["status"] != "Draft":
        conn.close()
        raise HTTPException(status_code=400, detail="Application is already submitted.")

    # Validate completeness
    missing_fields = []
    if not app_row["full_name"]: missing_fields.append("Full Name")
    if not app_row["dob"]: missing_fields.append("Date of Birth")
    if not app_row["contact_number"]: missing_fields.append("Contact Number")
    if not app_row["address"]: missing_fields.append("Address")
    if not app_row["course"]: missing_fields.append("Course Preference")
    if not app_row["doc_filepath"]: missing_fields.append("Supporting Document (PDF)")

    if missing_fields:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail=f"Cannot submit application. Missing required information: {', '.join(missing_fields)}"
        )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE applications SET
        status = 'Submitted',
        submitted_at = ?,
        updated_at = ?
    WHERE user_id = ?
    """, (now, now, user["user_id"]))

    # Record audit log
    cursor.execute("""
    INSERT INTO audit_logs (application_id, changed_by, old_status, new_status, remarks, timestamp)
    VALUES (?, ?, 'Draft', 'Submitted', 'Initial student application submission', ?)
    """, (app_row["id"], user["email"], now))

    conn.commit()
    conn.close()

    return {"message": "Application submitted successfully! Your application is now locked for review."}


# --------------------------------------------------------------------------
# Document Download Endpoint (FR-18)
# --------------------------------------------------------------------------

@app.get("/api/documents/{app_id}")
def get_document(app_id: int, user: dict = Depends(get_current_user)):
    """FR-18: Download or preview uploaded applicant PDF document with RBAC."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, doc_filename, doc_filepath FROM applications WHERE id = ?", (app_id,))
    app_row = cursor.fetchone()
    conn.close()

    if not app_row or not app_row["doc_filepath"]:
        raise HTTPException(status_code=404, detail="Document not found.")

    # Access check: user must be admin, director, or the student owner
    if user["role"] == "student" and user["user_id"] != app_row["user_id"]:
        raise HTTPException(status_code=403, detail="Forbidden: You can only view your own uploaded documents.")

    # Resolve document path dynamically so it remains fully portable if directory is moved
    doc_path = app_row["doc_filepath"]
    if not os.path.exists(doc_path):
        fallback_path = os.path.join(UPLOADS_DIR, os.path.basename(doc_path))
        if os.path.exists(fallback_path):
            doc_path = fallback_path
        else:
            raise HTTPException(status_code=404, detail="Document file missing from server storage.")

    return FileResponse(
        doc_path,
        media_type="application/pdf",
        filename=app_row["doc_filename"] or "application_document.pdf"
    )


# --------------------------------------------------------------------------
# Administrator & Director Endpoints (FR-12, FR-13, FR-15, FR-16, FR-17, FR-19, FR-20)
# --------------------------------------------------------------------------

@app.get("/api/admin/applications")
def list_applications(
    search: str = Query(None),
    course: str = Query(None),
    status: str = Query(None),
    user: dict = Depends(require_roles(["admin", "director"]))
):
    """FR-15, FR-16: View, search, and filter applications list."""
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

    return {"applications": [dict(r) for r in rows]}


@app.get("/api/admin/applications/{app_id}")
def get_application_detail(app_id: int, user: dict = Depends(require_roles(["admin", "director"]))):
    """FR-13, FR-17: View full application details and audit trail."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    app_row = cursor.fetchone()

    if not app_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Application not found.")

    app_dict = dict(app_row)

    # Fetch audit logs
    cursor.execute("SELECT * FROM audit_logs WHERE application_id = ? ORDER BY id ASC", (app_id,))
    logs = [dict(r) for r in cursor.fetchall()]
    app_dict["audit_trail"] = logs

    conn.close()
    return {"application": app_dict}


@app.patch("/api/admin/applications/{app_id}/status")
def update_application_status(
    app_id: int,
    req: StatusUpdateRequest,
    user: dict = Depends(require_roles(["admin"]))
):
    """FR-19, Module 3: Update application status with remarks and transition validation."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, status FROM applications WHERE id = ?", (app_id,))
    app_row = cursor.fetchone()

    if not app_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Application not found.")

    current_status = app_row["status"]
    new_status = req.new_status.strip()

    # Module 3 & Basis Path validation
    is_valid, reason = validate_status_transition(current_status, new_status, req.remarks or "")
    if not is_valid:
        conn.close()
        raise HTTPException(status_code=400, detail=reason)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE applications SET
        status = ?,
        remarks = ?,
        updated_at = ?
    WHERE id = ?
    """, (new_status, req.remarks.strip() if req.remarks else "", now, app_id))

    # Record in audit trail (FR-13)
    cursor.execute("""
    INSERT INTO audit_logs (application_id, changed_by, old_status, new_status, remarks, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (app_id, user["email"], current_status, new_status, req.remarks or "", now))

    conn.commit()
    conn.close()

    return {"message": f"Status successfully updated to '{new_status}'", "status": new_status}


@app.get("/api/admin/metrics")
def get_metrics(user: dict = Depends(require_roles(["admin", "director"]))):
    """FR-20, Module 4: Summary dashboard with status counts & dept distribution."""
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
        "metrics": {
            "total": total,
            "submitted": status_counts.get("Submitted", 0),
            "under_review": status_counts.get("Under Review", 0),
            "accepted": status_counts.get("Accepted", 0),
            "rejected": status_counts.get("Rejected", 0),
            "by_department": dept_counts
        }
    }


@app.get("/api/admin/export-csv")
def export_applications_csv(
    status: str = Query(None),
    course: str = Query(None),
    user: dict = Depends(require_roles(["admin", "director"]))
):
    """FR-12: Export full or filtered applications list to a CSV file."""
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

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Application ID", "Applicant Name", "DOB", "Contact Number", "Selected Course", "Class 10 (%)", "Class 12 (%)", "Status", "Submission Date", "Remarks"])

    for r in rows:
        writer.writerow([r["app_code"], r["full_name"], r["dob"], r["contact_number"], r["course"], r["class_10_marks"], r["class_12_marks"], r["status"], r["submitted_at"], r["remarks"] or ""])

    output.seek(0)
    filename = f"IEM_Admissions_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# --------------------------------------------------------------------------
# Mount Frontend Static Assets
# --------------------------------------------------------------------------

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
