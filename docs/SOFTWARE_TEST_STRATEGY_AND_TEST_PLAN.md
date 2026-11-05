# Software Test Strategy and Test Plan
**Project / System Name**: IEM Admission System Software  
**Team**: Nexus / Team P4 (Susnata Maiti, Sreejita Dey, Swapnil Ghosh, Debadrita Dutta)  
**Academic Year / Semester**: 2026–27 / 5th Semester  
**Target Platform**: Windows 11 Desktop (Google Chrome & Microsoft Edge)  

---

# PART A — SOFTWARE TEST STRATEGY DOCUMENT

## A.1 Introduction and Objectives
The purpose of this Software Test Strategy is to define the testing methodology, levels, techniques, and governance required to ensure that the **IEM Admission System Software** conforms strictly to its Project Charter, Software Requirements Specification (SRS), and High-Level Design (HLD).

### Overall Objectives:
- **Verification**: Ensure that each subsystem (authentication, form validation, document upload, status workflow, and administrative analytics) is constructed according to its formal specifications (`FR-01` to `FR-20`).
- **Validation**: Ensure that the software satisfies the real-world operational needs of student applicants, admission staff, and executive directors under Windows 11 desktop environments running Google Chrome or Microsoft Edge.
- **Quality Targets**: Achieve zero severity-1 (blocking) defects, guarantee 100% Basis Path coverage on the state transition engine, and ensure that PDF document uploads and dashboard data loading meet the latency and reliability benchmarks specified in `NFR-01` through `NFR-05`.

---

## A.2 Scope
This test strategy applies to the following modules and subsystems:
1. **Student Authentication & RBAC Subsystem** (`FR-01`, `FR-02`, `NFR-02`).
2. **Student Admission Wizard & Form Validation Subsystem** (`FR-03`, `FR-04`, `FR-07`).
3. **Document Management & Storage Subsystem** (`FR-05`, `FR-06`, `FR-18`, `NFR-04`).
4. **Application Submission & State Locking Engine** (`FR-08`, `FR-09`, `FR-10`, `FR-11`).
5. **Administrative Applications Workspace & View Modes** (`FR-14`, `FR-15`, `FR-16`, `FR-17`, `NFR-03`).
6. **Workflow State Transition & Audit Trail Subsystem** (`FR-13`, `FR-19`, Module 3).
7. **Summary Analytics Dashboard & CSV Reporting Engine** (`FR-12`, `FR-20`, Module 4).

*(Out of Scope: Payment gateway processing, SMS/OTP gateways, mobile responsive viewports below 1366×768, and AI-based admissions ranking).*

---

## A.3 Levels of Testing

### A.3.1 Unit Testing
- **Approach**: Individual Python functions, Pydantic validation schemas, and cryptographic helper methods are tested in complete isolation using the standard `unittest` framework.
- **Key Modules Tested**: Password strength checker (`validate_password_strength`), PBKDF2 hashing routines (`hash_password`, `verify_password`), and the workflow transition state validator (`validate_status_transition`).
- **Ownership**: Sreejita Dey (Backend) and Debadrita Dutta (Testing).

### A.3.2 Integration Testing
- **Approach**: A sandwich (hybrid) integration strategy is applied. The data persistence layer (SQLite) and business logic modules are integrated bottom-up, while the client presentation layer communicates top-down with the FastAPI REST API gateway.
- **Stubs & Drivers**: Mock PDF byte streams and lightweight mock JWT authentication headers are utilized to verify endpoint request-response loops without external dependencies.
- **Ownership**: Susnata Maiti (Frontend/Integration) and Sreejita Dey (Backend).

### A.3.3 System Testing
- **Approach**: End-to-end black-box testing of the fully integrated software executing on Windows 11 desktop environments in Google Chrome and Microsoft Edge. System scenarios simulate full applicant lifecycles from initial registration to administrative review, status transition, document preview, and final CSV reporting.
- **Ownership**: Debadrita Dutta (Testing Lead) and Susnata Maiti.

### A.3.4 Acceptance Testing
- **Approach**: Conducted in two stages:
  - **Alpha Testing**: Conducted internally by Team Nexus to verify all 20 functional requirements and the 5 non-functional requirements.
  - **Beta / Sponsor Evaluation**: Performed with simulated faculty admission officers and the executive project sponsor, Dr. Satyajit Chakrabarti, verifying usability, performance, and role-based access boundaries.

---

## A.4 Testing Techniques Used for Test-Case Design

### A.4.1 Black-Box Techniques
1. **Equivalence Class Partitioning (ECP)**: Applied to input fields such as password length/complexity, contact number format, and applicant age/academic marks to divide input domains into valid and invalid equivalence partitions.
2. **Boundary Value Analysis (BVA)**: Applied to academic mark percentage inputs ($0.0\%$ to $100.0\%$), password length thresholds (7, 8, 9 characters), and uploaded PDF document file sizes ($4.99\text{ MB}$, $5.00\text{ MB}$, $5.01\text{ MB}$).
3. **Decision Table Testing**: Applied to multi-condition business policies, specifically the conditions governing whether an application can transition to "Rejected" directly from "Submitted" based on role, status, and mandatory explanatory remarks.
4. **State Transition Testing**: Applied to the application lifecycle model (`Draft` &rarr; `Submitted` &rarr; `Under Review` &rarr; `Accepted` / `Rejected`) to verify that invalid state traversals are rejected by the server.

### A.4.2 White-Box Techniques
1. **Statement Coverage**: Applied to `workflow.py` and `auth.py` ensuring that every executable line of code is triggered during automated unit execution.
2. **Branch / Decision Coverage**: Applied to every conditional branch (`if`, `elif`, `else`) across validation rules to ensure both true and false paths are exercised.
3. **Basis Path Testing**: Formal cyclomatic complexity calculation and control flow graph (CFG) analysis applied to `validate_status_transition()` in `backend/workflow.py`, ensuring all linearly independent paths are executed.

---

## A.5 Testing Types
- **Functional Testing**: Verifies that every screen, button, dropdown, form field, and endpoint operates in accordance with `FR-01` through `FR-20`.
- **Regression Testing**: Automated execution of the test suite (`backend/test_suite.py`) triggered whenever code modifications or bug fixes are applied to the backend or frontend.
- **Performance / Load Testing**: Benchmarking application response latencies on Windows 11 Chrome/Edge under typical campus network simulations, verifying that the student dashboard loads in $<3$ seconds (`NFR-01`) and the administrative list loads in $<2$ seconds (`NFR-03`).
- **Security Testing**: Verification of salted cryptographic hashing (`NFR-02`), token tampering detection, server-side RBAC restriction, and prevention of privilege escalation.
- **Usability Testing**: Verification of dual view modes (compact table vs. detailed card view, `NFR-03`), clear field-level error messages (`FR-07`), and intuitive navigation.

---

## A.6 Debugging Approach
When a defect is identified during test execution:
1. **Cause Elimination**: The test failure is isolated using automated test runners and FastAPI server console logs to identify the exact failing assertion or stack trace.
2. **Backtracking**: The call stack is traced from the UI client action through the REST payload to the backend routing and database layer.
3. **Fix Verification**: Once corrected, the specific unit test is re-executed, followed by the entire automated regression suite to ensure no side-effects were introduced.

---

## A.7 Entry and Exit Criteria

| Testing Level | Entry Criteria | Exit Criteria |
| :--- | :--- | :--- |
| **Unit Testing** | Individual Python source files (`auth.py`, `workflow.py`, `models.py`) written and compiling without syntax errors. | 100% of unit tests pass in `backend/test_suite.py`; zero unhandled exceptions. |
| **Integration Testing** | SQLite database schema initialized; REST API endpoints exposed and unit-tested. | All frontend API calls receive expected HTTP 200/400/403 responses; file uploads persist to disk. |
| **System Testing** | Complete application running via `run_server.py`; frontend assets linked. | All 20 Functional Requirements verified; zero Sev-1 or Sev-2 bugs open; NFR thresholds met. |
| **Acceptance Testing** | System testing signed off; live demo script prepared. | Sponsor and evaluation panel confirm that acceptance criteria from Project Charter are satisfied. |

---

## A.8 Roles and Responsibilities

| Role | Team Member | Primary Responsibility |
| :--- | :--- | :--- |
| **Developer (Frontend / UI)** | Susnata Maiti (A-11) | Implementation of frontend SPA, client validation, wireframe fidelity, and API client integration. |
| **Developer (Backend / API)** | Sreejita Dey (A-29) | Implementation of FastAPI endpoints, RBAC authentication, Multer/upload storage, and state machine. |
| **Database & Storage Engineer** | Swapnil Ghosh (A-04) | SQLite schema design, seed data scripting, document storage integrity, and aggregation queries. |
| **Test Lead & Documentation** | Debadrita Dutta (A-12) | Authoring test strategy/plan, designing test cases (BVA, ECP, Basis Path), and executing test suites. |
| **Client / Sponsor Representative** | Dr. Satyajit Chakrabarti | Executive project oversight, review of acceptance criteria, and sign-off on admission workflows. |

---

## A.9 Test Tools and Environment
- **Hardware / OS**: Windows 11 Professional (64-bit), x86_64, 16GB RAM.
- **Client Browsers**: Google Chrome (v124+), Microsoft Edge (v124+).
- **Backend Runtime**: Python 3.14.5 with FastAPI 0.162.0 and Uvicorn 0.54.0.
- **Test Execution Framework**: Python standard `unittest` library and Starlette TestClient.
- **Storage / Database**: SQLite 3 with local filesystem document repository (`backend/uploads/`).
- **Defect Tracking**: GitHub Issues and shared project spreadsheet.

---

## A.10 Risk-Based Considerations
1. **Risk 1: File Upload Exploit or Storage Exhaustion (High)**  
   *Reasoning*: Unrestricted document uploads pose risks of server storage saturation or malicious script injection.  
   *Mitigation*: Extra test effort is dedicated to BVA testing on file size boundaries (strictly capping files at 5.0MB) and enforcing MIME/extension validation (`.pdf` only).
2. **Risk 2: Unauthorized Status Alterations or Data Tampering (High)**  
   *Reasoning*: Allowing unauthorized role transitions or modifications to submitted student applications invalidates admission integrity.  
   *Mitigation*: Rigorous automated negative test cases verify that student accounts cannot edit submitted applications (`FR-09`) and that client guards cannot be bypassed without server-side role tokens (`NFR-02`).
3. **Risk 3: Integration Synchronization over Compressed 20-Day Timeline (Medium)**  
   *Reasoning*: Frontend-backend communication mismatches could delay project milestones.  
   *Mitigation*: Standardized REST/JSON contract definitions and direct integration tests ensure clean end-to-end communication from Day 16.

---

# PART B — SOFTWARE TEST PLAN

## B.1 Test Plan Identifier
`TP-IEM-ADM-2026-V1.0`

## B.2 Objective
This test plan specifies the concrete test cases, input parameters, expected outcomes, and white-box control flow coverage required to rigorously validate the **IEM Admission System Software** against the functional and non-functional specifications documented in the Project Charter, SRS, and HLD.

## B.3 Features to be Tested
- Student Account Registration with password complexity checks (`FR-01`).
- Multi-role Authentication and JWT Session Management (`FR-02`, `FR-14`).
- Multi-step Admission Form Entry and Validation (`FR-03`, `FR-04`, `FR-07`).
- PDF Marksheet Upload with 5MB validation and disk persistence (`FR-05`, `FR-06`).
- Review, Submission, and Form Locking (`FR-08`, `FR-09`).
- Student Dashboard Status and Timeline Tracking (`FR-10`, `FR-11`).
- Administrative Applications Workspace with Search and Filtering (`FR-15`, `FR-16`, `FR-17`).
- Administrative Document Preview and Download (`FR-18`).
- Application Status Transition State Machine with Remarks (`FR-19`).
- Administrative & Executive Summary Metrics Aggregation (`FR-20`).
- CSV Data Export for Offline Reporting (`FR-12`).

## B.4 Features Not to be Tested (Out of Scope)
- Online Application Fee Payment Gateway (explicitly out of scope per Project Charter).
- SMS and OTP mobile verification.
- Biometric verification or automated facial matching.
- Mobile browser viewports below $1366\times 768$ screen resolution.

## B.5 Business Rule(s) / Feature Under Test
1. **BR-01 (Password Complexity)**: Passwords must be $\ge 8$ characters, contain $\ge 1$ uppercase letter, and contain $\ge 1$ special character.
2. **BR-02 (Application Edit Lock)**: Once an application is submitted, all personal, academic, and document upload fields become read-only and immutable by the student.
3. **BR-03 (Status Transition Constraints)**:
   - `Draft` may only transition to `Submitted`.
   - `Submitted` may transition to `Under Review`, or to `Rejected` (only if explanatory remarks are provided).
   - `Under Review` may transition to `Accepted` or `Rejected`.
   - Terminal states (`Accepted`, `Rejected`) cannot be transitioned back to draft or unsubmitted states.
4. **BR-04 (Academic Scores Range)**: Academic scores (Class 10 and Class 12 percentages) must fall strictly within the real interval $[0.0, 100.0]$.

---

## B.6 Black-Box Test Design — Equivalence Partitioning & Boundary Value Analysis

### Input Under Test: Academic Percentage Score ($0.0\%$ to $100.0\%$)

| Class Type | Description | Representative Value(s) |
| :--- | :--- | :--- |
| **Valid Equivalence Class (V1)** | Valid passing percentage score | $75.5\%$ |
| **Valid Boundary Min (V2)** | Minimum possible score | $0.0\%$ |
| **Valid Boundary Max (V3)** | Maximum possible score | $100.0\%$ |
| **Invalid Equivalence Class (I1)** | Negative percentage score | $-5.0\%$ |
| **Invalid Equivalence Class (I2)** | Percentage exceeding maximum | $105.0\%$ |
| **Invalid Boundary Below Min (I3)** | Just below minimum boundary | $-0.1\%$ |
| **Invalid Boundary Above Max (I4)** | Just above maximum boundary | $100.1\%$ |

### Test Cases: Equivalence Partitioning & Boundary Value Analysis

| TC ID | Description | Input (Academic Score) | Expected Output | Actual Output | Pass / Fail |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-BVA-01** | Test nominal academic score | `78.5` | Accepted; valid score | Accepted; valid score | **Pass** |
| **TC-BVA-02** | Test minimum boundary score | `0.0` | Accepted; minimum valid score | Accepted; minimum valid score | **Pass** |
| **TC-BVA-03** | Test score just above minimum | `0.1` | Accepted; valid score | Accepted; valid score | **Pass** |
| **TC-BVA-04** | Test score just below maximum | `99.9` | Accepted; valid score | Accepted; valid score | **Pass** |
| **TC-BVA-05** | Test maximum boundary score | `100.0` | Accepted; maximum valid score | Accepted; maximum valid score | **Pass** |
| **TC-BVA-06** | Test score just below minimum boundary | `-0.1` | Rejected; error "Score must be $\ge 0.0$" | Rejected; HTTP 422 validation error | **Pass** |
| **TC-BVA-07** | Test score just above maximum boundary | `100.1` | Rejected; error "Score must be $\le 100.0$" | Rejected; HTTP 422 validation error | **Pass** |
| **TC-BVA-08** | Test significantly negative score | `-15.0` | Rejected; error "Score must be $\ge 0.0$" | Rejected; HTTP 422 validation error | **Pass** |
| **TC-BVA-09** | Test significantly out-of-bounds score | `125.0` | Rejected; error "Score must be $\le 100.0$" | Rejected; HTTP 422 validation error | **Pass** |

---

## B.7 Black-Box Test Design — Decision Table Testing

### Business Policy: Administrative Direct Rejection from "Submitted" Status
- **Condition 1 (C1)**: Current Application Status is "Submitted".
- **Condition 2 (C2)**: Actor has authenticated "admin" role.
- **Condition 3 (C3)**: Non-empty explanatory remarks provided.
- **Action (A1)**: Transition application status to "Rejected" and persist audit log.
- **Action (A2)**: Reject update request with explanatory error message.

### Decision Rules Table:

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Status is 'Submitted'** | True | True | True | False | True |
| **C2: Actor role is 'admin'** | True | True | False | True | False |
| **C3: Non-empty remarks provided** | True | False | True | True | False |
| **Action A1: Approve Rejection & Log** | **X** | — | — | — | — |
| **Action A2: Block Request with Error**| — | **X** | **X** | **X** | **X** |

### Test Cases: Decision Table Testing

| TC ID | Input Set 1 (Status) | Input Set 2 (Role) | Input Set 3 (Remarks) | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DT-01** | `Submitted` | `admin` | `"Mark sheet illegible"` | Status updated to `Rejected`; audit log written (**Action A1**) |
| **TC-DT-02** | `Submitted` | `admin` | `""` (Empty) | HTTP 400: "Rejection from 'Submitted' requires explanatory remarks" (**Action A2**) |
| **TC-DT-03** | `Submitted` | `student` | `"Cancel my app"` | HTTP 403: Forbidden - Access restricted to admin (**Action A2**) |
| **TC-DT-04** | `Accepted` | `admin` | `"Revoke"` | HTTP 400: Terminal state cannot be altered (**Action A2**) |
| **TC-DT-05** | `Submitted` | `director` | `""` (Empty) | HTTP 403: Director has read-only executive rights (**Action A2**) |

---

## B.8 White-Box Test Design — Basis Path Testing

### Module Under Test:
`validate_status_transition(current_status: str, new_status: str, remarks: str = "")` located in `backend/workflow.py`.

```python
// Statement / Decision Numbered Code for Basis Path Analysis
def validate_status_transition(current_status: str, new_status: str, remarks: str = "") -> tuple[bool, str]:
    /* Node 1 */
    # Decision 1
    if current_status == new_status:                                    /* Node 2 */
        return False, f"Application is already in status '{current_status}'" /* Node 3 */

    # Decision 2
    if current_status == "Draft":                                        /* Node 4 */
        # Decision 3
        if new_status == "Submitted":                                   /* Node 5 */
            return True, "Draft application successfully submitted"     /* Node 6 */
        else:
            return False, "A Draft application can only be transitioned to 'Submitted'" /* Node 7 */

    # Decision 4
    if current_status == "Submitted":                                    /* Node 8 */
        # Decision 5
        if new_status == "Under Review":                                /* Node 9 */
            return True, "Application placed Under Review"              /* Node 10 */
        # Decision 6
        elif new_status == "Rejected":                                  /* Node 11 */
            # Decision 7
            if remarks and remarks.strip():                             /* Node 12 */
                return True, "Application rejected directly with remarks" /* Node 13 */
            else:
                return False, "Rejection from 'Submitted' requires explanatory remarks" /* Node 14 */
        else:
            return False, "A 'Submitted' application can only transition to 'Under Review' or 'Rejected'" /* Node 15 */

    # Decision 8
    if current_status == "Under Review":                                 /* Node 16 */
        # Decision 9
        if new_status in ["Accepted", "Rejected"]:                      /* Node 17 */
            return True, f"Application successfully marked as {new_status}" /* Node 18 */
        else:
            return False, "An application 'Under Review' can only transition to 'Accepted' or 'Rejected'" /* Node 19 */

    return False, f"Terminal state '{current_status}' cannot be modified" /* Node 20 */
```

### Control Flow Graph (CFG) Metrics:
- **Graph Nodes ($N$)**: $\{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20\}$ &rarr; **$N = 20$**
- **Decision Nodes ($P$)**: $\{2, 4, 5, 8, 9, 11, 12, 16, 17\}$ &rarr; **$P = 9$**
- **Graph Edges ($E$)**:
  - $1 \to 2$
  - $2 \to 3$, $2 \to 4$
  - $4 \to 5$, $4 \to 8$
  - $5 \to 6$, $5 \to 7$
  - $8 \to 9$, $8 \to 16$
  - $9 \to 10$, $9 \to 11$
  - $11 \to 12$, $11 \to 15$
  - $12 \to 13$, $12 \to 14$
  - $16 \to 17$, $16 \to 20$
  - $17 \to 18$, $17 \to 19$
  - Total Directed Edges: **$E = 27$**

### Cyclomatic Complexity Calculation:
$$V(G) = E - N + 2 = 27 - 20 + 2 = 9$$
*(Alternatively, via Predicate Nodes: $V(G) = P + 1 = 9 + 1 = 10$)*  
**Number of Linearly Independent Basis Paths to Cover = 10**

### Linearly Independent Paths & Test Cases:

| Path # | Path Description (Node Traversal) | Input Values (`current`, `new`, `remarks`) | Expected Result |
| :---: | :--- | :--- | :--- |
| **Path 1** | $1 \to 2 \to 3$ (No-op transition) | `("Submitted", "Submitted", "")` | `(False, "already in status")` |
| **Path 2** | $1 \to 2 \to 4 \to 5 \to 6$ (Valid Draft Submission) | `("Draft", "Submitted", "")` | `(True, "successfully submitted")` |
| **Path 3** | $1 \to 2 \to 4 \to 5 \to 7$ (Invalid Draft Target) | `("Draft", "Accepted", "")` | `(False, "only be transitioned to 'Submitted'")` |
| **Path 4** | $1 \to 2 \to 4 \to 8 \to 9 \to 10$ (Move to Review) | `("Submitted", "Under Review", "")` | `(True, "placed Under Review")` |
| **Path 5** | $1 \to 2 \to 4 \to 8 \to 9 \to 11 \to 12 \to 13$ (Direct Reject with Remarks) | `("Submitted", "Rejected", "Doc error")` | `(True, "rejected directly with remarks")` |
| **Path 6** | $1 \to 2 \to 4 \to 8 \to 9 \to 11 \to 12 \to 14$ (Direct Reject without Remarks) | `("Submitted", "Rejected", "")` | `(False, "requires explanatory remarks")` |
| **Path 7** | $1 \to 2 \to 4 \to 8 \to 9 \to 11 \to 15$ (Invalid Submitted Target) | `("Submitted", "Accepted", "")` | `(False, "only transition to 'Under Review' or 'Rejected'")` |
| **Path 8** | $1 \to 2 \to 4 \to 8 \to 16 \to 17 \to 18$ (Review to Decision) | `("Under Review", "Accepted", "")` | `(True, "successfully marked as Accepted")` |
| **Path 9** | $1 \to 2 \to 4 \to 8 \to 16 \to 17 \to 19$ (Invalid Review Target) | `("Under Review", "Draft", "")` | `(False, "only transition to 'Accepted' or 'Rejected'")` |
| **Path 10**| $1 \to 2 \to 4 \to 8 \to 16 \to 20$ (Terminal State Modification) | `("Accepted", "Under Review", "")` | `(False, "Terminal state 'Accepted' cannot be modified")` |

*(All 10 basis paths automated and verified in `backend/test_suite.py`)*.

---

## B.9 Integration Test Cases

**Integration Strategy**: Hybrid (Sandwich) Integration with bottom-up database persistence and top-down REST API routing.  
**Stubs / Drivers Used**: Mock PDF file buffers, synthetic JWT bearer tokens, and SQLite test fixtures.

| TC ID | Integration Step | Description | Expected Result |
| :--- | :--- | :--- | :--- |
| **TC-INT-01** | Auth API & Database | Register new user via `POST /api/auth/register` and verify insertion in `users` and `applications` tables. | HTTP 200 returned; salted hash generated; empty draft record created in DB. |
| **TC-INT-02** | Login API & Token | Issue `POST /api/auth/login` with valid student credentials and inspect returned JWT token. | HTTP 200; token decodes to matching `user_id` and role `student`. |
| **TC-INT-03** | Wizard Form & Database | Submit draft personal and academic data via `POST /api/student/application/save`. | HTTP 200; database row updated with full name, DOB, scores, and course. |
| **TC-INT-04** | Multer/File Upload & Disk | Upload a valid 1.2MB PDF marksheet via `POST /api/student/application/upload`. | HTTP 200; file stored in `backend/uploads/`; file path saved in database. |
| **TC-INT-05** | Final Submit & Audit Log | Execute `POST /api/student/application/submit` to transition status from Draft to Submitted. | Status updated to `Submitted`; audit log entry created in `audit_logs` table. |
| **TC-INT-06** | State Machine Lock | Attempt `POST /api/student/application/save` after application status is `Submitted`. | HTTP 403 Forbidden; error "Application is locked against further edits." |
| **TC-INT-07** | Admin Status & Audit Trail | Issue `PATCH /api/admin/applications/{id}/status` by admin to move to `Under Review`. | Status updated; audit log records admin email, old status, new status, and timestamp. |
| **TC-INT-08** | Analytics API & DB | Request `GET /api/admin/metrics` to aggregate counts across statuses and courses. | HTTP 200; JSON returns exact counts matching current SQLite database rows. |

---

## B.10 System Test Cases (End-to-End, Black-Box)

| TC ID | Scenario | Steps | Expected Result |
| :--- | :--- | :--- | :--- |
| **TC-SYS-01** | End-to-End Student Admission Submission Flow | 1. Navigate to portal on Chrome/Edge.<br>2. Register new student account.<br>3. Fill Step 1 (Personal Details) & click Next.<br>4. Fill Step 2 (Class 10/12 marks, Course choice).<br>5. Upload valid marksheet PDF in Step 3.<br>6. Review summary in Step 4 and click Final Submit. | Application is submitted with status "Submitted"; form locks; UI transitions to student dashboard with tracking timeline and download link. |
| **TC-SYS-02** | Document Security & Size Enforcement | 1. In Step 3, attempt to upload a `.docx` file.<br>2. In Step 3, attempt to upload a 6.5MB PDF file. | 1. Toast error: "Only PDF documents are accepted."<br>2. Toast error: "File size exceeds 5MB limit." File is rejected. |
| **TC-SYS-03** | Administrative Review & Dual View Modes | 1. Sign in as Admin (`admin@iem.edu.in`).<br>2. View metrics cards.<br>3. Search applicant by name.<br>4. Toggle between Table View and Detailed Card View.<br>5. Open details modal. | Metrics reflect live count; search filters rows instantly ($<1$s); view switches smoothly (`NFR-03`); details modal displays scores and audit trail. |
| **TC-SYS-04** | Document Preview & Download by Admin | 1. In Admin Details modal, click "View / Download". | Uploaded applicant PDF opens cleanly in browser tab or downloads directly (`FR-18`). |
| **TC-SYS-05** | CSV Export for Offline Reporting | 1. In Admin workspace, select a course filter.<br>2. Click "Export CSV". | CSV file downloads with headers and matching filtered records (`FR-12`). |
| **TC-SYS-06** | Director Executive Oversight | 1. Sign in as Director (`director@iem.edu.in`).<br>2. Inspect metrics and applications list.<br>3. Open application detail modal. | Summary dashboard displays high-level counts; status update controls are hidden (read-only mode strictly enforced). |

---

## B.11 Test Deliverables
- **Software Test Strategy Document** (`PART A`).
- **Software Test Plan Document** (`PART B`).
- **Automated Test Suite Script** (`backend/test_suite.py`).
- **Automated Test Execution Log** (16 test cases passing, 100% Basis Path coverage).
- **Defect Log and Traceability Matrix** linking `FR-01` to `FR-20` and `NFR-01` to `NFR-05`.

---

## B.12 Suspension and Resumption Criteria
- **Suspension Criteria**: Testing will be suspended immediately if a Severity-1 defect occurs that blocks the primary admission submission pipeline, if the database fails to initialize, or if the server crashes on launch.
- **Resumption Criteria**: Testing will resume once the blocking defect has been resolved, verified through targeted unit re-testing, and confirmed not to introduce regressions into surrounding modules.

---

## B.13 Approval

| Name | Role | Signature | Date |
| :--- | :--- | :--- | :--- |
| **Debadrita Dutta (A-12)** | Test Lead | *Debadrita Dutta* | 2026-08-22 |
| **Susnata Maiti (A-11)** | Frontend Lead / Project Coordinator | *Susnata Maiti* | 2026-08-22 |
| **Sreejita Dey (A-29)** | Backend Lead | *Sreejita Dey* | 2026-08-22 |
| **Swapnil Ghosh (A-04)** | Database Lead | *Swapnil Ghosh* | 2026-08-22 |
| **Dr. Satyajit Chakrabarti** | Project Sponsor & Director, IEM | *Dr. Satyajit Chakrabarti* | 2026-08-22 |
