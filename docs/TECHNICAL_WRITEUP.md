# Technical Design & Architectural Choices Write-Up
**Course**: PCCCS504 Software Engineering & Project Management Lab  
**Project**: IEM Admission System Software  
**Team**: Nexus / P4 (Susnata Maiti, Sreejita Dey, Swapnil Ghosh, Debadrita Dutta)  

---

## 1. Executive Summary & Design Philosophy
The objective of this assignment was to engineer a robust, user-centric proof-of-concept (POC) for the **IEM Admission System**, addressing all functional requirements (`FR-01` through `FR-20`) and non-functional requirements (`NFR-01` through `NFR-05`) specified in the Project Charter, SRS, and HLD. 

In constructing this software, our team evaluated the design patterns specified in the **MEAN Stack POC** guide and integrated them with the FastAPI/Next.js/SQLite architecture outlined in the approved project charter. The result is a lightweight, responsive system optimized for Windows 11 desktop environments running Google Chrome or Microsoft Edge.

---

## 2. Key Architectural Decisions & Module Implementations

### Module 1: Document Storage Architecture (File on Disk vs. DB Blobs)
- **Design Choice**: Uploaded PDF marksheets are written directly to physical disk storage (`backend/uploads/`), with only a sanitized metadata reference (`filename`, `filepath`, `mimetype`, `size`) persisted in the database.
- **Rationale**: Storing raw binary blobs in a relational (SQLite) or NoSQL (MongoDB) database severely impairs query throughput, bloats database backups, and degrades indexing performance. By offloading file storage to the filesystem and serving PDFs via controlled streaming endpoints (`GET /api/documents/{app_id}`), we achieve sub-millisecond document retrieval and comply with `NFR-04` (reliable upload and validation under 5MB).

### Module 2: Authentication & Role-Based Access Control (RBAC)
- **Design Choice**: Client guards are treated solely as User Experience (UX) conveniences; absolute security and role enforcement are guaranteed on the server side through signed bearer tokens and cryptographic hashing.
- **Cryptographic Security**: In accordance with `NFR-02`, student passwords are never stored in plaintext. We utilize **PBKDF2-HMAC-SHA256** with 100,000 hashing rounds and cryptographically unique per-user 16-byte random salts.
- **Server-Side Role Guarding**: Endpoints utilize dependency injection middleware (`require_roles(["admin", "director"])`) to parse and verify the HMAC signature and role claim before executing database queries. Unauthorized access attempts immediately return HTTP 403 Forbidden.

### Module 3: State Machine & Status Workflow Integrity
- **Design Choice**: The admission status is not treated as a free-edit database text field. Instead, transitions are governed by a deterministic finite state machine implemented in `backend/workflow.py`.
- **Allowed Transitions**:
  - `Draft` &rarr; `Submitted` (only when all required academic fields and PDF are attached).
  - `Submitted` &rarr; `Under Review` or `Rejected` (direct rejection requires mandatory explanatory remarks).
  - `Under Review` &rarr; `Accepted` or `Rejected`.
  - Terminal States (`Accepted`, `Rejected`) cannot be transitioned back to draft or unsubmitted states.
- **Audit Logging**: Any status change automatically records an entry in the `audit_logs` table (`FR-13`), capturing the actor's username, previous status, new status, timestamp, and review remarks.

### Module 4: Administrative Dashboard & Analytics Aggregation
- **Design Choice**: In the FastAPI/SQLite backend, we execute atomic aggregation queries (`GROUP BY status` and `GROUP BY course`) to dynamically calculate application counts. In our corresponding MEAN stack implementation, this is achieved using the **MongoDB Aggregation Pipeline** with `$match` and `$group` operators rather than inefficient in-memory array filtering.
- **Dual-View UX Pattern (`NFR-03`)**: To accommodate different administrative workflows, the portal features an instantaneous toggle between a **Compact Table View** (for high-density triage) and a **Detailed Card View** (for deep-dive qualitative reviews).

---

## 3. Communication Integrity Between Frontend & Backend
The frontend and backend communicate strictly via decoupled RESTful JSON interfaces (`INT-02`):
1. **Dynamic Options Population**: Dropdown menus (such as Course Preferences) are loaded asynchronously from `/api/courses` upon initialization in under 1 second (`NFR-03`).
2. **Field-Level Validation Feedback (`FR-07`)**: Invalid email formats, incomplete academic scores, or non-compliant passwords trigger immediate, non-blocking visual toasts and inline error states.
3. **Optimistic Locking**: Once an applicant submits their application, the record status updates to `"Submitted"`, triggering the UI to transition from an editable 4-step wizard to a read-only progress tracking screen (`FR-09`).

---

## 4. Retrospective & Future Improvements
While the current POC satisfies all functional and non-functional requirements within the 20-day project scope, subsequent production iterations would implement:
1. **Distributed Object Storage**: Migrating local filesystem document storage to Amazon S3 or Google Cloud Storage with presigned URLs for multi-instance scalability.
2. **Real-time Notifications via WebSockets**: Upgrading status polling to bidirectional WebSockets or Server-Sent Events (SSE) so applicants receive instant desktop push notifications when their application moves from "Under Review" to "Accepted".
3. **Automated Optical Character Recognition (OCR)**: Integrating an OCR pipeline to cross-verify student-entered Class 10 and 12 percentages directly against the uploaded marksheet PDF.
4. **Automated Email & SMS Gateway Integration**: Triggering formal admission offer letters and verification reminders via SendGrid or Twilio upon decision finalization.
