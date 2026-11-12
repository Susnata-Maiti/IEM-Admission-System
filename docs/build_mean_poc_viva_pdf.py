import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Professional Color Palette
C_NAVY = colors.HexColor("#1e3a8a")        # Navy 900
C_PRIMARY = colors.HexColor("#2563eb")     # Blue 600
C_PRIMARY_LIGHT = colors.HexColor("#eff6ff")# Blue 50
C_DARK = colors.HexColor("#0f172a")        # Slate 900
C_MUTED = colors.HexColor("#334155")       # Slate 700
C_BORDER = colors.HexColor("#cbd5e1")      # Slate 300
C_BORDER_BLUE = colors.HexColor("#93c5fd") # Blue 300
C_ROW_BG = colors.HexColor("#f8fafc")      # Slate 50
C_WHITE = colors.HexColor("#ffffff")
C_GREEN_BG = colors.HexColor("#f0fdf4")
C_GREEN_BORDER = colors.HexColor("#86efac")
C_AMBER_BG = colors.HexColor("#fefce8")
C_AMBER_BORDER = colors.HexColor("#fde047")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Footer
        footer_text = "IEM Admission System Software  •  MEAN Stack POC & Viva Guide  •  Team Nexus (P4)"
        self.drawString(54, 36, footer_text)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 54, 36, page_str)

        # Running header (on pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, A4[1] - 36, "MEAN Stack Proof of Concept (POC) — Technical Architecture & Viva Guide")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, A4[1] - 40, A4[0] - 54, A4[1] - 40)

        self.restoreState()

def build_pdf(out_path):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    style_category = ParagraphStyle(
        'CategoryTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=C_PRIMARY,
        spaceAfter=4
    )

    style_title = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=23,
        textColor=C_NAVY,
        spaceAfter=4
    )

    style_subtitle = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=C_MUTED,
        spaceAfter=10
    )

    style_part = ParagraphStyle(
        'PartHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#ffffff"),
        alignment=1
    )

    style_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=C_NAVY,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=C_PRIMARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_q_title = ParagraphStyle(
        'QuestionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=13,
        textColor=C_NAVY,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=C_DARK,
        spaceAfter=5
    )

    style_body_muted = ParagraphStyle(
        'BodyMuted',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_MUTED,
        spaceAfter=5
    )

    style_code = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a")
    )

    style_meta_key = ParagraphStyle(
        'MetaKey',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11,
        textColor=C_DARK
    )

    style_meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=C_MUTED
    )

    style_th = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=C_WHITE,
        alignment=0
    )

    style_td = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=11,
        textColor=C_MUTED
    )

    style_td_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.0,
        leading=11,
        textColor=C_DARK
    )

    def make_part_banner(title_text):
        tbl = Table([[Paragraph(title_text, style_part)]], colWidths=[487])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_NAVY),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        return tbl

    story = []

    # Title & Metadata
    story.append(Paragraph("PCCCS504 SOFTWARE ENGINEERING & PROJECT MANAGEMENT LAB  •  ACADEMIC YEAR 2026-27", style_category))
    story.append(Paragraph("IEM Admission System: MEAN Stack POC & Comprehensive Viva Guide", style_title))
    story.append(Paragraph("In-Depth Technical Architecture, Implementation Mechanics & Exam-Ready Viva Question Bank", style_subtitle))

    meta_rows = [
        [Paragraph("<b>Project Title:</b>", style_meta_key), Paragraph("IEM Admission System Software (MEAN Stack Proof of Concept)", style_meta_val)],
        [Paragraph("<b>Team Details:</b>", style_meta_key), Paragraph("Team Number: P4  |  Team Name: Nexus  |  Batch: 2024-2028 (Section A, 5th Semester)", style_meta_val)],
        [Paragraph("<b>Team Members:</b>", style_meta_key), Paragraph("Susnata Maiti (A-11, Frontend) | Sreejita Dey (A-29, Backend) | Swapnil Ghosh (A-04, Database) | Debadrita Dutta (A-12, Testing)", style_meta_val)],
        [Paragraph("<b>Supervisors:</b>", style_meta_key), Paragraph("Prof. Sangeeta Sarkar, Prof. Saikat Dutta  |  Sponsor & Director: Dr. Satyajit Chakrabarti", style_meta_val)],
        [Paragraph("<b>POC Location:</b>", style_meta_key), Paragraph("<code>mean_stack_equivalent/</code> (Client: Angular 17+ | Server: Node.js + Express + Mongoose)", style_meta_val)]
    ]
    t_meta = Table(meta_rows, colWidths=[105, 382])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER_BLUE),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dbeafe")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # =========================================================================
    # PART I: COMPLETE TECHNICAL EXPLANATION OF THE MEAN STACK POC
    # =========================================================================
    story.append(make_part_banner("PART I: COMPLETE TECHNICAL EXPLANATION OF THE MEAN STACK POC"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Architectural Overview & Request-Response Loop", style_h1))
    story.append(Paragraph(
        "While the primary production deployment of the IEM Admission System utilizes a FastAPI (Python) backend with "
        "dual-engine persistence (MongoDB Atlas and SQLite3 fallback), the team built a complete <b>MEAN Stack Proof of Concept (POC)</b> "
        "in <code>mean_stack_equivalent/</code>. This POC mirrors the exact same business logic, security policies, and "
        "data models using the traditional full-stack JavaScript architecture: <b>MongoDB, Express.js, Angular, and Node.js</b>.",
        style_body
    ))

    # Architecture Box Diagram in Table
    arch_diag = (
        "┌────────────────────────────────────────────────────────────────────────────────────────┐\n"
        "│                               MEAN STACK FLOW OF CONTROL                               │\n"
        "├────────────────────────────────────────────────────────────────────────────────────────┤\n"
        "│  [Angular 17+ SPA Client] (client/src/app/)                                            │\n"
        "│        │                                                                               │\n"
        "│        │  1. Asynchronous HTTP Request (JSON + Bearer JWT Header) via RxJS Observable  │\n"
        "│        ▼                                                                               │\n"
        "│  [Node.js Runtime + Express.js Web Server] (server/server.js, port 5000)               │\n"
        "│        │                                                                               │\n"
        "│        ├─► Middleware Pipeline:                                                        │\n"
        "│        │     ├─ cors() & express.json() body parsing                                   │\n"
        "│        │     ├─ authenticateToken (JWT signature & expiry verification)                 │\n"
        "│        │     ├─ requireRole(['student', 'admin', 'director']) server-side guard        │\n"
        "│        │     └─ multer (stream validator, 5MB limit, PDF MIME inspection)              │\n"
        "│        │                                                                               │\n"
        "│        ├─► Local File System (/uploads): Streams & saves raw PDF marksheet binary       │\n"
        "│        │                                                                               │\n"
        "│        ▼                                                                               │\n"
        "│  [MongoDB Atlas / Local NoSQL Engine] (via Mongoose ODM models)                        │\n"
        "│        ├─ users collection (Stores salted bcrypt password hashes)                      │\n"
        "│        └─ applications collection (Bio-data, scores, docReference, auditTrail array)   │\n"
        "└────────────────────────────────────────────────────────────────────────────────────────┘"
    )
    t_diag = Table([[Paragraph(f"<pre>{arch_diag}</pre>", style_code)]], colWidths=[487])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_diag)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Component-by-Component Working", style_h1))
    
    story.append(Paragraph("2.1 M — MongoDB & Mongoose Object Data Modeling (ODM)", style_h2))
    story.append(Paragraph(
        "MongoDB operates as the document database storing JSON-like BSON documents. Mongoose provides a schema-based solution "
        "to model application data, complete with validation rules and middleware:<br/>"
        "• <b>User Model (<code>models/User.js</code>):</b> Manages authentication accounts. Enforces unique, lowercase email "
        "indexing and restricts the <code>role</code> field strictly to an enumeration: <code>['student', 'admin', 'director']</code>. "
        "Passwords are saved strictly as salted cryptographic hashes; plaintext passwords never reach the database.<br/>"
        "• <b>Application Model (<code>models/Application.js</code>):</b> Stores complete applicant submissions. Marks (Class 10 and 12) "
        "are bounded by schema-level validators (<code>min: 0, max: 100</code>). Implements a subdocument schema (<code>AuditLogSchema</code>) "
        "embedded as an array (<code>auditTrail: [AuditLogSchema]</code>) to log every status mutation with author and timestamp.",
        style_body
    ))

    story.append(Paragraph("2.2 E — Express.js Routing & Middleware Pipeline", style_h2))
    story.append(Paragraph(
        "Express serves as the routing framework mounted on top of Node.js. It organizes incoming HTTP traffic through a sequential "
        "middleware pipeline:<br/>"
        "• <b>Global Middleware:</b> <code>cors()</code> permits cross-origin requests from the Angular client, while "
        "<code>express.json()</code> parses JSON payloads into <code>req.body</code>.<br/>"
        "• <b>Authentication Middleware (<code>authenticateToken</code>):</b> Extracts the <code>Bearer &lt;token&gt;</code> from the "
        "HTTP <code>Authorization</code> header and cryptographically validates it using <code>jsonwebtoken</code>. On failure, "
        "it immediately terminates the request with HTTP <code>401 Unauthorized</code>.<br/>"
        "• <b>Server-Side Role Guard (<code>requireRole</code>):</b> Inspects the verified role in <code>req.user.role</code>. If a student "
        "attempts to invoke administrative endpoints (such as metrics or status mutation), Express halts execution with HTTP <code>403 Forbidden</code>.",
        style_body
    ))

    story.append(Paragraph("2.3 A — Angular 17+ Client-Side Single Page Application", style_h2))
    story.append(Paragraph(
        "Angular provides the component-driven frontend architecture, maintaining client state without full-page browser reloads:<br/>"
        "• <b>Service Layer (<code>admission.service.ts</code>):</b> Uses Angular's Dependency Injection (DI) to inject <code>HttpClient</code>. "
        "All network interactions return <b>RxJS <code>Observable&lt;any&gt;</code></b> streams. The service automatically extracts JWT tokens "
        "from browser <code>localStorage</code> and attaches them to outbound request headers.<br/>"
        "• <b>Component Layer (<code>app.component.ts</code>):</b> Subscribes to service observables, binds form values using two-way data "
        "binding, and constructs native <code>FormData</code> objects for binary file uploads.",
        style_body
    ))

    story.append(Paragraph("2.4 N — Node.js Asynchronous Runtime", style_h2))
    story.append(Paragraph(
        "Node.js runs the V8 JavaScript engine over an asynchronous, single-threaded Event Loop. All heavy I/O tasks—such as Multer "
        "writing PDF streams to disk, bcrypt running CPU-intensive key derivation, and Mongoose querying MongoDB over TCP sockets—are "
        "dispatched to <code>libuv</code>'s thread pool. This guarantees that concurrent applicant requests are handled without blocking.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3. Implementation of the 4 Core Project Modules", style_h1))
    story.append(Paragraph(
        "The MEAN POC implements the exact four functional modules defined in the Project Charter and SRS baseline:",
        style_body
    ))

    modules_data = [
        ("Module 1: Document Upload (Decoupled Reference Pattern)", 
         "Rather than storing large PDF binaries directly in MongoDB documents (which risks hitting MongoDB's 16MB document limit and "
         "thrashing RAM cache), the POC implements a Decoupled Reference Pattern: Multer streams the PDF directly to the filesystem at "
         "<code>server/uploads/</code> with an enforced 5MB ceiling and MIME check. Only lightweight metadata (<code>filename, filepath, size</code>) "
         "is saved into MongoDB under <code>docReference</code>."),
        
        ("Module 2: Auth & Role-Based Access Control (RBAC)", 
         "Passwords are encrypted using <code>bcryptjs</code> with an adaptive work factor (10 salt rounds). Valid logins receive a signed "
         "JSON Web Token encoded with user ID and role. While Angular uses client-side route guards for user experience, the backend "
         "<code>requireRole()</code> middleware strictly enforces server-side role isolation on all sensitive routes."),
        
        ("Module 3: Finite-State Machine & Audit Trail Logging", 
         "State transitions follow strict business rules evaluated by <code>validateTransition()</code>: Draft can only transition to Submitted; "
         "Submitted can transition to Under Review, or directly to Rejected (the latter strictly requiring explanatory remarks); terminal states "
         "(Accepted / Rejected) cannot be modified. Every transition pushes a record to the embedded <code>auditTrail</code> array."),
        
        ("Module 4: Admin Metrics Aggregation Pipeline", 
         "Instead of loading thousands of documents into Node.js memory and looping, the POC leverages MongoDB's native Aggregation Framework: "
         "<code>$match</code> filters out unsubmitted draft records, and <code>$group</code> computes real-time counts by status and department "
         "directly inside the database engine, returning a tiny ~100-byte summary to the dashboard.")
    ]

    for m_title, m_desc in modules_data:
        m_tbl = Table([[Paragraph(f"<b>{m_title}</b>", style_h2)], [Paragraph(m_desc, style_body)]], colWidths=[487])
        m_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#ffffff")),
            ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(m_tbl)
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 6))
    story.append(Paragraph("4. Architectural Comparison: MEAN Stack POC vs. Production FastAPI Stack", style_h1))

    comp_rows = [
        ["Architectural Dimension", "Production Implementation", "MEAN Stack POC Equivalent"],
        ["Backend Runtime", "Python 3.14 + FastAPI (ASGI Coroutines)", "Node.js 18+ + Express.js (Single Thread + libuv)"],
        ["Type Safety & Validation", "Pydantic Schemas (BaseModel) with Python type hints", "Mongoose Schema validation + manual route checks"],
        ["Database Architecture", "Dual-Engine: MongoDB Atlas Cloud + SQLite fallback", "MongoDB Atlas / Local MongoDB via Mongoose ODM"],
        ["DNS SRV Resilience", "Auto-injected public DNS resolvers (8.8.8.8, 1.1.1.1)", "Standard Node.js dns.lookup / system resolver"],
        ["Client Framework", "Responsive Vanilla JS Single Page Application (SPA)", "Angular 17+ (TypeScript, RxJS Observables, DI)"],
        ["File Stream Handling", "python-multipart streaming to backend/uploads/", "multer diskStorage middleware to server/uploads/"],
        ["Password Cryptography", "PBKDF2-HMAC-SHA256 (600,000 hashing rounds)", "bcryptjs (Blowfish adaptive hashing with salt rounds)"]
    ]

    t_comp_cells = []
    for r_idx, r_data in enumerate(comp_rows):
        row = []
        for c_idx, val in enumerate(r_data):
            if r_idx == 0:
                row.append(Paragraph(val, style_th))
            elif c_idx == 0:
                row.append(Paragraph(f"<b>{val}</b>", style_td_bold))
            else:
                row.append(Paragraph(val, style_td))
        t_comp_cells.append(row)

    t_comp = Table(t_comp_cells, colWidths=[120, 185, 182])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_ROW_BG]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 14))

    # =========================================================================
    # PART II: COMPREHENSIVE VIVA VOCE QUESTION BANK & ANSWERS
    # =========================================================================
    story.append(PageBreak())
    story.append(make_part_banner("PART II: COMPREHENSIVE VIVA VOCE QUESTION BANK & ANSWERS"))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "This question bank is structured across the primary engineering domains of the MEAN Stack POC. "
        "Each answer is calibrated for technical precision during laboratory vivas and external examinations:",
        style_body
    ))

    viva_qa = [
        # Category A
        ("CATEGORY A: CORE MEAN STACK ARCHITECTURE & FUNDAMENTALS", [
            ("Q1: What does each letter in the MEAN stack stand for, and how does data flow end-to-end?",
             "<b>Answer:</b> MEAN stands for <b>MongoDB</b>, <b>Express.js</b>, <b>Angular</b>, and <b>Node.js</b>.<br/>"
             "The end-to-end request-response lifecycle operates in 6 distinct steps:<br/>"
             "1. <i>User Action in Angular:</i> A user interacts with an Angular template component. The component delegates to an injected service (<code>AdmissionService</code>).<br/>"
             "2. <i>HTTP Request Dispatch:</i> The service issues an asynchronous HTTP request (e.g. <code>POST /api/auth/login</code>) over an RxJS <code>Observable</code>, carrying JSON and an <code>Authorization: Bearer &lt;token&gt;</code> header.<br/>"
             "3. <i>Node.js Event Handling:</i> Node.js receives the incoming TCP socket connection and delegates the request to the Express.js routing pipeline.<br/>"
             "4. <i>Express Middleware & Business Logic:</i> Express filters the request through middleware (CORS, JSON parser, JWT authentication, and RBAC role validation) before invoking the controller.<br/>"
             "5. <i>Mongoose & MongoDB Interaction:</i> The controller invokes Mongoose ODM methods (e.g., <code>User.findOne()</code> or <code>Application.aggregate()</code>) communicating with MongoDB over the binary wire protocol.<br/>"
             "6. <i>Response & DOM Update:</i> Express serializes the result into an HTTP JSON response with standard status codes. Angular's observable subscriber receives the payload and updates component state, causing Angular's change detector to refresh the DOM without reloading."),

            ("Q2: Why is Node.js called 'single-threaded' if it handles thousands of concurrent requests simultaneously?",
             "<b>Answer:</b> Node.js executes JavaScript on a single thread known as the <b>Event Loop</b> (powered by Google's V8 engine). "
             "However, Node.js offloads all non-blocking I/O operations—such as disk reads/writes via Multer, cryptographic key derivations via bcrypt, "
             "and MongoDB TCP sockets—to <b><code>libuv</code>'s internal C++ thread pool</b> (defaulting to 4 worker threads).<br/>"
             "When an I/O operation finishes, <code>libuv</code> queues its callback on the Event Loop's task queue. This asynchronous, non-blocking "
             "architecture allows Node.js to achieve high concurrency without the heavy RAM overhead of creating a dedicated OS thread per client request."),

            ("Q3: What is the architectural difference between Angular and React, and why was Angular chosen for the MEAN POC?",
             "<b>Answer:</b> Angular is a complete, opinionated, battery-included <b>framework</b> written in TypeScript, featuring built-in routing, "
             "form validation, dependency injection, and HTTP services out of the box. In contrast, React is a minimalist <b>library</b> focused "
             "solely on the view layer, requiring third-party packages for routing, state, and HTTP.<br/>"
             "Angular was chosen for the MEAN POC because its structured architectural pattern (Component-Service-Module hierarchy) enforces clean "
             "separation of concerns, robust TypeScript typing, and adherence to enterprise software engineering design principles.")
        ]),

        # Category B
        ("CATEGORY B: MONGODB, MONGOOSE & DATA STORAGE DESIGN", [
            ("Q4: Why did you store uploaded PDF marksheets on the filesystem instead of directly inside MongoDB?",
             "<b>Answer:</b> Storing raw binary files inside MongoDB documents (as BSON binary buffers or GridFS chunks) creates severe bottlenecks:<br/>"
             "1. <i>16MB BSON Limit:</i> MongoDB enforces a strict 16MB document size ceiling. Multiple high-resolution student marksheets risk hitting this limit.<br/>"
             "2. <i>Memory & Cache Thrashing:</i> MongoDB caches active working sets in RAM via WiredTiger. Storing large binary chunks in memory evicts critical document indices and query data.<br/>"
             "3. <i>Stateless File Streaming:</i> Files on disk can be streamed directly via static file servers (<code>express.static</code>) or CDNs with HTTP caching headers, bypassing database overhead entirely.<br/>"
             "Therefore, we implemented the <b>Decoupled Reference Pattern</b>: physical PDFs reside in <code>server/uploads/</code>, and only lightweight metadata references (filename, filepath, size) are stored in MongoDB."),

            ("Q5: What is the difference between Embedding and Referencing in MongoDB, and how are both used in your POC?",
             "<b>Answer:</b><br/>"
             "• <b>Embedding (Denormalization):</b> Child documents are nested inside an array within the parent document. Used for bounded 1:N relationships where child data is always queried with the parent.<br/>"
             "  <i>POC Usage:</i> The <code>auditTrail</code> array is embedded directly inside <code>ApplicationSchema</code> because audit logs are always read with the application and have a strictly bounded lifecycle.<br/>"
             "• <b>Referencing (Normalization):</b> Storing an <code>ObjectId</code> pointing to another collection. Used for independent entities or to prevent unbounded document growth.<br/>"
             "  <i>POC Usage:</i> <code>ApplicationSchema</code> references the user record via <code>userId: { type: ObjectId, ref: 'User' }</code>, linking the candidate profile to authentication credentials without data duplication."),

            ("Q6: Explain how the MongoDB Aggregation Pipeline works in your /admin/metrics endpoint. Why not use find() and JavaScript reduce()?",
             "<b>Answer:</b> The metrics endpoint executes a native MongoDB Aggregation Pipeline:<br/>"
             "<code>Application.aggregate([{ $match: { status: { $ne: 'Draft' } } }, { $group: { _id: '$status', count: { $sum: 1 } } }])</code><br/>"
             "• <i>Pipeline Mechanism:</i> <code>$match</code> filters out draft records at the database engine level using indexes. The filtered stream passes to <code>$group</code>, which groups documents by categorical keys and tallies counts using native C++ accumulators.<br/>"
             "• <i>Why not find() + reduce():</i> If an institution receives 50,000 applications, <code>find()</code> would serialize 50,000 JSON documents across the network, consuming hundreds of megabytes of Node.js RAM and blocking the Event Loop. The Aggregation Pipeline performs all computations inside the database engine and returns only 4 small summary objects (~100 bytes).")
        ]),

        # Category C
        ("CATEGORY C: EXPRESS.JS, MIDDLEWARE & SECURITY", [
            ("Q7: What is middleware in Express.js, and what happens if you forget to call next()?",
             "<b>Answer:</b> In Express, middleware functions have access to the request object (<code>req</code>), response object (<code>res</code>), "
             "and the next middleware in the execution chain (<code>next</code>). Middleware can execute logic, modify request/response properties, "
             "end the cycle via <code>res.json()</code>, or pass control forward by invoking <code>next()</code>.<br/>"
             "If a middleware function neither sends a response nor calls <code>next()</code>, the request will <b>hang indefinitely</b> until the client socket times out."),

            ("Q8: How does your JWT authentication work, and why is client-side role checking insufficient for security?",
             "<b>Answer:</b><br/>"
             "1. <i>JWT Workflow:</i> Upon valid login, Express issues a signed JSON Web Token consisting of three Base64URL-encoded segments: <code>Header.Payload.Signature</code>. The signature is encrypted with a server-side secret using HMAC-SHA256. Subsequent requests transmit this token in the <code>Authorization: Bearer</code> header, verified statelessly by <code>authenticateToken</code>.<br/>"
             "2. <i>Why Client-Side Checks are Insufficient:</i> Client-side JavaScript running in the browser is completely under the user's control. A student can open Chrome DevTools, modify JavaScript variables, or send requests directly using Postman or curl. Client-side checks are merely a UI convenience. True security is established exclusively by server-side middleware (<code>requireRole(['admin'])</code>) verifying cryptographic tokens on every API endpoint."),

            ("Q9: What is the difference between bcrypt and standard hashing algorithms like SHA-256 or MD5?",
             "<b>Answer:</b> SHA-256 and MD5 are general-purpose hash functions designed to be extremely fast for checksums. Because they are fast, attackers with GPUs can compute billions of guesses per second in offline dictionary attacks.<br/>"
             "In contrast, <b>bcrypt</b> is an adaptive, one-way cryptographic hash algorithm based on the Blowfish cipher. It includes:<br/>"
             "1. <i>Automatic Salting:</i> Appends a unique 16-byte random salt to prevent Rainbow Table attacks.<br/>"
             "2. <i>Configurable Work Factor:</i> Developers can configure the cost factor ($2^{10} = 1024$ rounds in our POC). As hardware speeds advance, the cost factor can be increased to deliberately slow down computation, making brute-force attacks computationally infeasible.")
        ]),

        # Category D
        ("CATEGORY D: ANGULAR SERVICES, RXJS & FINITE-STATE MACHINE", [
            ("Q10: What is an RxJS Observable, and how does it differ from a standard JavaScript Promise?",
             "<b>Answer:</b> In Angular's <code>AdmissionService</code>, all HTTP requests return <code>Observable&lt;any&gt;</code> rather than Promises.<br/>"
             "• <i>Emission:</i> A Promise emits a single value and resolves or rejects; an Observable can emit multiple values over time (a stream).<br/>"
             "• <i>Execution:</i> Promises are <b>eager</b> (they execute immediately upon creation); Observables are <b>lazy</b> (they do not execute until a subscriber calls <code>.subscribe()</code>).<br/>"
             "• <i>Cancellation:</i> Promises cannot be cancelled once started; Observables can be cancelled at any time by calling <code>.unsubscribe()</code>.<br/>"
             "• <i>Transformation:</i> Observables support a rich suite of functional reactive operators (<code>map</code>, <code>filter</code>, <code>catchError</code>, <code>debounceTime</code>)."),

            ("Q11: Explain the state transition logic in validateTransition. What is Cyclomatic Complexity, and how does it apply here?",
             "<b>Answer:</b><br/>"
             "1. <i>Transition Logic:</i> Applications start in <code>Draft</code>, transition to <code>Submitted</code>, then to <code>Under Review</code>, and finally to terminal states (<code>Accepted</code> or <code>Rejected</code>). Direct rejection from 'Submitted' strictly requires non-empty remarks. Terminal states cannot be altered.<br/>"
             "2. <i>McCabe's Cyclomatic Complexity:</i> Defined as $V(G) = E - N + 2P$, where $E$ is edges, $N$ is nodes, and $P$ is connected components ($P=1$). In our transition function, there are 9 decision predicates, yielding $V(G) = 9 + 1 = 10$. This proves mathematically that exactly <b>10 linearly independent basis paths</b> must be tested to ensure 100% statement and branch coverage."),

            ("Q12: Why did your team deploy FastAPI for production instead of this MEAN Stack POC?",
             "<b>Answer:</b> While the MEAN stack POC is fully functional, FastAPI was selected for production due to three architectural advantages:<br/>"
             "1. <i>Dual-Engine Database Fallback:</i> FastAPI seamlessly incorporated our intelligent persistence router, automatically injecting public DNS (8.8.8.8) and failing over to local SQLite3 (<code>iem_admission.db</code>) in $<4000$ms during campus network outages.<br/>"
             "2. <i>Strict Pydantic Type Validation:</i> Python type annotations validate incoming JSON schemas and serialize responses with zero runtime type ambiguity.<br/>"
             "3. <i>Interactive OpenAPI Generation:</i> FastAPI automatically generates live Swagger UI documentation (<code>/docs</code>) directly from source code without third-party plugins.<br/>"
             "4. <i>Edge Serverless Cold-Start:</i> On Vercel's serverless edge, Python runtime handlers boot with minimal latency compared to full Angular CLI compilations.")
        ])
    ]

    for cat_title, q_list in viva_qa:
        story.append(Paragraph(cat_title, style_h1))
        for q_text, a_text in q_list:
            q_box = [
                [Paragraph(q_text, style_q_title)],
                [Paragraph(a_text, style_body)]
            ]
            t_q = Table(q_box, colWidths=[487])
            t_q.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
                ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#ffffff")),
                ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 7),
                ('RIGHTPADDING', (0, 0), (-1, -1), 7),
            ]))
            story.append(t_q)
            story.append(Spacer(1, 5))
        story.append(Spacer(1, 6))

    # Viva Tips Box
    story.append(Paragraph("STRATEGIC VIVA VOCE TIPS FOR SCORING MAXIMUM MARKS", style_h1))
    tips = [
        [Paragraph("<b>Lead with Architectural Layers:</b>", style_meta_key), 
         Paragraph("Always explain features through both client and server layers (e.g. <i>'On the client, Angular builds a FormData payload; on the server, Express uses multer to stream to disk while Mongoose records only the metadata reference'</i>).", style_meta_val)],
        [Paragraph("<b>Emphasize Server-Side Authority:</b>", style_meta_key), 
         Paragraph("Highlight that client-side validations are purely for user experience (UX), while true security is enforced strictly on the server by JWT verification and database schemas.", style_meta_val)],
        [Paragraph("<b>Cite Exact Quantitative Metrics:</b>", style_meta_key), 
         Paragraph("Impress examiners by citing concrete numbers: the <b>5MB</b> PDF upload limit, <b>10 salt rounds</b> in bcrypt, <b>$V(G) = 10$</b> basis paths in the state machine, and the <b>16MB</b> BSON document limit.", style_meta_val)]
    ]
    t_v_tips = Table(tips, colWidths=[130, 357])
    t_v_tips.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_GREEN_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_GREEN_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#bbf7d0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_v_tips)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully compiled at: {out_path}")

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_pdf = os.path.join(root_dir, "MEAN_Stack_POC_Explanation_and_Viva_Guide.pdf")
    build_pdf(target_pdf)
