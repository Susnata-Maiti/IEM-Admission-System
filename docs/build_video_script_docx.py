import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

FONT_FAMILY = "Google Sans"
FONT_FALLBACK = "Arial"

# Colors
COLOR_NAVY = RGBColor(30, 58, 138)       # #1E3A8A
COLOR_PRIMARY = RGBColor(37, 99, 235)    # #2563EB
COLOR_DARK = RGBColor(15, 23, 42)        # #0F172A
COLOR_MUTED = RGBColor(71, 85, 105)      # #475569
COLOR_GREEN = RGBColor(5, 150, 105)      # #059669
COLOR_AMBER = RGBColor(217, 119, 6)      # #D97706

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, border_color="CBD5E1"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:left w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def build_docx(out_path):
    doc = Document()

    # Page Setup: A4, 0.75-inch margins for spacious presentation tables
    sec = doc.sections[0]
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(0.75)
    sec.bottom_margin = Inches(0.75)
    sec.left_margin = Inches(0.75)
    sec.right_margin = Inches(0.75)

    # Header / Footer
    footer = sec.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f_run = f_p.add_run("IEM Admission System Software  •  Video Demonstration Script  •  Team Nexus (P4)")
    f_run.font.name = FONT_FAMILY
    f_run.font.size = Pt(8.5)
    f_run.font.color.rgb = COLOR_MUTED

    # Helpers
    def add_p(text="", size=Pt(10), bold=False, color=COLOR_DARK, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=Pt(0), space_after=Pt(4)):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = space_before
        p.paragraph_format.space_after = space_after
        if text:
            r = p.add_run(text)
            r.font.name = FONT_FAMILY
            r.font.size = size
            r.font.bold = bold
            r.font.color.rgb = color
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = FONT_FAMILY
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = COLOR_NAVY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = FONT_FAMILY
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY
        return p

    def add_callout(title, items, bg_hex="EFF6FF", border_color="93C5FD"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.77)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        set_cell_background(cell, bg_hex)

        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="8" w:space="0" w:color="{border_color}"/>
                <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{border_color}"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>
                <w:right w:val="single" w:sz="8" w:space="0" w:color="{border_color}"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(2)
        cp.paragraph_format.space_after = Pt(4)
        r_title = cp.add_run(title)
        r_title.font.name = FONT_FAMILY
        r_title.font.size = Pt(11)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_NAVY

        for prefix, body in items:
            p_item = cell.add_paragraph()
            p_item.paragraph_format.space_before = Pt(1)
            p_item.paragraph_format.space_after = Pt(3)
            r1 = p_item.add_run("• " + prefix + (" " if prefix else ""))
            r1.font.name = FONT_FAMILY
            r1.font.size = Pt(9.5)
            r1.font.bold = True
            r1.font.color.rgb = COLOR_DARK

            r2 = p_item.add_run(body)
            r2.font.name = FONT_FAMILY
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = COLOR_MUTED

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # DOCUMENT TITLE & METADATA HEADER
    # -------------------------------------------------------------
    add_p("PCCCS504 SOFTWARE ENGINEERING & PROJECT MANAGEMENT LAB  •  ACADEMIC YEAR 2026-27",
          size=Pt(9.5), bold=True, color=COLOR_PRIMARY, space_after=Pt(3))
    
    add_p("Video Demonstration Script: IEM Admission System Software",
          size=Pt(22), bold=True, color=COLOR_NAVY, space_after=Pt(4))
    
    add_p("Production-Ready Walkthrough Script from GitHub to Live Cloud Deployment",
          size=Pt(12), bold=False, color=COLOR_MUTED, space_after=Pt(10))

    # Metadata Card
    add_callout("Project & Video Metadata", [
        ("Target Duration:", "~9 Minutes 30 Seconds (Strictly <= 10 Minutes at ~135 words/minute)"),
        ("Initial Browser View:", "Google Chrome on Windows 11 with GitHub Repository tab open (Susnata-Maiti/IEM-Admission-System)"),
        ("Live Production URL:", "https://iem-admission-system-nexus-p4.vercel.app/ (Global CDN Edge + MongoDB Atlas Cloud)"),
        ("Interactive API Docs:", "https://iem-admission-system-nexus-p4.vercel.app/docs (FastAPI OpenAPI / Swagger UI)"),
        ("Team Number & Name:", "Team Number: P4  |  Team Name: Nexus  |  Batch: 2024-2028 (Section A, 5th Semester)"),
        ("Team Members & Roles:", "Susnata Maiti (A-11, Frontend Developer) | Sreejita Dey (A-29, Backend Developer) | Swapnil Ghosh (A-04, Database Lead) | Debadrita Dutta (A-12, Test Lead)"),
        ("Faculty Supervisors:", "Prof. Sangeeta Sarkar & Prof. Saikat Dutta"),
        ("Project Sponsor & Director:", "Dr. Satyajit Chakrabarti (Director, Institute of Engineering & Management, Kolkata)")
    ], bg_hex="EFF6FF", border_color="93C5FD")

    # -------------------------------------------------------------
    # SECTION 1: RECORDING SETUP CHECKLIST
    # -------------------------------------------------------------
    add_heading_1("1. Video Recording Setup & Environment Checklist")
    add_callout("Pre-Recording Checklist (Complete Before Starting Screen Capture)", [
        ("Screen Resolution:", "Windows 11 Desktop display set to 1920x1080 (1080p) or 16:9 widescreen with 100% or 125% scaling."),
        ("Chrome Browser Prep:", "Open Google Chrome maximized. Hide bookmarks bar (Ctrl+Shift+B). Close all unrelated personal tabs."),
        ("Tab 1 (Starting Tab):", "GitHub repo (https://github.com/Susnata-Maiti/IEM-Admission-System) scrolled to the top."),
        ("Tab 2 (Background Tab):", "FastAPI Swagger Docs (https://iem-admission-system-nexus-p4.vercel.app/docs) ready for Scene 7."),
        ("Sample Asset Prepared:", "Keep a valid sample marksheet PDF under 5MB (e.g., marksheet_sample.pdf, ~1.2MB) accessible on your Desktop."),
        ("Audio Configuration:", "Use a dedicated headset or USB microphone in a quiet room with noise cancellation enabled."),
        ("Pacing Target:", "Maintain a measured, confident speaking rate of ~130 to 140 words per minute. Pause 1-2 seconds after clicking buttons to let views settle.")
    ], bg_hex="F8FAFC", border_color="CBD5E1")

    # -------------------------------------------------------------
    # SECTION 2: TIMING & SCENE SUMMARY TABLE
    # -------------------------------------------------------------
    add_heading_1("2. Timing & Scene Overview Table")
    add_p("The demonstration is structured into 8 modular scenes totaling exactly 9 minutes and 45 seconds, ensuring strict compliance with the 10-minute maximum ceiling:")

    scenes_data = [
        ("0:00 - 0:45", "Scene 1: Introduction & Launch", "GitHub Repository README.md in Chrome", "Team introductions, PCCCS504 context, 20-day timeline, clicking live deployment link."),
        ("0:45 - 2:00", "Scene 2: Landing & Registration", "Live Web Portal (/) Onboarding Card", "Official IEM crest, Google Sans font, @gmail.com validation guard, salted PBKDF2 password hashing."),
        ("2:00 - 4:15", "Scene 3: 4-Step Application Wizard", "Application Stepper (/application)", "Personal details, academic scores, B.Tech CSE choice, PDF upload (<5MB limit), immutable submission lock."),
        ("4:15 - 5:30", "Scene 4: Student Dashboard", "Student Dashboard (/dashboard)", "Application ID (IEM-2026-XXXX), tracking timeline, marksheet download preview, edit-lock verification."),
        ("5:30 - 7:15", "Scene 5: Administrator Workspace", "Admin Console (/admin)", "Real-time KPI metrics, instant <1s search filter, Table/Card dual views, state machine update with mandatory remarks."),
        ("7:15 - 8:15", "Scene 6: Director Executive View", "Director Dashboard (/director)", "Executive bird's-eye metrics, read-only mode verification, one-click full CSV report export."),
        ("8:15 - 9:15", "Scene 7: Architecture & Testing", "Swagger Docs (/docs) / Architecture", "FastAPI ASGI engine, Dual-Engine DB abstraction (MongoDB Atlas + SQLite3 fallback), 100% McCabe Basis Path tests."),
        ("9:15 - 9:45", "Scene 8: Conclusion & Sign-Off", "GitHub Repository / Presentation Slide", "Summary of completed deliverables, faculty acknowledgments, and closing thanks.")
    ]

    t_summary = doc.add_table(rows=len(scenes_data) + 1, cols=4)
    t_summary.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_summary)

    headers = ["Timestamp", "Scene / Section", "Primary Visual Focus", "Topics Covered"]
    col_w = [Inches(1.0), Inches(1.8), Inches(1.8), Inches(2.17)]

    # Format header
    for j, h in enumerate(headers):
        cell = t_summary.cell(0, j)
        cell.width = col_w[j]
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        set_cell_background(cell, "1E3A8A")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = FONT_FAMILY
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    # Format rows
    for i, row in enumerate(scenes_data):
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            cell = t_summary.cell(i + 1, j)
            cell.width = col_w[j]
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = FONT_FAMILY
            r.font.size = Pt(9.0)
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            elif j == 1:
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK
            else:
                r.font.color.rgb = COLOR_MUTED

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(8)
    p_sp.paragraph_format.space_after = Pt(2)

    # -------------------------------------------------------------
    # SECTION 3: STEP-BY-STEP TWO-COLUMN PRODUCTION SCRIPT
    # -------------------------------------------------------------
    add_heading_1("3. Detailed Two-Column Production Script (Visual Cues & Spoken Narration)")
    add_p("Each scene provides exact synchronised instructions: what the presenter demonstrates on screen (left column) and the word-for-word voiceover narration to read (right column):")

    script_scenes = [
        {
            "num": 1,
            "title": "Scene 1: Introduction & Launch from GitHub",
            "time": "0:00 - 0:45 (Duration: 45s)",
            "visual": (
                "Screen: Chrome browser showing GitHub repository Susnata-Maiti/IEM-Admission-System.\n\n"
                "Action: Cursor hovers over repository title and team header in README.md.\n\n"
                "Scroll smoothly down to Section '🌐 Live Production Deployment'.\n\n"
                "Action: Hover mouse cursor over the live Vercel URL and click 'https://iem-admission-system-nexus-p4.vercel.app/' to open in the active tab."
            ),
            "narration": (
                "\"Hello everyone. Welcome to the technical demonstration of the IEM Admission System Software, "
                "engineered for the Software Engineering and Project Management Lab (PCCCS504) at the Institute of Engineering & Management, Kolkata.\n\n"
                "I am Susnata Maiti, Frontend Developer for Team Nexus (P4). I am presenting on behalf of our team comprising "
                "Sreejita Dey as Backend Developer, Swapnil Ghosh as Database Lead, and Debadrita Dutta as Test Lead, "
                "under the guidance of our faculty in-charge Prof. Sangeeta Sarkar, Prof. Saikat Dutta, and our Project Sponsor and Director, Dr. Satyajit Chakrabarti.\n\n"
                "Our objective was to deliver a resilient, user-focused college admission platform within an accelerated 20-day timeline. "
                "As documented in our repository README, the application is deployed live on Vercel with a global CDN edge, backed by MongoDB Atlas Cloud. "
                "Let us click our live production link and walk through the complete admission lifecycle in real time.\""
            )
        },
        {
            "num": 2,
            "title": "Scene 2: Landing Page, Design Standards & Student Registration",
            "time": "0:45 - 2:00 (Duration: 75s)",
            "visual": (
                "Screen: Browser opens https://iem-admission-system-nexus-p4.vercel.app/.\n\n"
                "Action: Point out the official IEM laurel wreath crest and clean Google Sans font. Toggle to 'Register' tab.\n\n"
                "Action: In Name, type 'Susnata Maiti'. In Email, enter an invalid address 'susnata@yahoo.com' and click Register to demonstrate inline @gmail.com domain error toast.\n\n"
                "Action: Correct email to 'maitisusnata135531@gmail.com'. In Password, type 'Student@2026!'. Click 'Create Account / Register'. Show success toast and automatic login."
            ),
            "narration": (
                "\"Here on our live production portal, the user interface adheres strictly to our SRS design specifications: "
                "featuring the official IEM laurel wreath crest, responsive container layouts, and clean typography rendered in Google Sans.\n\n"
                "The system implements strict Role-Based Access Control separating Student Applicants, Admissions Administrators, and the Executive Director. "
                "Let us begin by registering a new student applicant.\n\n"
                "Notice our client-side validation guard: if I input a non-Gmail address, the portal immediately rejects it because student registrations "
                "are restricted strictly to @gmail.com addresses. Once I provide my valid email—maitisusnata135531@gmail.com—and enter a password satisfying "
                "our complexity policy (minimum 8 characters with uppercase and special symbols), the client sends an asynchronous REST call to our FastAPI backend.\n\n"
                "On the server side, passwords are never stored in plaintext—they are securely hashed using salted PBKDF2-HMAC-SHA256. "
                "The backend issues a signed JWT token, logging us in seamlessly.\""
            )
        },
        {
            "num": 3,
            "title": "Scene 3: The 4-Step Application Wizard & PDF Upload",
            "time": "2:00 - 4:15 (Duration: 135s)",
            "visual": (
                "Screen: Application Wizard (/application).\n\n"
                "Action 1 (Step 1): Point out 4-step progress stepper. Fill DOB: 15/08/2005, Phone: +91 98765 43210, Address: Salt Lake Sector V, Kolkata. Click Next.\n\n"
                "Action 2 (Step 2): Enter Class 10 marks (92.5%, CBSE), Class 12 marks (90.0%, WBCHSE), Passing Year (2024). Select Course: 'B.Tech Computer Science & Engineering'. Click Next.\n\n"
                "Action 3 (Step 3): Drag and drop sample PDF marksheet (~1.2MB). Show file preview card with size verification. Click Next.\n\n"
                "Action 4 (Step 4): Review consolidated summary. Point out the Business Rule BR-02 immutability warning. Click 'Confirm & Final Submit'."
            ),
            "narration": (
                "\"We are now guided into the 4-Step Application Wizard. The top visual stepper anchors candidate progress, minimizing cognitive fatigue.\n\n"
                "In Step 1, personal details are sanitized and checked for mandatory fields before enabling navigation to Step 2.\n\n"
                "In Step 2, the candidate inputs academic scores and selects their target degree from a predefined list. "
                "Per Business Rule BR-04, percentages must fall strictly between 0.0% and 100.0%, enforced via Pydantic schema validation.\n\n"
                "Step 3 implements Module 1: Document Upload. In compliance with requirement FR-05, uploads are restricted strictly to PDF format "
                "with an enforced 5 megabyte ceiling. Both client-side JavaScript and the FastAPI multipart stream validator inspect MIME headers "
                "to protect against malicious file uploads. The file is stored safely and linked to our record.\n\n"
                "In Step 4, the student reviews their full application. Notice the explicit notice for Business Rule BR-02: once submitted, "
                "all personal, academic, and document fields become permanently immutable to protect admission integrity. Let us click 'Confirm and Final Submit'.\""
            )
        },
        {
            "num": 4,
            "title": "Scene 4: Student Dashboard & Real-Time Tracking Timeline",
            "time": "4:15 - 5:30 (Duration: 75s)",
            "visual": (
                "Screen: Student Dashboard (/dashboard).\n\n"
                "Action: Highlight the generated Application ID (e.g., IEM-2026-0847) and green status badge: 'SUBMITTED'.\n\n"
                "Action: Point out chronological progress timeline: Application Submitted (Completed) -> Under Review (Pending) -> Final Decision (Pending).\n\n"
                "Action: Click 'View / Download Uploaded Marksheet' button to preview the PDF in a new browser tab.\n\n"
                "Action: Click 'Sign Out' in top navbar to return to login page."
            ),
            "narration": (
                "\"The portal redirects immediately to the Student Dashboard, satisfying requirements FR-10 and FR-11. "
                "Notice our assigned application identifier—IEM-2026-0847—and the active status badge marked 'Submitted'.\n\n"
                "Below the summary card is our chronological tracking timeline. The candidate can clearly track their progress through document triage "
                "and departmental review. Candidates can also preview or download their uploaded PDF marksheets anytime to verify their records. "
                "Per requirement FR-09, editing controls have been completely removed—the record is securely locked against further edits.\n\n"
                "Now, let us log out of the student session and log in as an Admissions Administrator to process this application.\""
            )
        },
        {
            "num": 5,
            "title": "Scene 5: Administrator Workspace & Finite-State Machine Triage",
            "time": "5:30 - 7:15 (Duration: 105s)",
            "visual": (
                "Screen: Login Card. Enter admin credentials: admin@iem.edu.in / Admin@2026!. Click 'Sign In as Staff / Admin'.\n\n"
                "Action: Arrive at /admin. Highlight the top 4 metric counters: Total, Pending, Accepted, Rejected.\n\n"
                "Action: Point out Dual View toggle. Switch between 'Table View' and 'Card View' (NFR-03).\n\n"
                "Action: Type 'Susnata' in the live search bar -> show the table filtering in under 1 second.\n\n"
                "Action: Click 'Review / Update Status' on Susnata Maiti's row. In status dropdown, select 'Under Review'. "
                "Enter remark: 'Academic credentials verified. Forwarded to CSE Departmental Board.' Click Update."
            ),
            "narration": (
                "\"We now authenticate using the pre-seeded administrator credentials: admin@iem.edu.in. "
                "The backend verifies our role claim and opens the Administrator Workspace.\n\n"
                "At the top, dynamic metric counters aggregate application volumes in real time. To satisfy Non-Functional Requirement NFR-03, "
                "administrators can toggle smoothly between a Compact Table View for fast screening and a Detailed Card View for comprehensive candidate inspection.\n\n"
                "Notice our live search filter: as I type 'Susnata', the applications table updates in under one second without page reloading.\n\n"
                "Clicking 'Review' opens our candidate evaluation modal. Here, our Finite-State Machine (Module 3) regulates status transitions. "
                "An application in 'Submitted' state can transition to 'Under Review', or directly to 'Rejected'—provided explanatory remarks are supplied "
                "to prevent arbitrary rejections. Let us place this candidate 'Under Review' with an official remark. "
                "The update is persisted immediately, and an immutable audit log entry is recorded with timestamp and reviewer identity per FR-13.\""
            )
        },
        {
            "num": 6,
            "title": "Scene 6: Executive Director Dashboard & CSV Export",
            "time": "7:15 - 8:15 (Duration: 60s)",
            "visual": (
                "Screen: Log out of Admin. Enter Director credentials: director@iem.edu.in / Director@2026!. Click 'Sign In'.\n\n"
                "Action: Show Director Dashboard (/director). Point out high-level KPI cards and that status update buttons are hidden/read-only.\n\n"
                "Action: Click 'Export Full Applications List (CSV)'. Show browser downloading iem_applications_export.csv."
            ),
            "narration": (
                "\"Next, let us demonstrate executive governance by logging in as our Director, Dr. Satyajit Chakrabarti.\n\n"
                "The Director Dashboard (FR-20) provides an executive overview of enrollment metrics. To enforce role separation, the Director view is strictly "
                "read-only: status mutation controls are hidden, eliminating the risk of accidental alterations during executive review.\n\n"
                "To satisfy requirement FR-12, leadership can export the entire dataset with one click. As you see, the browser immediately downloads "
                "a formatted CSV file containing complete applicant bio-data, academic scores, and lifecycle statuses for offline reporting and university accreditation.\""
            )
        },
        {
            "num": 7,
            "title": "Scene 7: Architecture, Dual-Engine Persistence & Testing Rigor",
            "time": "8:15 - 9:15 (Duration: 60s)",
            "visual": (
                "Screen: Switch to browser tab showing FastAPI Interactive OpenAPI Docs (/docs) or System Architecture Diagram.\n\n"
                "Action: Scroll through REST endpoints (/api/auth, /api/student/application, /api/admin/metrics).\n\n"
                "Action: Highlight the Dual-Engine Database Abstraction (MongoDB Atlas Cloud + SQLite3 local failover) and 16/16 tests passing."
            ),
            "narration": (
                "\"Behind this user interface is a high-performance FastAPI ASGI backend, fully documented with interactive OpenAPI endpoints and typed Pydantic models.\n\n"
                "Our primary engineering breakthrough is the Dual-Engine Database Abstraction Layer. In production, the system connects to MongoDB Atlas Cloud. "
                "However, within academic institutions, campus firewalls frequently block Windows DNS queries for SRV records. "
                "To prevent connection drops, our database layer automatically injects public DNS resolvers (8.8.8.8 and 1.1.1.1). "
                "Furthermore, if cloud latency exceeds 4000 milliseconds, the engine silently falls back to an embedded SQLite3 database (iem_admission.db) with zero downtime.\n\n"
                "Finally, our Test Lead, Debadrita Dutta, conducted McCabe's Cyclomatic Complexity basis path testing on our transition logic (V(G)=10), "
                "verifying all 10 independent paths across our automated test runner with a 100% pass rate across both MongoDB and SQLite.\""
            )
        },
        {
            "num": 8,
            "title": "Scene 8: Conclusion & Acknowledgments",
            "time": "9:15 - 9:45 (Duration: 30s)",
            "visual": (
                "Screen: Return to the GitHub repository tab in Chrome or the presentation cover slide.\n\n"
                "Action: Display Team Nexus member details and live project links. Cursor rests on the live production URL."
            ),
            "narration": (
                "\"In conclusion, the IEM Admission System successfully fulfills all 20 Functional Requirements and 5 Non-Functional Requirements, "
                "delivered on schedule within our strict 20-day milestone plan.\n\n"
                "On behalf of Team Nexus—Susnata Maiti, Sreejita Dey, Swapnil Ghosh, and Debadrita Dutta—we express our gratitude to Prof. Sangeeta Sarkar, "
                "Prof. Saikat Dutta, and our Director, Dr. Satyajit Chakrabarti, for their guidance.\n\n"
                "Thank you very much for watching our demonstration!\""
            )
        }
    ]

    for sc in script_scenes:
        add_heading_2(f"{sc['title']}  •  {sc['time']}")
        
        tbl = doc.add_table(rows=2, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl)

        # Header
        col_widths = [Inches(2.55), Inches(4.22)]
        for j, h_txt in enumerate(["Visual Cue & On-Screen Action", "Spoken Narration (Voiceover Script)"]):
            c = tbl.cell(0, j)
            c.width = col_widths[j]
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            set_cell_background(c, "1E3A8A")
            cp = c.paragraphs[0]
            cr = cp.add_run(h_txt)
            cr.font.name = FONT_FAMILY
            cr.font.size = Pt(9.5)
            cr.font.bold = True
            cr.font.color.rgb = RGBColor(255, 255, 255)

        # Body Row
        cell_l = tbl.cell(1, 0)
        cell_l.width = col_widths[0]
        set_cell_margins(cell_l, top=80, bottom=80, left=100, right=100)
        set_cell_background(cell_l, "F8FAFC")
        
        # Split visual cues by paragraph
        p_vis = cell_l.paragraphs[0]
        v_lines = sc["visual"].split("\n\n")
        for idx, line in enumerate(v_lines):
            if idx > 0:
                p_vis = cell_l.add_paragraph()
            p_vis.paragraph_format.space_before = Pt(1)
            p_vis.paragraph_format.space_after = Pt(4)
            r_v = p_vis.add_run(line)
            r_v.font.name = FONT_FAMILY
            r_v.font.size = Pt(9.0)
            r_v.font.color.rgb = COLOR_DARK
            if "Screen:" in line or "Action:" in line:
                r_v.font.bold = True

        cell_r = tbl.cell(1, 1)
        cell_r.width = col_widths[1]
        set_cell_margins(cell_r, top=80, bottom=80, left=100, right=100)
        set_cell_background(cell_r, "FFFFFF")
        
        # Split spoken narration by paragraph
        p_nar = cell_r.paragraphs[0]
        n_lines = sc["narration"].split("\n\n")
        for idx, line in enumerate(n_lines):
            if idx > 0:
                p_nar = cell_r.add_paragraph()
            p_nar.paragraph_format.space_before = Pt(2)
            p_nar.paragraph_format.space_after = Pt(5)
            r_n = p_nar.add_run(line)
            r_n.font.name = FONT_FAMILY
            r_n.font.size = Pt(9.5)
            r_n.font.color.rgb = COLOR_DARK
            r_n.font.italic = True

        p_gap = doc.add_paragraph()
        p_gap.paragraph_format.space_before = Pt(4)
        p_gap.paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # SECTION 4: DEMO ACCOUNTS QUICK REFERENCE
    # -------------------------------------------------------------
    add_heading_1("4. Demo Accounts & Credentials Quick Reference")
    add_p("Pre-configured accounts for recording the video demonstration:")

    creds_data = [
        ("New Student", "maitisusnata135531@gmail.com (or any @gmail.com)", "Student@2026!", "Self-registration, 4-step wizard form, PDF marksheet upload (<5MB), immutable submission, and live status tracking."),
        ("Existing Student", "priya.sharma@example.com", "Student@2026!", "Instant view of previously submitted B.Tech application, immutable locking verification, marksheet preview."),
        ("Administrator", "admin@iem.edu.in", "Admin@2026!", "Review applications queue, instant search & multi-parameter filter, Table/Card dual views, state machine update with mandatory remarks."),
        ("Executive Director", "director@iem.edu.in", "Director@2026!", "Bird's-eye metrics dashboard, read-only security mode verification, and one-click full CSV report export.")
    ]

    t_creds = doc.add_table(rows=len(creds_data) + 1, cols=4)
    t_creds.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_creds)

    c_headers = ["User Role", "Login Email Address", "Password", "Primary Workflow to Demonstrate"]
    c_widths = [Inches(1.2), Inches(2.2), Inches(1.1), Inches(2.27)]

    for j, h in enumerate(c_headers):
        cell = t_creds.cell(0, j)
        cell.width = c_widths[j]
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        set_cell_background(cell, "1E3A8A")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = FONT_FAMILY
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(creds_data):
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            cell = t_creds.cell(i + 1, j)
            cell.width = c_widths[j]
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = FONT_FAMILY
            r.font.size = Pt(9.0)
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            elif j == 2:
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK
            else:
                r.font.color.rgb = COLOR_MUTED

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(8)
    p_sp2.paragraph_format.space_after = Pt(2)

    # -------------------------------------------------------------
    # SECTION 5: PRESENTER DELIVERY TIPS
    # -------------------------------------------------------------
    add_heading_1("5. Presenter Delivery & Video Recording Tips")
    add_callout("Guidelines for Professional Presentation & Audio Delivery", [
        ("Speech Modulation:", "Speak with clear diction and confidence. Aim for 130 to 140 words per minute. Avoid rushing through technical terms like PBKDF2 or McCabe Complexity."),
        ("Intentional Mouse Movement:", "Avoid circular or erratic cursor motion. Place the cursor deliberately on the element being described (e.g. the IEM crest, the @gmail.com input, or the Table/Card toggle), then let it rest."),
        ("Natural Transitions:", "Allow 1 to 2 seconds of natural silence when transitions occur (such as logging in or submitting forms) so the video viewer sees the UI settle smoothly."),
        ("Clean Desktop:", "Ensure Windows notification banners are silenced ('Do Not Disturb' mode on Windows 11). Keep only Chrome open."),
        ("Post-Recording Quality Check:", "Verify that the audio track is synchronized with your clicks and that all text on the 1080p recording is crisp and readable.")
    ], bg_hex="F0FDF4", border_color="86EFAC")

    doc.save(out_path)
    print(f"Video demonstration script successfully created at: {out_path}")

if __name__ == "__main__":
    docs_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(docs_dir)
    build_docx(os.path.join(docs_dir, "video_demonstration_script.docx"))
    build_docx(os.path.join(root_dir, "video_demonstration_script.docx"))
