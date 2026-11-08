"""
FastAPI Main Application for IEM Admission System
Integrates all SRS Functional Requirements (FR-01 to FR-20),
NFR constraints, RBAC, document storage, and static frontend hosting.
Supports dual-engine storage (MongoDB Atlas Cloud & local SQLite fallback).
"""

import os
import io
import csv
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import (
    init_db,
    hash_password,
    verify_password,
    UPLOADS_DIR,
    get_db_engine,
    get_user_by_email,
    get_user_by_id,
    create_student_user,
    get_student_application_by_user,
    save_application_draft,
    update_document_upload,
    submit_student_application,
    get_document_info,
    admin_list_applications,
    admin_get_application,
    admin_update_status,
    admin_get_metrics,
    admin_get_export_records,
)
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
    if not req.email.strip().lower().endswith("@gmail.com"):
        raise HTTPException(status_code=400, detail="Registration is restricted to Gmail accounts (@gmail.com).")

    is_valid, msg = validate_password_strength(req.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)

    if get_user_by_email(req.email):
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    pwd_hash, salt = hash_password(req.password)
    user_id, app_code = create_student_user(req.name, req.email, pwd_hash, salt)

    token = create_access_token(user_id, req.email, "student", req.name)
    return {
        "message": "Registration successful",
        "token": token,
        "user": {"id": user_id, "name": req.name, "email": req.email, "role": "student"}
    }


@app.post("/api/auth/login")
def login(req: LoginRequest):
    """FR-02, FR-14: Authenticate student, administrator, or director."""
    user = get_user_by_email(req.email)
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
    return {"user": user, "db_engine": get_db_engine()}


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
    app_dict = get_student_application_by_user(user["user_id"])
    if not app_dict:
        raise HTTPException(status_code=404, detail="No application record found.")
    return {"application": app_dict}


@app.post("/api/student/application/save")
def save_draft(req: ApplicationDraftRequest, user: dict = Depends(require_roles(["student"]))):
    """FR-03, FR-04, FR-09: Save application draft details (locked if already submitted)."""
    app_dict = get_student_application_by_user(user["user_id"])
    if not app_dict:
        raise HTTPException(status_code=404, detail="Application record not found.")

    if app_dict.get("status") != "Draft":
        raise HTTPException(status_code=403, detail="Application is already submitted and locked against further edits.")

    save_application_draft(user["user_id"], req.model_dump())
    return {"message": "Application draft saved successfully."}


@app.post("/api/student/application/upload")
async def upload_document(file: UploadFile = File(...), user: dict = Depends(require_roles(["student"]))):
    """FR-05, FR-06, FR-09, NFR-04: Upload supporting PDF document (up to 5MB)."""
    app_dict = get_student_application_by_user(user["user_id"])
    if not app_dict:
        raise HTTPException(status_code=404, detail="Application record not found.")

    if app_dict.get("status") != "Draft":
        raise HTTPException(status_code=403, detail="Application is locked. Cannot upload new documents after submission.")

    # Validate file type
    if not (file.filename.lower().endswith(".pdf") or file.content_type == "application/pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF documents are accepted.")

    # Read content & validate file size (5MB max)
    content = await file.read()
    max_size = 5 * 1024 * 1024  # 5MB
    if len(content) > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")

    # Save to uploads folder
    safe_name = f"user_{user['user_id']}_{int(datetime.now().timestamp())}_{file.filename}"
    filepath = os.path.join(UPLOADS_DIR, safe_name)
    with open(filepath, "wb") as f:
        f.write(content)

    update_document_upload(user["user_id"], file.filename, filepath)
    return {"message": "Document uploaded successfully", "filename": file.filename}


@app.post("/api/student/application/submit")
def submit_application(user: dict = Depends(require_roles(["student"]))):
    """FR-08, FR-09: Review & Submit application. Sets status to 'Submitted' and locks."""
    app_dict = get_student_application_by_user(user["user_id"])
    if not app_dict:
        raise HTTPException(status_code=404, detail="Application record not found.")

    if app_dict.get("status") != "Draft":
        raise HTTPException(status_code=400, detail="Application is already submitted.")

    # Validate completeness
    missing_fields = []
    if not app_dict.get("full_name"): missing_fields.append("Full Name")
    if not app_dict.get("dob"): missing_fields.append("Date of Birth")
    if not app_dict.get("contact_number"): missing_fields.append("Contact Number")
    if not app_dict.get("address"): missing_fields.append("Address")
    if not app_dict.get("course"): missing_fields.append("Course Preference")
    if not app_dict.get("doc_filepath"): missing_fields.append("Supporting Document (PDF)")

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot submit application. Missing required information: {', '.join(missing_fields)}"
        )

    submit_student_application(user["user_id"], user["email"])
    return {"message": "Application submitted successfully! Your application is now locked for review."}


# --------------------------------------------------------------------------
# Document Download Endpoint (FR-18)
# --------------------------------------------------------------------------

@app.get("/api/documents/{app_id}")
def get_document(app_id: int, user: dict = Depends(get_current_user)):
    """FR-18: Download or preview uploaded applicant PDF document with RBAC."""
    doc_info = get_document_info(app_id)
    if not doc_info or not doc_info.get("doc_filepath"):
        raise HTTPException(status_code=404, detail="Document not found.")

    if user["role"] == "student" and user["user_id"] != doc_info.get("user_id"):
        raise HTTPException(status_code=403, detail="Forbidden: You can only view your own uploaded documents.")

    doc_path = doc_info["doc_filepath"]
    if not os.path.exists(doc_path):
        fallback_path = os.path.join(UPLOADS_DIR, os.path.basename(doc_path))
        if os.path.exists(fallback_path):
            doc_path = fallback_path
        else:
            raise HTTPException(status_code=404, detail="Document file missing from server storage.")

    return FileResponse(
        doc_path,
        media_type="application/pdf",
        filename=doc_info.get("doc_filename") or "application_document.pdf"
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
    apps = admin_list_applications(status=status, course=course, search=search)
    return {"applications": apps}


@app.get("/api/admin/applications/{app_id}")
def get_application_detail(app_id: int, user: dict = Depends(require_roles(["admin", "director"]))):
    """FR-13, FR-17: View full application details and audit trail."""
    app_dict = admin_get_application(app_id)
    if not app_dict:
        raise HTTPException(status_code=404, detail="Application not found.")
    return {"application": app_dict}


@app.patch("/api/admin/applications/{app_id}/status")
def update_application_status(
    app_id: int,
    req: StatusUpdateRequest,
    user: dict = Depends(require_roles(["admin"]))
):
    """FR-19, Module 3: Update application status with remarks and transition validation."""
    app_dict = admin_get_application(app_id)
    if not app_dict:
        raise HTTPException(status_code=404, detail="Application not found.")

    current_status = app_dict["status"]
    new_status = req.new_status.strip()

    is_valid, reason = validate_status_transition(current_status, new_status, req.remarks or "")
    if not is_valid:
        raise HTTPException(status_code=400, detail=reason)

    admin_update_status(app_id, new_status, req.remarks or "", user["email"], current_status)
    return {"message": f"Status successfully updated to '{new_status}'", "status": new_status}


@app.get("/api/admin/metrics")
def get_metrics(user: dict = Depends(require_roles(["admin", "director"]))):
    """FR-20, Module 4: Summary dashboard with status counts & dept distribution."""
    metrics = admin_get_metrics()
    return {"metrics": metrics}


@app.get("/api/admin/export-csv")
def export_applications_csv(
    status: str = Query(None),
    course: str = Query(None),
    user: dict = Depends(require_roles(["admin", "director"]))
):
    """FR-12: Export full or filtered applications list to a CSV file."""
    rows = admin_get_export_records(status=status, course=course)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Application ID", "Applicant Name", "DOB", "Contact Number", "Selected Course", "Class 10 (%)", "Class 12 (%)", "Status", "Submission Date", "Remarks"])

    for r in rows:
        writer.writerow([
            r.get("app_code", ""),
            r.get("full_name", ""),
            r.get("dob", ""),
            r.get("contact_number", ""),
            r.get("course", ""),
            r.get("class_10_marks", 0),
            r.get("class_12_marks", 0),
            r.get("status", ""),
            r.get("submitted_at", ""),
            r.get("remarks") or ""
        ])

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
