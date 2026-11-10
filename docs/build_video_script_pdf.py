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

# Color Palette matching DOCX / IEEE Paper
C_NAVY = colors.HexColor("#1e3a8a")        # Navy 900
C_PRIMARY = colors.HexColor("#2563eb")     # Blue 600
C_PRIMARY_LIGHT = colors.HexColor("#eff6ff")# Blue 50
C_DARK = colors.HexColor("#0f172a")        # Slate 900
C_MUTED = colors.HexColor("#334155")       # Slate 700
C_BORDER = colors.HexColor("#cbd5e1")      # Slate 300
C_BORDER_BLUE = colors.HexColor("#93c5fd") # Blue 300
C_ROW_BG = colors.HexColor("#f8fafc")      # Slate 50
C_WHITE = colors.HexColor("#ffffff")

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
        footer_text = "IEM Admission System Software  •  Video Demonstration Script  •  Team Nexus (P4)"
        self.drawString(54, 36, footer_text)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 54, 36, page_str)

        # Running header (on pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, A4[1] - 36, "IEM Admission System — Technical Video Demonstration Script")
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

    # Custom Paragraph Styles
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
        fontSize=20,
        leading=24,
        textColor=C_NAVY,
        spaceAfter=4
    )

    style_subtitle = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=C_MUTED,
        spaceAfter=10
    )

    style_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=C_NAVY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=C_PRIMARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=C_MUTED,
        spaceAfter=6
    )

    style_meta_key = ParagraphStyle(
        'MetaKey',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=C_DARK
    )

    style_meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
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
        fontSize=8.2,
        leading=11,
        textColor=C_MUTED
    )

    style_td_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11,
        textColor=C_DARK
    )

    style_visual = ParagraphStyle(
        'VisualCue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=C_DARK
    )

    style_narration = ParagraphStyle(
        'NarrationText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=C_DARK
    )

    story = []

    # Title & Header
    story.append(Paragraph("PCCCS504 SOFTWARE ENGINEERING & PROJECT MANAGEMENT LAB  •  ACADEMIC YEAR 2026-27", style_category))
    story.append(Paragraph("Video Demonstration Script: IEM Admission System Software", style_title))
    story.append(Paragraph("Production-Ready Walkthrough Script from GitHub to Live Cloud Deployment", style_subtitle))

    # Metadata Container Table
    meta_rows = [
        [Paragraph("<b>Target Duration:</b>", style_meta_key), Paragraph("~9 Minutes 30 Seconds (Strictly &le; 10 Minutes at ~135 words/minute)", style_meta_val)],
        [Paragraph("<b>Initial View:</b>", style_meta_key), Paragraph("Google Chrome on Windows 11 with GitHub Repository tab open (Susnata-Maiti/IEM-Admission-System)", style_meta_val)],
        [Paragraph("<b>Live URL:</b>", style_meta_key), Paragraph("https://iem-admission-system-nexus-p4.vercel.app/ (Vercel Edge CDN + MongoDB Atlas Cloud)", style_meta_val)],
        [Paragraph("<b>Interactive Docs:</b>", style_meta_key), Paragraph("https://iem-admission-system-nexus-p4.vercel.app/docs (FastAPI OpenAPI / Swagger UI)", style_meta_val)],
        [Paragraph("<b>Team Details:</b>", style_meta_key), Paragraph("Team Number: P4  |  Team Name: Nexus  |  Batch: 2024-2028 (Section A, 5th Sem)", style_meta_val)],
        [Paragraph("<b>Team Members:</b>", style_meta_key), Paragraph("Susnata Maiti (A-11, Frontend) | Sreejita Dey (A-29, Backend) | Swapnil Ghosh (A-04, Database) | Debadrita Dutta (A-12, Testing)", style_meta_val)],
        [Paragraph("<b>Faculty In-Charge:</b>", style_meta_key), Paragraph("Prof. Sangeeta Sarkar &amp; Prof. Saikat Dutta", style_meta_val)],
        [Paragraph("<b>Project Sponsor:</b>", style_meta_key), Paragraph("Dr. Satyajit Chakrabarti (Director, Institute of Engineering &amp; Management, Kolkata)", style_meta_val)]
    ]
    t_meta = Table(meta_rows, colWidths=[110, 377])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER_BLUE),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dbeafe")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # Section 1: Pre-Recording Checklist
    story.append(Paragraph("1. Pre-Recording Setup & Environment Checklist", style_h1))
    checklist_rows = [
        [Paragraph("<b>Screen Setup:</b>", style_meta_key), Paragraph("Windows 11 Desktop display set to 1920&times;1080 (1080p). Hide browser bookmarks bar (Ctrl+Shift+B).", style_meta_val)],
        [Paragraph("<b>Browser Tabs:</b>", style_meta_key), Paragraph("Tab 1: GitHub repo at top. Tab 2: FastAPI Swagger docs (/docs) ready in background.", style_meta_val)],
        [Paragraph("<b>Sample Asset:</b>", style_meta_key), Paragraph("Valid sample PDF marksheet under 5MB (e.g. marksheet_sample.pdf, ~1.2MB) accessible on Desktop.", style_meta_val)],
        [Paragraph("<b>Audio & Pacing:</b>", style_meta_key), Paragraph("Quiet room with headset/mic. Target speed: ~130-140 wpm. Allow 1-2s pauses for UI transitions.", style_meta_val)]
    ]
    t_check = Table(checklist_rows, colWidths=[110, 377])
    t_check.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_check)
    story.append(Spacer(1, 10))

    # Section 2: Timing & Scene Summary Table
    story.append(Paragraph("2. Timing & Scene Overview Table", style_h1))
    story.append(Paragraph("The video demonstration is organized into 8 modular scenes totaling 9m 45s, staying strictly below the 10-minute limit:", style_body))

    scenes_summary = [
        ["Timestamp", "Scene / Section", "Primary Visual Focus", "Topics Covered"],
        ["0:00 - 0:45", "Scene 1: Launch & Intro", "GitHub Repo README in Chrome", "Team intro, PCCCS504 context, 20-day timeline, clicking live link."],
        ["0:45 - 2:00", "Scene 2: Landing & Reg", "Live Web Portal (/) Onboarding", "IEM crest, Google Sans font, @gmail.com validation, PBKDF2 hashing."],
        ["2:00 - 4:15", "Scene 3: 4-Step Wizard", "Application Stepper (/application)", "Personal data, academic scores, B.Tech CSE, PDF upload (<5MB), form lock."],
        ["4:15 - 5:30", "Scene 4: Student Dashboard", "Student Dashboard (/dashboard)", "Application ID, tracking timeline, marksheet preview, immutable lock."],
        ["5:30 - 7:15", "Scene 5: Admin Workspace", "Admin Console (/admin)", "Real-time KPI metrics, <1s search filter, Table/Card views, state updates."],
        ["7:15 - 8:15", "Scene 6: Director View", "Director Dashboard (/director)", "Executive bird's-eye metrics, read-only mode, one-click CSV export."],
        ["8:15 - 9:15", "Scene 7: Architecture & QA", "Swagger Docs (/docs) / Diagrams", "FastAPI ASGI engine, Dual-Engine DB abstraction, 100% basis path tests."],
        ["9:15 - 9:45", "Scene 8: Conclusion", "GitHub Repo / Presentation Slide", "Deliverables summary, faculty acknowledgments, and closing thanks."]
    ]

    t_scenes = []
    for r_idx, r_data in enumerate(scenes_summary):
        row_cells = []
        for c_idx, val in enumerate(r_data):
            if r_idx == 0:
                p = Paragraph(val, style_th)
            elif c_idx == 0:
                p = Paragraph(f"<b>{val}</b>", style_td_bold)
            elif c_idx == 1:
                p = Paragraph(f"<b>{val}</b>", style_td_bold)
            else:
                p = Paragraph(val, style_td)
            row_cells.append(p)
        t_scenes.append(row_cells)

    t_sc_table = Table(t_scenes, colWidths=[65, 120, 130, 172])
    t_sc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_ROW_BG]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_sc_table)
    story.append(Spacer(1, 14))

    # Section 3: Detailed Two-Column Production Script
    story.append(Paragraph("3. Detailed Two-Column Production Script (Visual Actions & Voiceover)", style_h1))
    story.append(Paragraph("Follow the left column for on-screen actions and read the right column word-for-word:", style_body))

    detailed_scenes = [
        {
            "num": 1,
            "title": "Scene 1: Introduction & Launch from GitHub",
            "time": "0:00 - 0:45 (45s)",
            "visual": (
                "<b>Screen:</b> Chrome browser showing GitHub repository <i>Susnata-Maiti/IEM-Admission-System</i>.<br/><br/>"
                "<b>Action:</b> Cursor hovers over repository title and team header in README.md.<br/><br/>"
                "Scroll smoothly down to Section <i>'🌐 Live Production Deployment'</i>.<br/><br/>"
                "<b>Action:</b> Hover mouse cursor over the live Vercel URL and click <u>https://iem-admission-system-nexus-p4.vercel.app/</u>."
            ),
            "narration": (
                "\"Hello everyone. Welcome to the technical demonstration of the <b>IEM Admission System Software</b>, "
                "engineered for the Software Engineering and Project Management Lab (PCCCS504) at the Institute of Engineering &amp; Management, Kolkata.<br/><br/>"
                "I am <b>Susnata Maiti</b>, Frontend Developer for <b>Team Nexus (P4)</b>. I am presenting on behalf of our team comprising "
                "<b>Sreejita Dey</b> as Backend Developer, <b>Swapnil Ghosh</b> as Database Lead, and <b>Debadrita Dutta</b> as Test Lead, "
                "under the guidance of our faculty in-charge <b>Prof. Sangeeta Sarkar</b>, <b>Prof. Saikat Dutta</b>, and our Project Sponsor and Director, <b>Dr. Satyajit Chakrabarti</b>.<br/><br/>"
                "Our objective was to deliver a resilient, user-focused college admission platform within an accelerated 20-day timeline. "
                "As documented in our repository README, the application is deployed live on Vercel with a global CDN edge, backed by MongoDB Atlas Cloud. "
                "Let us click our live production link and walk through the complete admission lifecycle in real time.\""
            )
        },
        {
            "num": 2,
            "title": "Scene 2: Landing Page, Design Standards & Student Registration",
            "time": "0:45 - 2:00 (75s)",
            "visual": (
                "<b>Screen:</b> Browser opens <i>https://iem-admission-system-nexus-p4.vercel.app/</i>.<br/><br/>"
                "<b>Action:</b> Point out the official IEM crest and clean Google Sans font. Toggle to 'Register' tab.<br/><br/>"
                "<b>Action:</b> In Name, type 'Susnata Maiti'. In Email, enter an invalid address 'susnata@yahoo.com' and click Register to demonstrate inline @gmail.com domain error toast.<br/><br/>"
                "<b>Action:</b> Correct email to 'maitisusnata135531@gmail.com'. In Password, type 'Student@2026!'. Click 'Create Account / Register'. Show success toast and automatic login."
            ),
            "narration": (
                "\"Here on our live production portal, the user interface adheres strictly to our SRS design specifications: "
                "featuring the official IEM laurel wreath crest, responsive container layouts, and clean typography rendered in <b>Google Sans</b>.<br/><br/>"
                "The system implements strict Role-Based Access Control separating Student Applicants, Admissions Administrators, and the Executive Director. "
                "Let us begin by registering a new student applicant.<br/><br/>"
                "Notice our client-side validation guard: if I input a non-Gmail address, the portal immediately rejects it because student registrations "
                "are restricted strictly to <b>@gmail.com</b> addresses. Once I provide my valid email—<i>maitisusnata135531@gmail.com</i>—and enter a password satisfying "
                "our complexity policy (minimum 8 characters with uppercase and special symbols), the client sends an asynchronous REST call to our FastAPI backend.<br/><br/>"
                "On the server side, passwords are never stored in plaintext—they are securely hashed using salted <b>PBKDF2-HMAC-SHA256</b>. "
                "The backend issues a signed JWT token, logging us in seamlessly.\""
            )
        },
        {
            "num": 3,
            "title": "Scene 3: The 4-Step Application Wizard & PDF Upload",
            "time": "2:00 - 4:15 (135s)",
            "visual": (
                "<b>Screen:</b> Application Wizard (/application).<br/><br/>"
                "<b>Action 1 (Step 1):</b> Point out 4-step progress stepper. Fill DOB: 15/08/2005, Phone: +91 98765 43210, Address: Salt Lake Sector V, Kolkata. Click Next.<br/><br/>"
                "<b>Action 2 (Step 2):</b> Enter Class 10 marks (92.5%, CBSE), Class 12 marks (90.0%, WBCHSE), Passing Year (2024). Select Course: 'B.Tech Computer Science &amp; Engineering'. Click Next.<br/><br/>"
                "<b>Action 3 (Step 3):</b> Drag and drop sample PDF marksheet (~1.2MB). Show file preview card with size verification. Click Next.<br/><br/>"
                "<b>Action 4 (Step 4):</b> Review consolidated summary. Point out Business Rule BR-02 immutability warning. Click 'Confirm &amp; Final Submit'."
            ),
            "narration": (
                "\"We are now guided into the <b>4-Step Application Wizard</b>. The top visual stepper anchors candidate progress, minimizing cognitive fatigue.<br/><br/>"
                "In Step 1, personal details are sanitized and checked for mandatory fields before enabling navigation to Step 2.<br/><br/>"
                "In Step 2, the candidate inputs academic scores and selects their target degree from a predefined list. "
                "Per Business Rule <b>BR-04</b>, percentages must fall strictly between 0.0% and 100.0%, enforced via Pydantic schema validation.<br/><br/>"
                "Step 3 implements <b>Module 1: Document Upload</b>. In compliance with requirement <b>FR-05</b>, uploads are restricted strictly to PDF format "
                "with an enforced 5 megabyte ceiling. Both client-side JavaScript and the FastAPI multipart stream validator inspect MIME headers "
                "to protect against malicious file uploads. The file is stored safely and linked to our record.<br/><br/>"
                "In Step 4, the student reviews their full application. Notice the explicit notice for Business Rule <b>BR-02</b>: once submitted, "
                "all personal, academic, and document fields become permanently immutable to protect admission integrity. Let us click 'Confirm and Final Submit'.\""
            )
        },
        {
            "num": 4,
            "title": "Scene 4: Student Dashboard & Real-Time Tracking Timeline",
            "time": "4:15 - 5:30 (75s)",
            "visual": (
                "<b>Screen:</b> Student Dashboard (/dashboard).<br/><br/>"
                "<b>Action:</b> Highlight the generated Application ID (e.g. IEM-2026-0847) and green status badge: 'SUBMITTED'.<br/><br/>"
                "<b>Action:</b> Point out chronological progress timeline: Application Submitted (Completed) &rarr; Under Review (Pending) &rarr; Final Decision (Pending).<br/><br/>"
                "<b>Action:</b> Click 'View / Download Uploaded Marksheet' button to preview the PDF in a new browser tab.<br/><br/>"
                "<b>Action:</b> Click 'Sign Out' in top navbar to return to login page."
            ),
            "narration": (
                "\"The portal redirects immediately to the <b>Student Dashboard</b>, satisfying requirements <b>FR-10</b> and <b>FR-11</b>. "
                "Notice our assigned application identifier—<b>IEM-2026-0847</b>—and the active status badge marked 'Submitted'.<br/><br/>"
                "Below the summary card is our chronological tracking timeline. The candidate can clearly track their progress through document triage "
                "and departmental review. Candidates can also preview or download their uploaded PDF marksheets anytime to verify their records. "
                "Per requirement <b>FR-09</b>, editing controls have been completely removed—the record is securely locked against further edits.<br/><br/>"
                "Now, let us log out of the student session and log in as an Admissions Administrator to process this application.\""
            )
        },
        {
            "num": 5,
            "title": "Scene 5: Administrator Workspace & State Machine Workflow",
            "time": "5:30 - 7:15 (105s)",
            "visual": (
                "<b>Screen:</b> Login Card. Enter admin credentials: <i>admin@iem.edu.in</i> / <i>Admin@2026!</i>. Click 'Sign In as Staff / Admin'.<br/><br/>"
                "<b>Action:</b> Arrive at /admin. Highlight top 4 metric counters: Total, Pending, Accepted, Rejected.<br/><br/>"
                "<b>Action:</b> Point out Dual View toggle. Switch between 'Table View' and 'Card View' (NFR-03).<br/><br/>"
                "<b>Action:</b> Type 'Susnata' in live search bar &rarr; show table filtering in under 1 second.<br/><br/>"
                "<b>Action:</b> Click 'Review / Update Status' on Susnata Maiti's row. In status dropdown, select 'Under Review'. "
                "Enter remark: 'Academic credentials verified. Forwarded to CSE Departmental Board.' Click Update."
            ),
            "narration": (
                "\"We now authenticate using the pre-seeded administrator credentials: <i>admin@iem.edu.in</i>. "
                "The backend verifies our role claim and opens the <b>Administrator Workspace</b>.<br/><br/>"
                "At the top, dynamic metric counters aggregate application volumes in real time. To satisfy Non-Functional Requirement <b>NFR-03</b>, "
                "administrators can toggle smoothly between a <b>Compact Table View</b> for fast screening and a <b>Detailed Card View</b> for comprehensive candidate inspection.<br/><br/>"
                "Notice our live search filter: as I type 'Susnata', the applications table updates in under one second without page reloading.<br/><br/>"
                "Clicking 'Review' opens our candidate evaluation modal. Here, our <b>Finite-State Machine (Module 3)</b> regulates status transitions. "
                "An application in 'Submitted' state can transition to 'Under Review', or directly to 'Rejected'—provided explanatory remarks are supplied "
                "to prevent arbitrary rejections. Let us place this candidate <b>'Under Review'</b> with an official remark. "
                "The update is persisted immediately, and an immutable audit log entry is recorded with timestamp and reviewer identity per <b>FR-13</b>.\""
            )
        },
        {
            "num": 6,
            "title": "Scene 6: Executive Director Dashboard & CSV Export",
            "time": "7:15 - 8:15 (60s)",
            "visual": (
                "<b>Screen:</b> Log out of Admin. Enter Director credentials: <i>director@iem.edu.in</i> / <i>Director@2026!</i>. Click 'Sign In'.<br/><br/>"
                "<b>Action:</b> Show Director Dashboard (/director). Point out high-level KPI cards and that status update buttons are hidden/read-only.<br/><br/>"
                "<b>Action:</b> Click 'Export Full Applications List (CSV)'. Show browser downloading iem_applications_export.csv."
            ),
            "narration": (
                "\"Next, let us demonstrate executive governance by logging in as our Director, <b>Dr. Satyajit Chakrabarti</b>.<br/><br/>"
                "The <b>Director Dashboard (FR-20)</b> provides an executive overview of enrollment metrics. To enforce role separation, the Director view is strictly "
                "read-only: status mutation controls are hidden, eliminating the risk of accidental alterations during executive review.<br/><br/>"
                "To satisfy requirement <b>FR-12</b>, leadership can export the entire dataset with one click. As you see, the browser immediately downloads "
                "a formatted CSV file containing complete applicant bio-data, academic scores, and lifecycle statuses for offline reporting and university accreditation.\""
            )
        },
        {
            "num": 7,
            "title": "Scene 7: Architecture, Dual-Engine Persistence & Testing Rigor",
            "time": "8:15 - 9:15 (60s)",
            "visual": (
                "<b>Screen:</b> Switch to browser tab showing FastAPI Interactive OpenAPI Docs (/docs) or System Architecture Diagram.<br/><br/>"
                "<b>Action:</b> Scroll through REST endpoints (/api/auth, /api/student/application, /api/admin/metrics).<br/><br/>"
                "<b>Action:</b> Highlight Dual-Engine Database Abstraction (MongoDB Atlas Cloud + SQLite3 local failover) and 16/16 tests passing."
            ),
            "narration": (
                "\"Behind this user interface is a high-performance <b>FastAPI ASGI backend</b>, fully documented with interactive OpenAPI endpoints and typed Pydantic models.<br/><br/>"
                "Our primary engineering breakthrough is the <b>Dual-Engine Database Abstraction Layer</b>. In production, the system connects to MongoDB Atlas Cloud. "
                "However, within academic institutions, campus firewalls frequently block Windows DNS queries for SRV records. "
                "To prevent connection drops, our database layer automatically injects public DNS resolvers (8.8.8.8 and 1.1.1.1). "
                "Furthermore, if cloud latency exceeds 4000 milliseconds, the engine silently falls back to an embedded <b>SQLite3</b> database (<i>iem_admission.db</i>) with zero downtime.<br/><br/>"
                "Finally, our Test Lead, <b>Debadrita Dutta</b>, conducted McCabe's Cyclomatic Complexity basis path testing on our transition logic (<b>V(G)=10</b>), "
                "verifying all 10 independent paths across our automated test runner with a <b>100% pass rate</b> across both MongoDB and SQLite.\""
            )
        },
        {
            "num": 8,
            "title": "Scene 8: Conclusion & Acknowledgments",
            "time": "9:15 - 9:45 (30s)",
            "visual": (
                "<b>Screen:</b> Return to the GitHub repository tab in Chrome or the presentation cover slide.<br/><br/>"
                "<b>Action:</b> Display Team Nexus member details and live project links. Cursor rests on the live production URL."
            ),
            "narration": (
                "\"In conclusion, the <b>IEM Admission System</b> successfully fulfills all 20 Functional Requirements and 5 Non-Functional Requirements, "
                "delivered on schedule within our strict 20-day milestone plan.<br/><br/>"
                "On behalf of <b>Team Nexus</b>—Susnata Maiti, Sreejita Dey, Swapnil Ghosh, and Debadrita Dutta—we express our gratitude to <b>Prof. Sangeeta Sarkar</b>, "
                "<b>Prof. Saikat Dutta</b>, and our Director, <b>Dr. Satyajit Chakrabarti</b>, for their guidance.<br/><br/>"
                "Thank you very much for watching our demonstration!\""
            )
        }
    ]

    for sc in detailed_scenes:
        story.append(Paragraph(f"{sc['title']}  •  {sc['time']}", style_h2))

        table_data = [
            [Paragraph("Visual Cue & On-Screen Action", style_th), Paragraph("Spoken Narration (Voiceover Script)", style_th)],
            [Paragraph(sc["visual"], style_visual), Paragraph(sc["narration"], style_narration)]
        ]

        t_scene = Table(table_data, colWidths=[185, 302])
        t_scene.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), C_NAVY),
            ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
            ('BACKGROUND', (0, 1), (0, 1), C_ROW_BG),
            ('BACKGROUND', (1, 1), (1, 1), C_WHITE),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(t_scene)
        story.append(Spacer(1, 8))

    # Section 4: Demo Credentials
    story.append(Paragraph("4. Demo Accounts & Credentials Quick Reference", style_h1))
    creds_rows = [
        ["User Role", "Login Email Address", "Password", "Primary Workflow to Demonstrate"],
        ["New Student", "maitisusnata135531@gmail.com", "Student@2026!", "Self-registration, 4-step wizard, PDF marksheet upload (<5MB), form locking."],
        ["Existing Student", "priya.sharma@example.com", "Student@2026!", "Instant view of previously submitted application, immutable locking verification."],
        ["Administrator", "admin@iem.edu.in", "Admin@2026!", "Review applications queue, search/filter, Table/Card views, status transitions with remarks."],
        ["Executive Director", "director@iem.edu.in", "Director@2026!", "Bird's-eye metrics dashboard, read-only mode verification, one-click CSV export."]
    ]

    t_cr = []
    for r_idx, r_data in enumerate(creds_rows):
        row_cells = []
        for c_idx, val in enumerate(r_data):
            if r_idx == 0:
                p = Paragraph(val, style_th)
            elif c_idx == 0:
                p = Paragraph(f"<b>{val}</b>", style_td_bold)
            elif c_idx == 2:
                p = Paragraph(f"<b>{val}</b>", style_td_bold)
            else:
                p = Paragraph(val, style_td)
            row_cells.append(p)
        t_cr.append(row_cells)

    t_cr_table = Table(t_cr, colWidths=[95, 150, 80, 162])
    t_cr_table.setStyle(TableStyle([
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
    story.append(t_cr_table)
    story.append(Spacer(1, 12))

    # Section 5: Presenter Delivery Guidelines
    story.append(Paragraph("5. Presenter Delivery Guidelines", style_h1))
    tips_rows = [
        [Paragraph("<b>Speech Rate:</b>", style_meta_key), Paragraph("Maintain ~130 to 140 words per minute. Do not rush technical terms like PBKDF2 or McCabe Complexity.", style_meta_val)],
        [Paragraph("<b>Mouse Discipline:</b>", style_meta_key), Paragraph("Avoid erratic or circular motion. Rest cursor deliberately on the element being described.", style_meta_val)],
        [Paragraph("<b>Natural Pauses:</b>", style_meta_key), Paragraph("Allow 1-2 seconds of natural silence while views transition so the audience can see the DOM update.", style_meta_val)],
        [Paragraph("<b>Clean Desktop:</b>", style_meta_key), Paragraph("Silence Windows 11 notifications ('Do Not Disturb'). Hide bookmarks bar (Ctrl+Shift+B).", style_meta_val)]
    ]
    t_tips = Table(tips_rows, colWidths=[110, 377])
    t_tips.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#86efac")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#bbf7d0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_tips)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built at: {out_path}")

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_pdf = os.path.join(root_dir, "video_demonstration_script.pdf")
    build_pdf(target_pdf)
