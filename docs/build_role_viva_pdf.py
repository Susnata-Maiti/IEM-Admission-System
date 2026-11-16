import os
import sys
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Professional Palette
C_NAVY = colors.HexColor("#0f172a")         # Slate 900
C_PRIMARY = colors.HexColor("#1e3a8a")      # Blue 900
C_BORDER = colors.HexColor("#cbd5e1")       # Slate 300
C_WHITE = colors.HexColor("#ffffff")
C_ROW_BG = colors.HexColor("#f8fafc")       # Slate 50

# Role-specific Themes
# Frontend (Blue)
FE_PRIMARY = colors.HexColor("#1d4ed8")     # Blue 700
FE_BG = colors.HexColor("#eff6ff")          # Blue 50
FE_BORDER = colors.HexColor("#bfdbfe")      # Blue 200

# Backend (Emerald Green)
BE_PRIMARY = colors.HexColor("#047857")     # Emerald 700
BE_BG = colors.HexColor("#ecfdf5")          # Emerald 50
BE_BORDER = colors.HexColor("#a7f3d0")      # Emerald 200

# Database (Purple / Violet)
DB_PRIMARY = colors.HexColor("#6d28d9")     # Violet 700
DB_BG = colors.HexColor("#f5f3ff")          # Violet 50
DB_BORDER = colors.HexColor("#ddd6fe")      # Violet 200

# Testing (Crimson / Rose)
QA_PRIMARY = colors.HexColor("#b91c1c")     # Red 700
QA_BG = colors.HexColor("#fef2f2")          # Red 50
QA_BORDER = colors.HexColor("#fecaca")      # Red 200

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
        footer_text = "IEM Admission System Software  •  Role-Based Viva Voce Guide  •  Team Nexus (P4)"
        self.drawString(50, 28, footer_text)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 50, 28, page_str)

        # Running header on pages > 1
        if self._pageNumber > 1:
            self.drawString(50, A4[1] - 30, "PCCCS504 SE & PM Lab — Role-Based Viva Voce Guide (40 Comprehensive Q&A)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(50, A4[1] - 34, A4[0] - 50, A4[1] - 34)

        self.restoreState()

def build_role_viva_pdf(out_path):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=44,
        bottomMargin=44
    )

    styles = getSampleStyleSheet()

    style_top_tag = ParagraphStyle(
        'TopTag', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=10.5,
        textColor=C_PRIMARY, spaceAfter=2
    )
    style_main_title = ParagraphStyle(
        'MainTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=17.5, leading=21,
        textColor=C_NAVY, spaceAfter=3
    )
    style_sub_title = ParagraphStyle(
        'SubTitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=12.5,
        textColor=colors.HexColor("#475569"), spaceAfter=7
    )
    style_meta_k = ParagraphStyle(
        'MetaK', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.0, leading=10.5,
        textColor=C_NAVY
    )
    style_meta_v = ParagraphStyle(
        'MetaV', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.0, leading=10.5,
        textColor=colors.HexColor("#334155")
    )

    style_role_title = ParagraphStyle(
        'RoleBannerTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12.0, leading=15,
        textColor=C_WHITE, alignment=1
    )
    style_role_sub = ParagraphStyle(
        'RoleBannerSub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11.0,
        textColor=colors.HexColor("#f8fafc"), alignment=1
    )

    style_q_title = ParagraphStyle(
        'QuestionTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.0, leading=12,
        textColor=C_NAVY
    )
    style_a_body = ParagraphStyle(
        'AnswerBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.0, leading=11.2,
        textColor=colors.HexColor("#1e293b")
    )
    style_h2 = ParagraphStyle(
        'Heading2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=C_PRIMARY, spaceBefore=8, spaceAfter=4, keepWithNext=True
    )

    def make_role_banner(role_title, assignee_info, bg_color):
        t = Table([
            [Paragraph(role_title, style_role_title)],
            [Paragraph(assignee_info, style_role_sub)]
        ], colWidths=[495])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        return t

    story = []

    # Title & Metadata
    story.append(Paragraph("PCCCS504 SOFTWARE ENGINEERING & PROJECT MANAGEMENT LAB • ACADEMIC YEAR 2026-27", style_top_tag))
    story.append(Paragraph("IEM Admission System: Comprehensive Role-Based Viva Voce Guide", style_main_title))
    story.append(Paragraph("40 Specialized Viva Questions & In-Depth Technical Answers for Frontend, Backend, Database Lead, and Test Lead", style_sub_title))

    meta_rows = [
        [Paragraph("<b>Project Title:</b>", style_meta_k), Paragraph("IEM Admission System Software (Web-Based Responsive Portal & MEAN Stack POC)", style_meta_v)],
        [Paragraph("<b>Team Details:</b>", style_meta_k), Paragraph("Team Number: P4  |  Team Name: Nexus  |  Batch: 2024-2028 (Section A, 5th Semester)", style_meta_v)],
        [Paragraph("<b>Role Assignments:</b>", style_meta_k), Paragraph("1. Frontend Dev: Susnata Maiti (A-11)  |  2. Backend Dev: Sreejita Dey (A-29)<br/>3. Database Lead: Swapnil Ghosh (A-04)  |  4. Test Lead: Debadrita Dutta (A-12)", style_meta_v)],
        [Paragraph("<b>Supervisors:</b>", style_meta_k), Paragraph("Prof. Sangeeta Sarkar, Prof. Saikat Dutta  |  Sponsor & Director: Dr. Satyajit Chakrabarti", style_meta_v)],
        [Paragraph("<b>Coverage Scope:</b>", style_meta_k), Paragraph("Exact implementation mechanics, design patterns, testing metrics ($V(G)=10$, BVA/EP), database dual-engine routing, and security guards across production & POC stacks.", style_meta_v)]
    ]
    t_meta = Table(meta_rows, colWidths=[105, 390])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    # =========================================================================
    # ROLE 1: FRONTEND DEVELOPER
    # =========================================================================
    story.append(make_role_banner(
        "ROLE 1: FRONTEND DEVELOPER VIVA VOCE (10 QUESTIONS & ANSWERS)",
        "Assigned Lead: Susnata Maiti (Roll No: A-11) • Scope: UI Architecture, Single Page Application, Client Routing, RxJS & State",
        FE_PRIMARY
    ))
    story.append(Spacer(1, 6))

    fe_questions = [
        ("Q1: What architectural pattern did you implement for the frontend in production versus the MEAN stack POC, and what influenced this choice?",
         "<b>Answer:</b><br/>"
         "• <b>Production Implementation:</b> We engineered a high-performance, responsive <b>Vanilla JavaScript Single Page Application (SPA)</b>. This architecture completely eliminated heavy client-side node build toolchains, bundler overhead, and runtime hydrate delays, achieving instant First Contentful Paint (&lt;450ms) across constrained campus Wi-Fi networks and mobile devices.<br/>"
         "• <b>MEAN Stack POC Equivalent:</b> In <code>mean_stack_equivalent/client</code>, we developed a modern <b>Angular 17+ SPA</b> utilizing Standalone Components, Angular Signals for reactive local state, and dependency-injected services. This demonstrated enterprise-grade modularity, TypeScript type checking, and RxJS observable streaming.<br/>"
         "• <b>Decision Rationale:</b> Vanilla JS was chosen for production edge deployment to optimize cold starts and eliminate version churn on Vercel, while the Angular POC established polyglot enterprise architectural competency."),

        ("Q2: How does client-side routing work in your Single Page Application without triggering full browser reloads?",
         "<b>Answer:</b><br/>"
         "• In standard multi-page applications, clicking a link issues a fresh HTTP GET request for a full HTML document, resulting in a blank screen flash and state loss.<br/>"
         "• In our SPA, routing is managed purely on the client: navigation links intercept click events (`event.preventDefault()`) and utilize the browser's <b>HTML5 History API (<code>history.pushState()</code> and the <code>popstate</code> window event)</b> or view-state controllers.<br/>"
         "• The application dynamically shows and hides pre-rendered view containers (e.g., <code>#authView</code>, <code>#studentDashboard</code>, <code>#adminDashboard</code>) by toggling CSS classes and updating DOM subtrees. Browser back/forward navigation triggers <code>popstate</code>, restoring the appropriate view state while preserving active application memory."),

        ("Q3: How does the frontend handle authentication, session persistence, and secure token transmission across API calls?",
         "<b>Answer:</b><br/>"
         "• <b>Token Receipt & Persistence:</b> Upon successful login (<code>POST /api/auth/login</code>), the backend returns a signed JSON Web Token (JWT) and user profile object. The frontend securely stores the token in <code>localStorage</code> (or <code>sessionStorage</code>) under the key <code>iem_token</code>.<br/>"
         "• <b>Outbound Authorization:</b> Every subsequent authenticated request (via <code>fetch()</code> in Vanilla JS or <code>HttpClient</code> in Angular) retrieves this token and injects it into the standard HTTP header: <code>Authorization: Bearer &lt;token&gt;</code>.<br/>"
         "• <b>Client-Side Role Decoding:</b> The frontend parses the middle Base64URL-encoded section of the JWT to extract the payload (<code>role</code>, <code>email</code>, <code>exp</code>) for immediate UI rendering (displaying student vs. admin controls).<br/>"
         "• <b>Security Caveat:</b> Client-side decoding is strictly for user experience; actual security is 100% enforced on the server, which cryptographically verifies the HMAC-SHA256 signature on every request."),

        ("Q4: What is the distinction between client-side validation and server-side validation, and why can client-side validation never be trusted alone?",
         "<b>Answer:</b><br/>"
         "• <b>Client-Side Validation:</b> Implemented via HTML5 constraint attributes (<code>required</code>, <code>min='0'</code>, <code>max='100'</code>, <code>pattern</code>) and JavaScript event listeners (e.g., checking that marks are numeric and within 0–100, phone numbers have 10 digits, and file sizes are &le;5MB before dispatch). Its sole purpose is <i>User Experience (UX)</i>—providing immediate visual feedback and preventing unnecessary network traffic.<br/>"
         "• <b>Server-Side Validation:</b> Executed inside the backend runtime via Pydantic models (FastAPI) or Mongoose schema validators (Node.js). It is the sole <i>Security Authority</i>.<br/>"
         "• <b>Why Client Validation Cannot Stand Alone:</b> Any malicious actor or student can bypass client validation entirely by disabling JavaScript in Developer Tools, crafting custom HTTP requests via cURL or Postman, or altering DOM attributes in the browser console. Without server-side validation, invalid scores or malicious payloads would corrupt the database."),

        ("Q5: How did you implement asynchronous multipart/form-data file uploads for marksheet PDFs from the frontend?",
         "<b>Answer:</b><br/>"
         "• Traditional JSON payloads (<code>application/json</code>) cannot natively encode raw binary file streams without inefficient Base64 text encoding, which adds ~33% bandwidth overhead.<br/>"
         "• <b>Implementation:</b> When an applicant selects their marksheet PDF, the frontend captures the native <code>File</code> reference from the <code>&lt;input type='file'&gt;</code> DOM element.<br/>"
         "• The frontend constructs a native JavaScript <code>FormData</code> object: <code>const formData = new FormData(); formData.append('marksheet', fileInput.files[0]);</code> and appends academic score metadata.<br/>"
         "• The request is dispatched via <code>fetch('/api/applications/submit', { method: 'POST', headers: { 'Authorization': `Bearer ${token}` }, body: formData })</code>.<br/>"
         "• <b>Crucial Detail:</b> We deliberately <i>omit</i> the <code>Content-Type</code> header manually; the browser automatically sets it to <code>multipart/form-data; boundary=----WebKitFormBoundary...</code>, allowing the server (Multer or python-multipart) to stream the file cleanly."),

        ("Q6: In the Angular POC, explain the purpose of RxJS Observables and how they differ from standard JavaScript Promises.",
         "<b>Answer:</b><br/>"
         "• In <code>mean_stack_equivalent/client/src/app/admission.service.ts</code>, all HTTP interactions utilize Angular's <code>HttpClient</code>, which returns <b>RxJS <code>Observable&lt;any&gt;</code></b> instances rather than ES6 Promises.<br/>"
         "• <b>Key Differences:</b><br/>"
         "  1. <i>Eager vs. Lazy Execution:</i> A Promise executes immediately upon creation. An Observable is lazy and does not initiate the underlying network call until a consumer calls <code>.subscribe()</code>.<br/>"
         "  2. <i>Single vs. Multiple Values:</i> A Promise resolves exactly one value (or error) and terminates. An Observable is an asynchronous stream that can emit zero, one, or multiple values over time.<br/>"
         "  3. <i>Cancellability:</i> Standard native Promises cannot be cancelled once dispatched. Observables can be cancelled cleanly at any time by calling <code>unsubscribe()</code> or using operators like <code>takeUntil()</code>, preventing memory leaks when users navigate away before slow uploads finish.<br/>"
         "  4. <i>Pipelining Operators:</i> Observables provide powerful functional operators (<code>map</code>, <code>filter</code>, <code>debounceTime</code>, <code>catchError</code>) for reactive transformation."),

        ("Q7: How does the frontend enforce Role-Based Access Control (RBAC) to ensure students cannot see or trigger administrative actions?",
         "<b>Answer:</b><br/>"
         "• <b>Client-Side View Gating:</b> After authentication, the frontend inspects the user's role (<code>student</code>, <code>admin</code>, or <code>director</code>).<br/>"
         "• In the Vanilla JS frontend, administrative navigation pills, metric widgets, and review action forms (Accept/Reject buttons and remarks textareas) are stored inside DOM elements with <code>role-restricted</code> classes, styled as <code>display: none</code> or removed entirely from the DOM tree for students.<br/>"
         "• In the Angular POC, route guards (<code>CanActivate</code>) check the user token, and structural directives (<code>*ngIf=\"userRole === 'admin'\"</code>) prevent unauthorized template elements from rendering.<br/>"
         "• <b>Defensive Layering:</b> Even if a student manually modifies client JavaScript to display admin buttons, clicking them sends an HTTP request carrying the student's JWT. The backend middleware intercepts the request and terminates it immediately with HTTP 403 Forbidden."),

        ("Q8: How did you protect the frontend from Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF)?",
         "<b>Answer:</b><br/>"
         "• <b>XSS Mitigation:</b> Cross-Site Scripting occurs when untrusted user input is executed as JavaScript in the browser. We strictly avoid <code>element.innerHTML = userInput</code>. Instead, we use <code>element.textContent = data</code> or safe DOM manipulation methods (<code>document.createTextNode</code>) which automatically encode HTML entities (`<`, `>`, `&`). In the Angular POC, Angular's built-in DomSanitizer automatically escapes unsafe values in data-bound templates.<br/>"
         "• <b>CSRF Mitigation:</b> Cross-Site Request Forgery relies on browsers automatically attaching session cookies to third-party cross-site requests. Because our architecture uses <b>stateless JWT tokens transmitted via custom HTTP headers (<code>Authorization: Bearer &lt;token&gt;</code>)</b> rather than ambient cookies, malicious third-party websites cannot forge authenticated requests, rendering classic CSRF attacks ineffective."),

        ("Q9: What design principles and techniques did you use to make the admission portal responsive across desktop, tablet, and mobile devices?",
         "<b>Answer:</b><br/>"
         "• <b>Mobile-First Responsive Layout:</b> We implemented modern CSS Flexbox and CSS Grid layout models combined with dynamic CSS media query breakpoints (<code>@media (max-width: 768px)</code> for mobile viewports and <code>@media (max-width: 1024px)</code> for tablets).<br/>"
         "• <b>Viewport Configuration:</b> Configured the standard responsive meta tag <code>&lt;meta name='viewport' content='width=device-width, initial-scale=1.0'&gt;</code> to ensure correct pixel scaling without pinch-to-zoom glitches.<br/>"
         "• <b>Component Adaptability:</b> On desktop, administrative tables display multi-column grids with academic scores, status badges, and action toolbars side-by-side. On mobile screens, tables automatically collapse into individual card-based stacked summaries with touch-friendly tap targets (&ge;48px hit areas)."),

        ("Q10: How does the frontend handle real-time feedback and status tracking for the applicant?",
         "<b>Answer:</b><br/>"
         "• <b>Status Mapping Engine:</b> The frontend maintains a visual status dictionary mapping the 5 lifecycle states (<code>Draft</code>, <code>Submitted</code>, <code>Under Review</code>, <code>Accepted</code>, <code>Rejected</code>) to distinct semantic visual badges:<br/>"
         "  - Draft: Slate/Gray badge (indicates editable form).<br/>"
         "  - Submitted: Blue badge with lock icon (indicates immutable form).<br/>"
         "  - Under Review: Amber badge with pulsing animation (indicates active faculty review).<br/>"
         "  - Accepted: Emerald green badge with checkmark.<br/>"
         "  - Rejected: Crimson red badge with an alert container showing reviewer remarks.<br/>"
         "• <b>Audit Timeline Rendering:</b> When viewing an application, the frontend iterates over the <code>auditTrail</code> array, dynamically constructing a vertical timeline displaying who changed the status, the exact timestamp, and any accompanying institutional remarks.")
    ]

    for q_idx, (q_text, a_text) in enumerate(fe_questions):
        q_box = [
            [Paragraph(f"<b>{q_text}</b>", style_q_title)],
            [Paragraph(a_text, style_a_body)]
        ]
        t_q = Table(q_box, colWidths=[495])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), FE_BG),
            ('BACKGROUND', (0, 1), (-1, 1), C_WHITE),
            ('BOX', (0, 0), (-1, -1), 1, FE_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(KeepTogether(t_q))
        story.append(Spacer(1, 4))

    # =========================================================================
    # ROLE 2: BACKEND DEVELOPER
    # =========================================================================
    story.append(PageBreak())
    story.append(make_role_banner(
        "ROLE 2: BACKEND DEVELOPER VIVA VOCE (10 QUESTIONS & ANSWERS)",
        "Assigned Lead: Sreejita Dey (Roll No: A-29) • Scope: Server Architecture, REST APIs, State Machine Logic, Cryptography & Guards",
        BE_PRIMARY
    ))
    story.append(Spacer(1, 8))

    be_questions = [
        ("Q1: Why was FastAPI chosen for production, and how does its ASGI asynchronous runtime compare with Node.js/Express in the POC?",
         "<b>Answer:</b><br/>"
         "• <b>FastAPI (Production):</b> Built on top of Starlette and Pydantic, running on an <b>ASGI (Asynchronous Server Gateway Interface)</b> server (Uvicorn). It leverages Python 3's native <code>async</code> and <code>await</code> coroutines to handle concurrent client I/O without blocking worker threads. Crucially, FastAPI natively supported our intelligent persistence router, automatic OpenAPI (Swagger) generation, and seamless DNS injection for campus networks.<br/>"
         "• <b>Express.js (MEAN POC):</b> Built on Node.js, running over Google's V8 single-threaded <b>Event Loop</b> backed by <code>libuv</code>'s thread pool for file and socket operations. Express handles concurrency via non-blocking asynchronous callback and Promise chains.<br/>"
         "• <b>Comparison:</b> Both runtimes offer world-class non-blocking I/O. However, FastAPI enforces compile-time and runtime type safety via Pydantic schemas, eliminating entire classes of type errors that in JavaScript require manual defensive runtime checks."),

        ("Q2: Trace the complete lifecycle of an incoming HTTP request in your backend from socket ingestion to response dispatch.",
         "<b>Answer:</b><br/>"
         "1. <i>Socket Ingestion & Protocol Handshake:</i> Uvicorn/Node.js accepts the raw TCP connection, parses HTTP headers, and invokes the server application callable.<br/>"
         "2. <i>CORS Global Middleware:</i> Evaluates the <code>Origin</code> header against whitelisted clients (e.g. <code>http://localhost:4200</code> or Vercel origins). Preflight <code>OPTIONS</code> requests are terminated with appropriate CORS approval headers.<br/>"
         "3. <i>Body Parsing / Streaming:</i> JSON payloads are parsed into structured memory models; multipart form data is routed to streaming file parsers.<br/>"
         "4. <i>Authentication Dependency / Middleware:</i> Extracts the <code>Authorization: Bearer &lt;token&gt;</code> header, decodes the JWT, and verifies the HMAC signature. On failure, halts execution with HTTP 401 Unauthorized.<br/>"
         "5. <i>RBAC Role Authorization Guard:</i> Validates whether <code>user.role</code> satisfies route permissions. On failure, halts execution with HTTP 403 Forbidden.<br/>"
         "6. <i>Controller & Business Logic:</i> The route handler processes data, invokes state machine transition checks, and queries the database via Mongoose or SQLite.<br/>"
         "7. <i>Serialization & HTTP Dispatch:</i> Results are serialized to standard JSON, formatted with appropriate HTTP status codes (200, 201), and flushed over the TCP socket."),

        ("Q3: How are passwords secured in your system, and how does your JWT authentication workflow operate?",
         "<b>Answer:</b><br/>"
         "• <b>Password Cryptography:</b> Plaintext passwords never touch persistent storage. In FastAPI production, passwords undergo <b>PBKDF2-HMAC-SHA256</b> key derivation with <b>600,000 hashing rounds</b> and unique cryptographically secure salts. In the MEAN POC, passwords use <b>bcryptjs</b> with 10 adaptive salt rounds. This renders precomputed rainbow table attacks impossible and imposes high computational cost against brute-force attacks.<br/>"
         "• <b>Constant-Time Verification:</b> During authentication, password comparisons use constant-time algorithms (<code>hmac.compare_digest</code>) to eliminate side-channel timing attacks.<br/>"
         "• <b>JWT Token Workflow:</b> Upon valid credentials, the server signs a JSON Web Token consisting of three Base64URL-encoded parts: Header (algorithm: <code>HS256</code>), Payload (<code>sub: user_id, role: role, exp: expiration</code>), and Signature (<code>HMAC-SHA256(header + '.' + payload, SECRET_KEY)</code>). The token is stateless; the server verifies validity on incoming requests without requiring a session database lookup."),

        ("Q4: Explain the mathematical and logical implementation of your Finite-State Machine (FSM) governing application lifecycles.",
         "<b>Answer:</b><br/>"
         "• The admission application lifecycle is modeled as a formal deterministic Finite-State Machine with 5 discrete states: $S = \\{\\text{Draft}, \\text{Submitted}, \\text{Under Review}, \\text{Accepted}, \\text{Rejected}\\}$.<br/>"
         "• <b>Legal State Transition Function $\\delta(s, a)$:</b><br/>"
         "  - $\\delta(\\text{Draft}, \\text{Submit}) \\rightarrow \\text{Submitted}$ (Applicant only; locks bio-data and marks).<br/>"
         "  - $\\delta(\\text{Submitted}, \\text{StartReview}) \\rightarrow \\text{Under Review}$ (Admin / Faculty only).<br/>"
         "  - $\\delta(\\text{Submitted}, \\text{Reject}) \\rightarrow \\text{Rejected}$ (Strictly requires non-empty remarks).<br/>"
         "  - $\\delta(\\text{Under Review}, \\text{Approve}) \\rightarrow \\text{Accepted}$ (Terminal state).<br/>"
         "  - $\\delta(\\text{Under Review}, \\text{Reject}) \\rightarrow \\text{Rejected}$ (Terminal state; requires remarks).<br/>"
         "• <b>Terminal State Invariance:</b> No transitions are defined from Accepted or Rejected ($\\{Accepted, Rejected\\} \\times \\Sigma \\rightarrow \\emptyset$). Any attempt to mutate a terminal application triggers an immediate HTTP 400 Bad Request error."),

        ("Q5: What is McCabe's Cyclomatic Complexity, and what is the exact complexity of your state transition validation function?",
         "<b>Answer:</b><br/>"
         "• <b>Theoretical Definition:</b> McCabe's Cyclomatic Complexity measures the number of linearly independent paths through a software program's source code. It is formally calculated from the control flow graph as:<br/>"
         "  $$\\mathbf{V(G) = E - N + 2P}$$, where $E$ = number of edges, $N$ = number of nodes, and $P$ = connected components ($P=1$).<br/>"
         "• <b>Alternative Predicate Formula:</b> $V(G) = P_d + 1$, where $P_d$ is the number of binary decision points (predicates).<br/>"
         "• <b>Application to our Code:</b> In our <code>validateTransition(currentStatus, targetStatus, remarks)</code> function, there are exactly <b>9 decision predicates</b> (checking current status enum values, verifying valid target transitions, checking for non-empty remarks on rejections, and blocking terminal mutations).<br/>"
         "• Therefore, $$V(G) = 9 + 1 = \\mathbf{10}$$.<br/>"
         "• <b>Testing Significance:</b> This mathematical proof dictates that the test suite must execute a minimum of <b>10 distinct, linearly independent test paths</b> to achieve 100% Basis Path and Statement Coverage."),

        ("Q6: How does the backend process file uploads securely without causing memory exhaustion or remote code execution?",
         "<b>Answer:</b><br/>"
         "• <b>Memory Safeguard (Streaming Ingestion):</b> Rather than buffering entire multi-megabyte files in RAM (which would exhaust server heap memory under concurrent student uploads), the backend streams bytes directly from the HTTP socket to disk storage via Multer (Node.js) or <code>python-multipart</code>.<br/>"
         "• <b>Size Threshold Enforcement:</b> Enforces a strict <b>5MB file size limit</b>. The stream monitor aborts the upload immediately and emits HTTP 413 Payload Too Large if the byte counter exceeds 5,242,880 bytes.<br/>"
         "• <b>MIME & Magic Byte Inspection:</b> Checks both the HTTP <code>Content-Type</code> header and inspects the binary file's initial magic header bytes (<code>%PDF-</code> or hex <code>25 50 44 46</code>) to ensure non-PDF executables (.exe, .sh, .bat) disguised with a <code>.pdf</code> extension are rejected with HTTP 415.<br/>"
         "• <b>UUID Sanitization:</b> Uploaded files are renamed using cryptographically random UUIDs (e.g. <code>marksheet-9b1deb4d3b7d.pdf</code>) before writing to <code>server/uploads/</code>, preventing Path Traversal (<code>../../</code>) and filename collision exploits."),

        ("Q7: How is server-side Role-Based Access Control (RBAC) enforced across sensitive backend routes?",
         "<b>Answer:</b><br/>"
         "• <b>Architecture:</b> RBAC is enforced strictly at the route layer before any business logic or controller executes.<br/>"
         "• <b>FastAPI Implementation:</b> Enforced using Python dependency injection:<br/>"
         "  <code>async def require_role(allowed: list[str], user = Depends(get_current_user)):</code><br/>"
         "  <code>&nbsp;&nbsp;&nbsp;&nbsp;if user['role'] not in allowed: raise HTTPException(status_code=403, detail='Access Denied')</code>.<br/>"
         "• <b>Express.js POC Implementation:</b> Enforced using sequential middleware:<br/>"
         "  <code>const requireRole = (roles) =&gt; (req, res, next) =&gt; {</code><br/>"
         "  <code>&nbsp;&nbsp;&nbsp;&nbsp;if (!roles.includes(req.user.role)) return res.status(403).json({ error: 'Forbidden' });</code><br/>"
         "  <code>&nbsp;&nbsp;&nbsp;&nbsp;next();</code><br/>"
         "  <code>};</code><br/>"
         "• Endpoints like <code>/api/admin/metrics</code> and <code>/api/applications/:id/status</code> require <code>['admin', 'director']</code>, ensuring students can never view aggregated data or approve admissions."),

        ("Q8: List the HTTP status codes your REST API returns and explain the precise conditions that trigger each.",
         "<b>Answer:</b><br/>"
         "• <b>200 OK:</b> Successful query execution (e.g., retrieving application details, fetching metrics, login token generation).<br/>"
         "• <b>201 Created:</b> Successful resource creation (e.g., user account registration, initial application submission).<br/>"
         "• <b>400 Bad Request:</b> Client payload semantic or state machine violation (e.g., marks &gt;100, rejecting an application without remarks, attempting to alter an Accepted/Rejected application).<br/>"
         "• <b>401 Unauthorized:</b> Missing, expired, or cryptographically invalid JWT token; invalid login credentials.<br/>"
         "• <b>403 Forbidden:</b> Authenticated user has valid credentials but lacks required role permissions (e.g., student accessing admin metrics).<br/>"
         "• <b>404 Not Found:</b> Requested resource does not exist (e.g., application ID not found in database).<br/>"
         "• <b>413 Payload Too Large:</b> Uploaded PDF marksheet exceeds the 5MB file size limit.<br/>"
         "• <b>415 Unsupported Media Type:</b> Uploaded file is not an authentic PDF document.<br/>"
         "• <b>500 Internal Server Error:</b> Unhandled backend server exception (e.g., database network timeout)."),

        ("Q9: How did you implement defensive error handling to prevent sensitive server data leakage and server crashes?",
         "<b>Answer:</b><br/>"
         "• <b>Global Exception Interceptors:</b> All unhandled exceptions are caught by centralized middleware handlers (FastAPI <code>@app.exception_handler</code> and Express 4-argument error middleware <code>(err, req, res, next)</code>).<br/>"
         "• <b>Information Shielding:</b> Raw database error messages, stack traces, and internal server file paths are logged internally to server logs for debugging but are <i>never</i> returned to the client. The client receives standardized JSON: <code>{ \"error\": \"Internal Server Error\", \"code\": \"ERR_INTERNAL\" }</code>.<br/>"
         "• <b>Process Resilience:</b> In Node.js, uncaught exceptions and unhandled promise rejections are hooked via <code>process.on('unhandledRejection')</code> to prevent the single-threaded Node process from crashing abruptly."),

        ("Q10: How does your backend generate administrative metrics without degrading database performance under high load?",
         "<b>Answer:</b><br/>"
         "• <b>The Naive Antipattern:</b> Fetching thousands of application documents into backend server memory and looping through them in Python/JavaScript creates massive memory bloat and saturates CPU bandwidth.<br/>"
         "• <b>Our Solution (Database-Level Native Aggregation):</b> In the MEAN stack POC, we execute a native MongoDB Aggregation Pipeline: <code>Application.aggregate([ { $match: { status: { $ne: 'Draft' } } }, { $group: { _id: '$status', count: { $sum: 1 } } } ])</code>.<br/>"
         "• In SQLite production, we execute: <code>SELECT status, department, COUNT(*) FROM applications WHERE status != 'Draft' GROUP BY status, department;</code>.<br/>"
         "• <b>Performance Result:</b> Computations are executed inside the optimized C++ database storage engine using indexed lookups, returning a tiny ~100-byte summary over the network to the backend.")
    ]

    for q_idx, (q_text, a_text) in enumerate(be_questions):
        q_box = [
            [Paragraph(f"<b>{q_text}</b>", style_q_title)],
            [Paragraph(a_text, style_a_body)]
        ]
        t_q = Table(q_box, colWidths=[495])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), BE_BG),
            ('BACKGROUND', (0, 1), (-1, 1), C_WHITE),
            ('BOX', (0, 0), (-1, -1), 1, BE_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(KeepTogether(t_q))
        story.append(Spacer(1, 4))

    # =========================================================================
    # ROLE 3: DATABASE MANAGER / LEAD
    # =========================================================================
    story.append(PageBreak())
    story.append(make_role_banner(
        "ROLE 3: DATABASE MANAGER & LEAD VIVA VOCE (10 QUESTIONS & ANSWERS)",
        "Assigned Lead: Swapnil Ghosh (Roll No: A-04) • Scope: Persistence Architecture, Dual-Engine Failover, Aggregation, Indexing & Schemas",
        DB_PRIMARY
    ))
    story.append(Spacer(1, 8))

    db_questions = [
        ("Q1: Explain the Dual-Engine Database Architecture of the IEM Admission System and the rationale behind it.",
         "<b>Answer:</b><br/>"
         "• <b>Architecture Overview:</b> The system employs a resilient Dual-Engine persistence model comprising **MongoDB Atlas Cloud** (primary NoSQL document engine) and **Local SQLite3** (instant secondary relational fallback engine).<br/>"
         "• <b>Engineering Rationale:</b> Academic institutions and enterprise campus networks frequently enforce strict firewall policies that block DNS SRV lookups and outbound TCP traffic on port 27017, or suffer intermittent WAN outages.<br/>"
         "• If an admission system relies solely on a single cloud database, an internet hiccup shuts down the entire admission process. Our dual-engine architecture guarantees 100% operational availability: if MongoDB Atlas becomes unreachable, the backend automatically and transparently routes all read/write operations to local SQLite storage (<code>iem_admission.db</code>) with zero application downtime."),

        ("Q2: How does the Dynamic Connection Router detect database failures and execute automated failover?",
         "<b>Answer:</b><br/>"
         "• <b>Active Health Probing:</b> Upon server boot, the persistence router initializes a connection to MongoDB Atlas with a strict timeout ceiling ($<4000$ms). It issues an active ping command: <code>client.admin.command('ping')</code>.<br/>"
         "• <b>DNS SRV Auto-Injection:</b> On academic networks that drop MongoDB's <code>mongodb+srv://</code> DNS queries, the router automatically reconfigures the process socket resolver to inject public Google DNS (<code>8.8.8.8</code>) and Cloudflare DNS (<code>1.1.1.1</code>).<br/>"
         "• <b>Graceful Fallover:</b> If the connection probe fails or times out after 4000ms, the router catches the exception, logs a warning, and initializes the local SQLite3 engine, ensuring table schemas and indexes are verified. API requests proceed seamlessly against SQLite."),

        ("Q3: Compare your schema design in MongoDB (NoSQL) with SQLite (Relational). How are Users, Applications, and Audit Logs modeled?",
         "<b>Answer:</b><br/>"
         "• <b>MongoDB Document Model:</b><br/>"
         "  - <code>users</code> collection: Stores accounts with unique email indexing, salted bcrypt password hashes, and enum roles (<code>['student', 'admin', 'director']</code>).<br/>"
         "  - <code>applications</code> collection: Rich document containing applicant bio-data, marks bounded by validators (<code>min: 0, max: 100</code>), <code>docReference</code> object, and an <b>embedded array of subdocuments: <code>auditTrail: [AuditLogSchema]</code></b>.<br/>"
         "• <b>SQLite Relational Model:</b><br/>"
         "  - Normalized into three tables: <code>users</code>, <code>applications</code>, and <code>audit_trail</code>.<br/>"
         "  - One-to-many relationship: <code>applications.id</code> acts as a Foreign Key in <code>audit_trail.application_id</code> with <code>ON DELETE CASCADE</code>.<br/>"
         "• <b>Comparison:</b> MongoDB leverages document embedding for atomic updates of applications and audit logs in a single write operation, whereas SQLite uses foreign keys and normalized relational tables."),

        ("Q4: Why did you implement the Decoupled Reference Pattern for PDF marksheets instead of storing files directly in MongoDB via GridFS or Base64?",
         "<b>Answer:</b><br/>"
         "• <b>The 16MB Document Limit:</b> MongoDB enforces a strict, hard-coded 16MB maximum document size to prevent individual documents from consuming excessive RAM during queries.<br/>"
         "• <b>WiredTiger Cache Thrashing:</b> Storing 5MB PDF binaries (or Base64 strings) inside database documents bloats document sizes by megabytes. When MongoDB loads documents into its WiredTiger cache memory, multi-megabyte payloads push active indexes out of RAM, causing severe cache thrashing, high disk I/O, and massive query latency spikes.<br/>"
         "• <b>Our Decoupled Pattern:</b> Multer streams the raw binary directly to the filesystem at <code>server/uploads/</code>. The database document stores strictly a lightweight <b>~150-byte metadata reference</b> (<code>{ filename, filepath, mimetype, size }</code>). This keeps documents tiny, maximizes cache hit ratios, and maintains lightning-fast queries."),

        ("Q5: What indexing strategies did you implement in the database, and what is their concrete performance impact?",
         "<b>Answer:</b><br/>"
         "• <b>Unique Index on <code>users.email</code>:</b> Enforces database-level account uniqueness. Converts user authentication lookups from an $O(N)$ full-collection scan into an $O(\\log N)$ B-tree index lookup, executing in sub-millisecond time.<br/>"
         "• <b>Foreign Key Index on <code>applications.applicant_id</code>:</b> Enables instantaneous retrieval of an applicant's active submission when they log into their dashboard.<br/>"
         "• <b>Compound Index on <code>applications (status, department)</code>:</b> Directly accelerates administrative filtering and metric aggregation queries, allowing the database engine to group records by status and department entirely within index memory without scanning unindexed document fields.<br/>"
         "• <b>Write Cost Awareness:</b> We avoided over-indexing; every additional index imposes write amplification overhead during inserts and updates."),

        ("Q6: How do MongoDB Aggregation Pipelines work, and how did you implement the `$match` and `$group` pipeline stages?",
         "<b>Answer:</b><br/>"
         "• <b>Concept:</b> MongoDB's Aggregation Framework processes documents through a multi-stage sequential data transformation pipeline, analogous to Unix pipes (<code>|</code>).<br/>"
         "• <b>Our Metric Aggregation Pipeline:</b><br/>"
         "  <code>Application.aggregate([</code><br/>"
         "  <code>&nbsp;&nbsp;{ $match: { status: { $ne: 'Draft' } } },</code><br/>"
         "  <code>&nbsp;&nbsp;{ $group: { _id: '$status', totalCount: { $sum: 1 }, avgScore: { $avg: '$score_12' } } }</code><br/>"
         "  <code>])</code><br/>"
         "• <b>Stage 1 (<code>$match</code>):</b> Filters out unsubmitted 'Draft' applications immediately, pruning the working dataset before grouping.<br/>"
         "• <b>Stage 2 (<code>$group</code>):</b> Groups remaining documents by the distinct <code>status</code> field, calculating the count and average score in parallel directly inside the database C++ engine, returning only a compact summary array."),

        ("Q7: How do you enforce data integrity and validation at the database schema layer?",
         "<b>Answer:</b><br/>"
         "• <b>Mongoose Schema Validators (MongoDB):</b><br/>"
         "  - Email validator: Enforces regex pattern and converts strings to lowercase before storage.<br/>"
         "  - Numerical range bounds: <code>score_10: { type: Number, required: true, min: 0, max: 100 }</code> prevents negative marks or values &gt;100.<br/>"
         "  - Enum constraints: <code>status: { type: String, enum: ['Draft', 'Submitted', 'Under Review', 'Accepted', 'Rejected'] }</code> rejects unauthorized status states.<br/>"
         "• <b>SQLite Table Constraints:</b><br/>"
         "  - Uses SQL <code>CHECK</code> constraints: <code>CHECK (score_10 BETWEEN 0 AND 100 AND score_12 BETWEEN 0 AND 100)</code>.<br/>"
         "  - Enforces <code>NOT NULL</code> on mandatory bio-data fields and <code>UNIQUE</code> on user emails."),

        ("Q8: What are ACID properties, and how do MongoDB and SQLite differ in their handling of ACID transactions?",
         "<b>Answer:</b><br/>"
         "• <b>ACID Definitions:</b><br/>"
         "  - <i>Atomicity:</i> All operations in a transaction succeed, or none are applied (all-or-nothing).<br/>"
         "  - <i>Consistency:</i> Transactions transition the database from one valid state to another, preserving constraints.<br/>"
         "  - <i>Isolation:</i> Concurrent transactions execute without cross-transaction interference.<br/>"
         "  - <i>Durability:</i> Once committed, data persists permanently even during a power outage.<br/>"
         "• <b>SQLite:</b> Fully ACID-compliant out of the box using Write-Ahead Logging (WAL) mode for high-concurrency read/write operations.<br/>"
         "• <b>MongoDB:</b> Guarantees ACID atomicity at the <i>single-document level</i>. Because our application and its audit trail are stored within the same document (embedded subdocuments), updating the application and appending the audit log is naturally atomic without requiring distributed locks. MongoDB also supports multi-document transactions via two-phase commit when required."),

        ("Q9: Why is an immutable Audit Trail critical in an admission system, and how is it implemented in the database?",
         "<b>Answer:</b><br/>"
         "• <b>Academic & Legal Necessity:</b> In university admission software, administrative decisions (approving or rejecting students) carry legal and accreditation consequences. The system must prevent repudiation and guarantee transparency.<br/>"
         "• <b>Implementation:</b> Every state transition appends a new immutable log record to the <code>auditTrail</code> array: <code>{ previousStatus, newStatus, changedBy: userId, actorRole, remarks, timestamp: ISODate() }</code>.<br/>"
         "• <b>Immutability Principle:</b> The database models provide <i>no update or delete APIs</i> for audit trail items; records can only be appended. This creates an unalterable chronological ledger proving exactly which faculty member reviewed an application, when the action occurred, and why."),

        ("Q10: What disaster recovery, backup, and database migration strategies would you deploy for production?",
         "<b>Answer:</b><br/>"
         "• <b>MongoDB Atlas Backup:</b> Continuous cloud snapshots with Point-In-Time Recovery (PITR) allowing restoration to any exact minute within the last 7 days; automated daily snapshots retained for 30 days across multiple geographic regions.<br/>"
         "• <b>SQLite Backup Strategy:</b> Automated cron jobs utilizing SQLite's native online backup API (<code>sqlite3_backup_init</code>) or the CLI <code>.backup</code> command to copy <code>iem_admission.db</code> while live without acquiring exclusive write locks.<br/>"
         "• <b>Migration & Syncing:</b> For bi-directional synchronization between local SQLite failover records and MongoDB Atlas upon WAN restoration, an idempotent reconciliation worker scans local change logs (using timestamp watermarks) and executes upserts (<code>$setOnInsert</code> / <code>updateOne</code>) to sync data.")
    ]

    for q_idx, (q_text, a_text) in enumerate(db_questions):
        q_box = [
            [Paragraph(f"<b>{q_text}</b>", style_q_title)],
            [Paragraph(a_text, style_a_body)]
        ]
        t_q = Table(q_box, colWidths=[495])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), DB_BG),
            ('BACKGROUND', (0, 1), (-1, 1), C_WHITE),
            ('BOX', (0, 0), (-1, -1), 1, DB_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(KeepTogether(t_q))
        story.append(Spacer(1, 4))

    # =========================================================================
    # ROLE 4: TEST LEAD & QA ENGINEER
    # =========================================================================
    story.append(PageBreak())
    story.append(make_role_banner(
        "ROLE 4: TEST LEAD & QA ENGINEER VIVA VOCE (10 QUESTIONS & ANSWERS)",
        "Assigned Lead: Debadrita Dutta (Roll No: A-12) • Scope: Testing Methodology, BVA, Equivalence Partitioning, Basis Path Testing, Security & Defect Tracking",
        QA_PRIMARY
    ))
    story.append(Spacer(1, 6))

    qa_questions = [
        ("Q1: Explain your overall testing strategy and testing pyramid for the IEM Admission System.",
         "<b>Answer:</b><br/>"
         "• <b>Testing Pyramid Alignment:</b> Our quality assurance strategy adheres to the standard 3-tier Testing Pyramid:<br/>"
         "  1. <i>Unit Testing (Base Layer):</i> Automated tests evaluating isolated business logic functions (e.g. <code>validateTransition()</code>, password hash verification, mark range validation) using Pytest / Mocha.<br/>"
         "  2. <i>Integration Testing (Middle Layer):</i> Testing interaction between coupled modules: testing whether Express/FastAPI routes correctly invoke database queries, test file streaming to <code>/uploads</code>, and verify JWT middleware guards.<br/>"
         "  3. <i>System & End-to-End Testing (Top Layer):</i> Comprehensive end-to-end user journey validation from frontend UI registration through document upload to admin status approval.<br/>"
         "• <b>Methodological Balance:</b> Combines formal <b>Black-Box Testing</b> (Equivalence Partitioning, Boundary Value Analysis) with <b>White-Box Testing</b> (Basis Path Testing with Cyclomatic Complexity $V(G)=10$)."),

        ("Q2: How did you apply Equivalence Partitioning (EP) to test the academic score input fields?",
         "<b>Answer:</b><br/>"
         "• <b>Equivalence Partitioning Theory:</b> EP divides the input domain into distinct classes of equivalent data where the software is expected to handle all elements of a class identically, minimizing redundant tests.<br/>"
         "• <b>Input Field:</b> Academic Percentage Score (Class 10 and 12 marks). Valid range: $0 \\le x \\le 100$.<br/>"
         "• <b>Partition Classes Derived:</b><br/>"
         "  - <i>Valid Equivalence Class (V1):</i> $0 \\le x \\le 100$ (Test values: <code>75.5</code>, <code>88.0</code>). Expected: Accepted, HTTP 200/201.<br/>"
         "  - <i>Invalid Equivalence Class (I1 - Negative Marks):</i> $x &lt; 0$ (Test values: <code>-5.0</code>, <code>-0.01</code>). Expected: Rejected, validation error HTTP 400.<br/>"
         "  - <i>Invalid Equivalence Class (I2 - Excessive Marks):</i> $x &gt; 100$ (Test values: <code>101.0</code>, <code>150.0</code>). Expected: Rejected, validation error HTTP 400.<br/>"
         "  - <i>Invalid Equivalence Class (I3 - Non-Numeric Input):</i> Strings, special symbols, empty strings (Test values: <code>'eighty'</code>, <code>'#@%'</code>, <code>''</code>). Expected: Rejected with schema type error."),

        ("Q3: How did you apply Boundary Value Analysis (BVA) to test score validations and file upload limits?",
         "<b>Answer:</b><br/>"
         "• <b>Boundary Value Analysis Theory:</b> Defects cluster disproportionately at boundary edges rather than in center ranges. BVA tests the precise minimum, maximum, and adjacent values (min-1, min, min+1, max-1, max, max+1).<br/>"
         "• <b>Academic Score Boundaries ($0$ and $100$):</b><br/>"
         "  - Lower Boundary: <code>-0.01</code> (Reject), <code>0.00</code> (Accept - boundary minimum), <code>0.01</code> (Accept).<br/>"
         "  - Upper Boundary: <code>99.99</code> (Accept), <code>100.00</code> (Accept - boundary maximum), <code>100.01</code> (Reject).<br/>"
         "• <b>PDF File Upload Boundary ($5.0\\text{ MB} = 5,242,880\\text{ bytes}$):</b><br/>"
         "  - <code>0 bytes</code>: Rejected (Empty file validation).<br/>"
         "  - <code>1 byte</code>: Accepted (Valid non-empty PDF structure).<br/>"
         "  - <code>5,242,879 bytes</code>: Accepted (Under 5MB ceiling).<br/>"
         "  - <code>5,242,880 bytes</code>: Accepted (Exact 5MB limit).<br/>"
         "  - <code>5,242,881 bytes</code>: Rejected with HTTP 413 Payload Too Large."),

        ("Q4: Walk through your Basis Path Testing of the State Machine and list the 10 linearly independent basis test paths.",
         "<b>Answer:</b><br/>"
         "• With Cyclomatic Complexity $V(G) = 10$, exactly 10 independent basis paths exist through <code>validateTransition(current, target, remarks)</code>:<br/>"
         "  1. <i>Path 1 (Normal Submit):</i> Draft &rarr; Submitted (Valid &rarr; Success).<br/>"
         "  2. <i>Path 2 (Illegal Draft Jump):</i> Draft &rarr; Under Review (Invalid jump &rarr; Error).<br/>"
         "  3. <i>Path 3 (Illegal Draft Accept):</i> Draft &rarr; Accepted (Invalid jump &rarr; Error).<br/>"
         "  4. <i>Path 4 (Triage Initiation):</i> Submitted &rarr; Under Review (Valid &rarr; Success).<br/>"
         "  5. <i>Path 5 (Direct Rejection w/ remarks):</i> Submitted &rarr; Rejected with non-empty remarks (Valid &rarr; Success).<br/>"
         "  6. <i>Path 6 (Direct Rejection w/o remarks):</i> Submitted &rarr; Rejected with empty remarks (Invalid &rarr; Error).<br/>"
         "  7. <i>Path 7 (Review Approval):</i> Under Review &rarr; Accepted (Valid &rarr; Success).<br/>"
         "  8. <i>Path 8 (Review Rejection w/ remarks):</i> Under Review &rarr; Rejected with non-empty remarks (Valid &rarr; Success).<br/>"
         "  9. <i>Path 9 (Review Rejection w/o remarks):</i> Under Review &rarr; Rejected with empty remarks (Invalid &rarr; Error).<br/>"
         "  10. <i>Path 10 (Terminal Mutation Attempt):</i> Accepted / Rejected &rarr; Any State (Terminal lock &rarr; Error).<br/>"
         "• Executing these 10 automated test cases achieves 100% statement and decision branch coverage."),

        ("Q5: How did you conduct Security Testing for Authentication, JWT integrity, and Role Escalation?",
         "<b>Answer:</b><br/>"
         "• <b>JWT Signature Tampering Test:</b> We captured a valid student JWT, decoded the Base64 payload, changed <code>\"role\": \"student\"</code> to <code>\"role\": \"admin\"</code>, re-encoded without updating the secret signature, and dispatched it to <code>GET /api/admin/metrics</code>. Expected Result: Backend verification failed; returned HTTP 401 Unauthorized.<br/>"
         "• <b>Expired Token Test:</b> Minted a JWT with an expired timestamp (<code>exp = now - 3600</code>). Dispatched request. Expected Result: HTTP 401 Unauthorized with token expired error.<br/>"
         "• <b>Vertical Privilege Escalation Test:</b> Authenticated as a student with valid unexpired token, attempted to invoke <code>PATCH /api/applications/:id/status</code> to approve an admission. Expected Result: HTTP 403 Forbidden.<br/>"
         "• <b>Horizontal Privilege Escalation Test:</b> Authenticated as Student A, attempted to access application record belonging to Student B via <code>GET /api/applications/STUDENT_B_ID</code>. Expected Result: HTTP 403 / 404 Access Denied."),

        ("Q6: How did you test the Database Failover Mechanism from MongoDB Atlas to SQLite3?",
         "<b>Answer:</b><br/>"
         "• <b>Fault Injection Methodology:</b> We conducted simulated chaos testing during active application execution:<br/>"
         "  1. <i>DNS Blackholing:</i> Blocked DNS lookups to MongoDB Atlas clusters by routing <code>*.mongodb.net</code> to <code>127.0.0.1</code> via local host files.<br/>"
         "  2. <i>Socket Severing:</i> Blocked outgoing TCP traffic on port 27017 via Windows Firewall rules.<br/>"
         "• <b>Verification Metrics:</b><br/>"
         "  - Verified that the backend persistence router logged the connection timeout and completed fallback initialization in <b>&lt;4000ms</b>.<br/>"
         "  - Dispatched synthetic applicant registration and login requests immediately after socket severing.<br/>"
         "  - Verified that all CRUD operations completed successfully against <code>iem_admission.db</code> (SQLite) with HTTP 201/200, confirming zero service downtime."),

        ("Q7: What is Regression Testing, and how did you guarantee that bug fixes and new features did not break existing modules?",
         "<b>Answer:</b><br/>"
         "• <b>Concept:</b> Regression testing re-runs existing test suites to confirm that recent code modifications, bug resolutions, or environment updates have not inadvertently broken previously working functionality.<br/>"
         "• <b>Implementation:</b><br/>"
         "  - Maintained an automated regression test suite executed via <code>pytest</code> and <code>npm test</code>.<br/>"
         "  - Core regression suites covered: User registration & bcrypt login verification, application creation and score validation, marksheet upload integrity, state transition validation, and dashboard metric calculations.<br/>"
         "  - Whenever a bug was reported (e.g. rejection allowed without remarks), a dedicated regression test reproducing the defect was authored first, verified to fail, and then verified to pass permanently after the patch was merged."),

        ("Q8: Describe your Defect Lifecycle and explain how bug severity and priority were categorized in your project.",
         "<b>Answer:</b><br/>"
         "• <b>Defect Lifecycle States:</b> <code>New &rarr; Assigned &rarr; Open &rarr; Fixed &rarr; Retest &rarr; Verified &rarr; Closed</code> (or <code>Reopened</code> if retest failed).<br/>"
         "• <b>Severity vs. Priority Matrix:</b><br/>"
         "  - <i>Critical Severity / High Priority:</i> System crashes, database failover malfunction, JWT signature bypass, or data corruption. Handled immediately before any other work.<br/>"
         "  - <i>High Severity / High Priority:</i> State machine allowing illegal transitions (e.g. Draft &rarr; Accepted), student able to submit marks &gt;100.<br/>"
         "  - <i>Medium Severity / Medium Priority:</i> Validation error messages returning unclear text, file upload spinner freezing after completion.<br/>"
         "  - <i>Low Severity / Low Priority:</i> Minor CSS badge misalignments on mobile screens, typo in help modal text."),

        ("Q9: How did you test file upload edge cases, malicious file injections, and MIME spoofing?",
         "<b>Answer:</b><br/>"
         "• <b>Oversized File Test:</b> Uploaded a 6.2MB marksheet PDF. Verified upload stream was terminated with HTTP 413 Payload Too Large.<br/>"
         "• <b>Zero-Byte File Test:</b> Uploaded an empty 0-byte file named <code>marksheet.pdf</code>. Verified rejection with validation error.<br/>"
         "• <b>MIME Spoofing / Magic Byte Test:</b> Renamed a Python script (<code>exploit.py</code>) and a Windows executable (<code>malware.exe</code>) to <code>marksheet.pdf</code> with <code>Content-Type: application/pdf</code>. Verified that server-side binary header inspection detected missing <code>%PDF-</code> magic bytes and rejected the file with HTTP 415.<br/>"
         "• <b>Path Traversal Filename Test:</b> Uploaded a file named <code>../../../../etc/passwd.pdf</code>. Verified server sanitized filename into a clean random UUID (<code>marksheet-[uuid].pdf</code>), eliminating path traversal risks."),

        ("Q10: What Non-Functional Testing (NFT) did you perform to assess system performance, usability, and accessibility?",
         "<b>Answer:</b><br/>"
         "• <b>Performance & Latency Benchmarking:</b> Used load testing tools to measure server response latency under concurrent applicant loads; verified that API endpoints responded in <b>&lt;200ms</b> on SQLite and <b>&lt;450ms</b> on MongoDB Atlas.<br/>"
         "• <b>Cross-Browser & Cross-Device Compatibility:</b> Verified rendering and functional workflows across Google Chrome, Microsoft Edge, Mozilla Firefox, and mobile Safari.<br/>"
         "• <b>Usability & Accessibility (WCAG 2.1 AA):</b> Evaluated visual color contrast ratios (text vs. badge backgrounds &gt;4.5:1), verified full keyboard tab navigation across form inputs, and verified ARIA attributes on modal dialogs and alert banners.")
    ]

    for q_idx, (q_text, a_text) in enumerate(qa_questions):
        q_box = [
            [Paragraph(f"<b>{q_text}</b>", style_q_title)],
            [Paragraph(a_text, style_a_body)]
        ]
        t_q = Table(q_box, colWidths=[495])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), QA_BG),
            ('BACKGROUND', (0, 1), (-1, 1), C_WHITE),
            ('BOX', (0, 0), (-1, -1), 1, QA_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(KeepTogether(t_q))
        story.append(Spacer(1, 4))

    # =========================================================================
    # APPENDIX: STRATEGIC EXAMINER SCORING TIPS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("STRATEGIC EXAMINER SCORING TIPS FOR TEAM NEXUS (P4)", style_h2))
    story.append(Paragraph(
        "To achieve maximum grades during the lab viva examination, team members should adhere to the following communication guidelines:",
        style_a_body
    ))
    story.append(Spacer(1, 4))

    scoring_tips = [
        [Paragraph("<b>Susnata Maiti<br/>(Frontend Dev):</b>", style_meta_k),
         Paragraph("Focus on <b>user experience vs. server security authority</b>: clearly explain that while client validation provides snappy UX, server validation is the only true defense. Highlight the HTML5 History API for SPA navigation and why Bearer JWT headers avoid CSRF.", style_meta_v)],
        [Paragraph("<b>Sreejita Dey<br/>(Backend Dev):</b>", style_meta_k),
         Paragraph("Lead with exact numbers and algorithms: <b>600,000 PBKDF2 hashing rounds</b>, <b>$V(G) = 10$</b> Cyclomatic Complexity basis paths, <b>5MB file streaming limits</b>, and sequential middleware error containment.", style_meta_v)],
        [Paragraph("<b>Swapnil Ghosh<br/>(Database Lead):</b>", style_meta_k),
         Paragraph("Emphasize <b>architectural resilience</b>: explain why Dual-Engine fallback with Google DNS injection was necessary for campus networks, and articulate the <b>Decoupled Reference Pattern</b> (preventing 16MB document limits and WiredTiger cache thrashing).", style_meta_v)],
        [Paragraph("<b>Debadrita Dutta<br/>(Test Lead):</b>", style_meta_k),
         Paragraph("Present the rigorous mathematical basis of testing: <b>Equivalence Partitioning & Boundary Value Analysis</b> on scores/file limits, <b>Basis Path Testing</b> deriving all 10 independent execution paths, and fault injection for database failover.", style_meta_v)],
        [Paragraph("<b>Unified Team Stance:</b>", style_meta_k),
         Paragraph("Highlight cross-functional synergy: e.g., how the Tester's boundary values reflected the Database schema constraints, and how Frontend form encoders matched Backend Multer stream parsers.", style_meta_v)]
    ]
    t_tips = Table(scoring_tips, colWidths=[120, 375])
    t_tips.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fefce8")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#fde047")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#fef08a")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_tips)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Role-based viva PDF successfully compiled at: {out_path}")

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_pdf = os.path.join(root_dir, "Role_Based_Viva_Questions_and_Answers.pdf")
    docs_pdf = os.path.join(root_dir, "docs", "Role_Based_Viva_Questions_and_Answers.pdf")
    temp_pdf = os.path.join(root_dir, "docs", "temp_role_viva_build.pdf")

    build_role_viva_pdf(temp_pdf)

    # Always update docs copy
    shutil.copyfile(temp_pdf, docs_pdf)
    print(f"Docs copy saved at: {docs_pdf}")

    # Try updating root copy
    try:
        shutil.copyfile(temp_pdf, target_pdf)
        print(f"Root copy saved at: {target_pdf}")
    except PermissionError:
        fallback_pdf = os.path.join(root_dir, "Role_Based_Viva_Questions_and_Answers_Latest.pdf")
        shutil.copyfile(temp_pdf, fallback_pdf)
        print(f"[NOTE] Root target locked; saved at fallback: {fallback_pdf}")

    if os.path.exists(temp_pdf):
        os.remove(temp_pdf)
