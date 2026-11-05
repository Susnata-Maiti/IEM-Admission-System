# IEM Admission System Software
**PCCCS504 Software Engineering & Project Management Lab**  
**Team Nexus / P4**: Susnata Maiti (A-11), Sreejita Dey (A-29), Swapnil Ghosh (A-04), Debadrita Dutta (A-12)  
**Project Sponsor**: Dr. Satyajit Chakrabarti  

---

## 1. Project Overview & Scope
The **IEM Admission System** is a streamlined, user-focused web application engineered according to the Project Charter, Software Requirements Specification (SRS), and High-Level Design (HLD). It is built specifically for **Windows 11 desktop environments** running **Google Chrome** or **Microsoft Edge**.

### Core Modules Implemented (MEAN Stack POC Format):
1. **Module 1: Document Upload** — Direct PDF marksheet upload with client & server-side MIME and 5MB size limit validation. Stored on disk (`backend/uploads/`) with only the path reference held in the database.
2. **Module 2: Auth & Role-Based Access Control (RBAC)** — Student Applicant vs. Admissions Administrator vs. Executive Director login. Passwords protected with salted PBKDF2-HMAC-SHA256 cryptographic hashes; signed session tokens with server-side role enforcement (client guard is UX-only).
3. **Module 3: Status Transition Workflow** — State machine enforcing strict allowed transitions (`Draft` &rarr; `Submitted` &rarr; `Under Review` &rarr; `Accepted` / `Rejected`) with mandatory remarks on direct rejection and complete audit trails (`FR-13`).
4. **Module 4: Admin & Director Dashboard** — Real-time metrics aggregation counting submissions by status and course/department.

---

## 2. System Architecture & Request-Response Loop

The application strictly adheres to the 3-Tier Architecture specified in the HLD:

```
[ Client Browser (Chrome / Edge on Win 11) ]
                  │
          HTTP / REST (JSON)
                  ▼
[ Application Layer: FastAPI Backend Server ]
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
[ SQLite / MongoDB ]   [ Local Document Storage ]
  (Structured Data)         (PDF Files on Disk)
```

### The Request-Response Loop:
1. **Frontend Action**: The user fills in form data, selects a course, or uploads a document in the responsive SPA.
2. **HTTP Request**: The frontend issues a `fetch` REST call (e.g., `POST /api/student/application/save` or `PATCH /api/admin/applications/{id}/status`) carrying JSON data and a Bearer authorization token.
3. **API Routing & Middleware**: The FastAPI router validates payload types with Pydantic schemas and verifies authorization and roles server-side.
4. **Business Logic & State Machine**: Business rules (such as password policies, PDF size limits, or allowed status transitions) are executed.
5. **Persistence**: The backend executes parameterized queries against SQLite (or MongoDB Mongoose queries) and writes file streams to the upload directory.
6. **JSON Response**: The backend returns HTTP status codes with structured JSON confirmation or error messages.
7. **UI Update**: The frontend immediately updates the DOM, moves steppers, updates progress badges, and displays toast alerts.

---

## 3. Demo Accounts & Credentials

Pre-seeded credentials are provided for rapid in-lab demonstrations:

| Role | Name | Email Address | Password | Privileges |
| :--- | :--- | :--- | :--- | :--- |
| **Student** | Priya Sharma | `priya.sharma@example.com` | `Student@2026!` | View submitted application, track status, download marksheet. |
| **New Student** | Self-Registered | Any valid email | Pass with uppercase & special char | Fill 4-step wizard, upload PDF, submit and lock. |
| **Admin** | IEM Admission Office | `admin@iem.edu.in` | `Admin@2026!` | Search/filter, Table/Card views, status transitions, remarks, CSV export. |
| **Director** | Dr. Satyajit Chakrabarti | `director@iem.edu.in` | `Director@2026!` | Executive read-only high-level metrics dashboard & application monitoring. |

---

## 4. Setup and Run Instructions (Windows 11)

### Prerequisites:
- Python 3.10+ (Installed on system `PATH`).
- Google Chrome or Microsoft Edge on Windows 11.

### Step 1: Clone / Navigate to Directory
```powershell
git clone https://github.com/Susnata-Maiti/IEM-Admission-System.git
cd IEM-Admission-System
```

### Step 2: One-Click Execution
Double-click `run_server.bat` or run via PowerShell:
```powershell
python run_server.py
```

The script will automatically:
1. Initialize the SQLite database `backend/iem_admission.db` and seed demo records.
2. Start the Uvicorn web server at `http://127.0.0.1:8000`.
3. Launch your default browser (Chrome or Edge) pointing to `http://127.0.0.1:8000`.

### Step 3: Run the Automated Test Suite
To verify unit tests, Basis Path testing, and boundary validations:
```powershell
python backend/test_suite.py
```
*(All 16 tests will run and report `OK`)*.

---

## 5. Deliverables Directory Structure

```
IEM Admission System/
├── backend/
│   ├── app.py                # FastAPI REST API & Static File Server
│   ├── auth.py               # Cryptographic Hash & JWT/Token RBAC
│   ├── database.py           # SQLite connection, schema, and demo seed data
│   ├── models.py             # Pydantic validation schemas
│   ├── workflow.py           # State machine & status transition validator (Basis Path module)
│   ├── test_suite.py         # Automated unit & integration tests
│   └── uploads/              # Document storage for uploaded PDF files
├── frontend/
│   ├── index.html            # Responsive UI with Stepper Wizard, Card/Table Views, Modals
│   ├── styles.css            # Modern aesthetic styling, colors, and responsive layouts
│   └── app.js                # Frontend client logic, state management, REST integration
├── mean_stack_equivalent/    # Canonical MEAN implementation for assignment reference
│   ├── server/               # Express.js + Mongoose + Multer + JWT
│   └── client/               # Angular 17+ Service & Component Templates
├── docs/
│   ├── README.md             # Setup & Architecture Document
│   ├── TECHNICAL_WRITEUP.md  # 1–2 page Technical Write-up (Deliverable 3)
│   └── SOFTWARE_TEST_STRATEGY_AND_TEST_PLAN.md # Filled-in Test Plan Template
├── .gitignore                # Git exclusions (ignoring caches, databases, etc.)
├── README.md                 # Root Repository Documentation
├── run_server.py             # One-click Python launcher
└── run_server.bat            # Windows 1-click batch launcher
```
