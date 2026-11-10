import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

FONT_NAME = "Google Sans"

# Background Canvas
C_BG_SLIDE = RGBColor(248, 250, 252)        # Slate 50

# Text Colors
C_DARK = RGBColor(15, 23, 42)              # Slate 900 (High contrast)
C_MUTED = RGBColor(51, 65, 85)             # Slate 700 (Readable, dark enough for light shades)
C_PRIMARY_DARK = RGBColor(30, 58, 138)     # Blue 900
C_PRIMARY = RGBColor(37, 99, 235)          # Blue 600
C_SUCCESS_DARK = RGBColor(6, 95, 70)       # Green 900
C_WARNING_DARK = RGBColor(146, 64, 14)     # Amber 900
C_PURPLE_DARK = RGBColor(107, 33, 168)     # Purple 900

# Light Shaded Container Backgrounds (Soft, elegant pastels)
C_SHADE_SLATE = RGBColor(241, 245, 249)    # Slate 100
C_SHADE_BLUE = RGBColor(239, 246, 255)     # Blue 50
C_SHADE_GREEN = RGBColor(240, 253, 244)    # Emerald 50
C_SHADE_AMBER = RGBColor(254, 252, 232)    # Amber 50
C_SHADE_PURPLE = RGBColor(250, 245, 255)   # Purple 50
C_SHADE_INDIGO = RGBColor(238, 242, 255)   # Indigo 50

# Container Borders
C_BORDER_SLATE = RGBColor(203, 213, 225)   # Slate 300
C_BORDER_BLUE = RGBColor(147, 197, 253)    # Blue 300
C_BORDER_GREEN = RGBColor(134, 239, 172)   # Green 300
C_BORDER_AMBER = RGBColor(253, 230, 138)   # Amber 300
C_BORDER_PURPLE = RGBColor(216, 180, 254)  # Purple 300
C_BORDER_INDIGO = RGBColor(165, 180, 252)  # Indigo 300

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = C_BG_SLIDE

def add_header(slide, title_text, category_text, slide_num):
    # Category Tag
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.32), Inches(11.733), Inches(0.28))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = category_text.upper()
    p.font.name = FONT_NAME
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    # Main Slide Title (Increased size)
    tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.62), Inches(11.733), Inches(0.60))
    tf_t = tx_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    pt = tf_t.paragraphs[0]
    pt.text = title_text
    pt.font.name = FONT_NAME
    pt.font.size = Pt(23)
    pt.font.bold = True
    pt.font.color.rgb = C_DARK

    # Footer Left
    tx_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(9.5), Inches(0.3))
    tf_f = tx_foot.text_frame
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    pf = tf_f.paragraphs[0]
    pf.text = "IEM Admission System  •  Team Nexus (P4)  •  PCCCS504 Software Engineering & Project Management Lab"
    pf.font.name = FONT_NAME
    pf.font.size = Pt(9.2)
    pf.font.color.rgb = C_MUTED

    # Footer Page Number
    tx_num = slide.shapes.add_textbox(Inches(10.5), Inches(7.05), Inches(2.033), Inches(0.3))
    tf_n = tx_num.text_frame
    tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
    pn = tf_n.paragraphs[0]
    pn.alignment = PP_ALIGN.RIGHT
    pn.text = f"Slide {slide_num} of 10"
    pn.font.name = FONT_NAME
    pn.font.size = Pt(9.2)
    pn.font.bold = True
    pn.font.color.rgb = C_MUTED

def add_container(slide, x, y, w, h, bg_color=C_SHADE_SLATE, border_color=C_BORDER_SLATE, line_width=Pt(1.3)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = line_width
    return shape

def add_container_content(shape, title, items, title_color=C_DARK, item_size=Pt(10.0), prefix_size=Pt(10.5), title_size=Pt(13.2)):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.14)
    tf.margin_bottom = Inches(0.12)
    
    # Title Paragraph
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_NAME
    p.font.size = title_size
    p.font.bold = True
    p.font.color.rgb = title_color
    p.space_after = Pt(6)

    # Content Items (Increased font size)
    for prefix, body in items:
        pi = tf.add_paragraph()
        pi.space_after = Pt(4)
        if prefix:
            r1 = pi.add_run()
            r1.text = prefix + (" " if not prefix.endswith(" ") else "")
            r1.font.name = FONT_NAME
            r1.font.size = prefix_size
            r1.font.bold = True
            r1.font.color.rgb = C_DARK
        
        r2 = pi.add_run()
        r2.text = body
        r2.font.name = FONT_NAME
        r2.font.size = item_size
        r2.font.bold = False
        r2.font.color.rgb = C_MUTED

def build_presentation(out_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title & Team Nexus (Cover)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Hero Banner (Light Blue Shaded Container)
    hero = add_container(s1, Inches(0.8), Inches(0.52), Inches(11.733), Inches(2.20),
                         bg_color=C_SHADE_BLUE, border_color=C_BORDER_BLUE)
    htf = hero.text_frame
    htf.word_wrap = True
    htf.margin_left = Inches(0.30)
    htf.margin_top = Inches(0.18)
    
    hp0 = htf.paragraphs[0]
    hp0.text = "PCCCS504 SOFTWARE ENGINEERING & PROJECT MANAGEMENT LAB  •  ACADEMIC YEAR 2026-27"
    hp0.font.name = FONT_NAME
    hp0.font.size = Pt(10.5)
    hp0.font.bold = True
    hp0.font.color.rgb = C_PRIMARY
    hp0.space_after = Pt(4)

    hp1 = htf.add_paragraph()
    hp1.text = "IEM Admission System Software"
    hp1.font.name = FONT_NAME
    hp1.font.size = Pt(28)
    hp1.font.bold = True
    hp1.font.color.rgb = C_PRIMARY_DARK
    hp1.space_after = Pt(4)

    hp2 = htf.add_paragraph()
    hp2.text = "A Resilient, Dual-Engine College Admissions & Verification Platform"
    hp2.font.name = FONT_NAME
    hp2.font.size = Pt(13)
    hp2.font.color.rgb = C_MUTED
    hp2.space_after = Pt(6)

    hp3 = htf.add_paragraph()
    hp3.text = "Team Number: P4   |   Team Name: Nexus   |   Batch: 2024-2028 (Section A, 5th Sem)   |   Institute of Engineering & Management, Kolkata"
    hp3.font.name = FONT_NAME
    hp3.font.size = Pt(9.8)
    hp3.font.bold = True
    hp3.font.color.rgb = C_DARK

    # 4 Team Members Cards (Light Shaded Containers)
    members = [
        {
            "name": "Susnata Maiti",
            "roll": "Roll: A-11 • CSE",
            "role": "Role: Frontend Developer",
            "email": "maitisusnata135531@gmail.com",
            "bg": C_SHADE_BLUE,
            "border": C_BORDER_BLUE,
            "color": C_PRIMARY,
            "tasks": [
                ("Responsibilities:", "UI/UX design, client-side validation, 4-step wizard form, and REST API integration."),
                ("Deliverables:", "Responsive SPA, error toasts, and student dashboard.")
            ]
        },
        {
            "name": "Sreejita Dey",
            "roll": "Roll: A-29 • CSE",
            "role": "Role: Backend Developer",
            "email": "sreejitad05@gmail.com",
            "bg": C_SHADE_GREEN,
            "border": C_BORDER_GREEN,
            "color": C_SUCCESS_DARK,
            "tasks": [
                ("Responsibilities:", "FastAPI ASGI API, PBKDF2 hashing, JWT tokens, and finite-state machine."),
                ("Deliverables:", "Async API routes, RBAC security, transition validation logic.")
            ]
        },
        {
            "name": "Swapnil Ghosh",
            "roll": "Roll: A-04 • CSE",
            "role": "Role: Database Lead",
            "email": "swapnilghosh2005@gmail.com",
            "bg": C_SHADE_AMBER,
            "border": C_BORDER_AMBER,
            "color": C_WARNING_DARK,
            "tasks": [
                ("Responsibilities:", "Dual-engine database layer, MongoDB Atlas, SQLite3 offline failover."),
                ("Deliverables:", "SRV DNS auto-recovery, schema design, document storage.")
            ]
        },
        {
            "name": "Debadrita Dutta",
            "roll": "Roll: A-12 • CSE",
            "role": "Role: Test Lead",
            "email": "debadritadutta831@gmail.com",
            "bg": C_SHADE_PURPLE,
            "border": C_BORDER_PURPLE,
            "color": C_PURPLE_DARK,
            "tasks": [
                ("Responsibilities:", "Software test strategy & plan, McCabe basis path testing, BVA/ECP design."),
                ("Deliverables:", "16 automated test fixtures, 100% path coverage, defect log.")
            ]
        }
    ]

    card_w = Inches(2.78)
    card_h = Inches(3.70)
    gap = Inches(0.20)
    top_pos = Inches(2.95)

    for i, m in enumerate(members):
        left_pos = Inches(0.8) + i * (card_w + gap)
        c_box = add_container(s1, left_pos, top_pos, card_w, card_h, bg_color=m["bg"], border_color=m["border"])
        ctf = c_box.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.16)
        ctf.margin_right = Inches(0.16)
        ctf.margin_top = Inches(0.16)
        ctf.margin_bottom = Inches(0.12)

        # Name
        p0 = ctf.paragraphs[0]
        p0.text = m["name"]
        p0.font.name = FONT_NAME
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = C_DARK

        # Roll
        p_roll = ctf.add_paragraph()
        p_roll.text = m["roll"]
        p_roll.font.name = FONT_NAME
        p_roll.font.size = Pt(9.5)
        p_roll.font.color.rgb = C_MUTED
        p_roll.space_after = Pt(2)

        # Role
        p1 = ctf.add_paragraph()
        p1.text = m["role"]
        p1.font.name = FONT_NAME
        p1.font.size = Pt(11.2)
        p1.font.bold = True
        p1.font.color.rgb = m["color"]
        p1.space_after = Pt(3)

        # Email
        p2 = ctf.add_paragraph()
        p2.text = m["email"]
        p2.font.name = FONT_NAME
        p2.font.size = Pt(9.2)
        p2.font.bold = True
        p2.font.color.rgb = C_PRIMARY
        p2.space_after = Pt(8)

        # Tasks
        for prefix, text in m["tasks"]:
            pt = ctf.add_paragraph()
            pt.space_after = Pt(4)
            r1 = pt.add_run()
            r1.text = prefix + " "
            r1.font.name = FONT_NAME
            r1.font.size = Pt(9.2)
            r1.font.bold = True
            r1.font.color.rgb = C_DARK

            r2 = pt.add_run()
            r2.text = text
            r2.font.name = FONT_NAME
            r2.font.size = Pt(9.0)
            r2.font.color.rgb = C_MUTED

    # Footer Acknowledgments (Light Shaded Slate)
    foot = add_container(s1, Inches(0.8), Inches(6.80), Inches(11.733), Inches(0.38),
                         bg_color=C_SHADE_SLATE, border_color=C_BORDER_SLATE)
    ftf = foot.text_frame
    ftf.word_wrap = True
    ftf.margin_left = Inches(0.2)
    ftf.margin_top = Inches(0.06)
    p_ft = ftf.paragraphs[0]
    p_ft.text = "Faculty In-Charge: Prof. Sangeeta Sarkar & Prof. Saikat Dutta   |   Project Sponsor & Director: Dr. Satyajit Chakrabarti"
    p_ft.font.name = FONT_NAME
    p_ft.font.size = Pt(9.2)
    p_ft.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 2: Project Charter & Problem Statement
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement & Project Charter Overview", "Project Context & Scope", 2)

    p_box1 = add_container(s2, Inches(0.8), Inches(1.45), Inches(5.7), Inches(2.60),
                           bg_color=C_SHADE_SLATE, border_color=C_BORDER_SLATE)
    add_container_content(p_box1, "The Problem & Operational Challenges", [
        ("Legacy Bottlenecks:", "Paper forms and unvalidated portals cause application loss and processing delays."),
        ("Network Fragility:", "Campus network drops and DNS filters disrupt cloud database connections during rush periods."),
        ("Validation Vulnerabilities:", "Unchecked file formats and oversized files crash application handlers and consume storage."),
        ("Core Mission:", "Deliver a unified admissions platform with zero downtime and immutable data governance.")
    ], title_color=C_PRIMARY_DARK)

    p_box2 = add_container(s2, Inches(0.8), Inches(4.25), Inches(5.7), Inches(2.60),
                           bg_color=C_SHADE_BLUE, border_color=C_BORDER_BLUE)
    add_container_content(p_box2, "Project Charter Constraints & Governance", [
        ("Strict 20-Day Timeline:", "Accelerated development lifecycle from charter approval to full cloud deployment."),
        ("Target Client Environment:", "Exclusively optimized for Windows 11 Desktop on Google Chrome and Microsoft Edge."),
        ("Fixed Technology Stack:", "Next.js / Vanilla JS Frontend, FastAPI Python ASGI backend, and Dual DB layer."),
        ("Autonomous Governance:", "Separation of duties across Frontend, Backend, Database, and Testing teams.")
    ], title_color=C_PRIMARY)

    p_box3 = add_container(s2, Inches(6.83), Inches(1.45), Inches(5.70), Inches(5.40),
                           bg_color=C_SHADE_AMBER, border_color=C_BORDER_AMBER)
    tf3 = p_box3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = Inches(0.22)
    tf3.margin_top = Inches(0.18)
    p_title = tf3.paragraphs[0]
    p_title.text = "6-Stage Admission Workflow Lifecycle"
    p_title.font.name = FONT_NAME
    p_title.font.size = Pt(13.2)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WARNING_DARK
    p_title.space_after = Pt(8)

    steps = [
        ("1. Account Registration", "Applicant enters name, email (@gmail.com enforced), and password; salted PBKDF2 hash."),
        ("2. 4-Step Form Wizard", "Student inputs personal details, academic scores (Class 10/12), and course selection."),
        ("3. PDF Marksheet Upload", "FastAPI validates PDF MIME type and enforces strict <5MB size ceiling before saving."),
        ("4. Immutable Final Submit", "Application state locks permanently into 'Submitted' state; timestamp and audit log stored."),
        ("5. Admin Triage & Review", "Admission officers inspect credentials, preview marksheets, and update status with remarks."),
        ("6. Live Student Tracking", "Applicant tracks decision timeline (Under Review, Accepted, Rejected) in real time.")
    ]
    for s_title, s_desc in steps:
        ps = tf3.add_paragraph()
        ps.space_after = Pt(6)
        r1 = ps.add_run()
        r1.text = "▸ " + s_title + ": "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(10.5)
        r1.font.bold = True
        r1.font.color.rgb = C_DARK
        r2 = ps.add_run()
        r2.text = s_desc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(10.0)
        r2.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 3: SRS & Multi-Actor Matrix
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Software Requirements Specification & Actor Matrix", "System Requirements & Governance", 3)

    scope_box = add_container(s3, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.95),
                              bg_color=C_SHADE_SLATE, border_color=C_BORDER_SLATE)
    stf = scope_box.text_frame
    stf.word_wrap = True
    stf.margin_left = Inches(0.2)
    stf.margin_top = Inches(0.12)
    sp0 = stf.paragraphs[0]
    sp0.text = "Requirements Baseline: 20 Functional Requirements (FR-01 to FR-20) + 5 Non-Functional Requirements (NFR-01 to NFR-05)"
    sp0.font.name = FONT_NAME
    sp0.font.size = Pt(11.5)
    sp0.font.bold = True
    sp0.font.color.rgb = C_PRIMARY_DARK
    sp1 = stf.add_paragraph()
    sp1.text = "Explicit Scope Boundary: Out-of-scope for 20-day delivery: Online payment gateways, SMS/OTP gateways, biometric auth, and screen resolutions below 1366×768."
    sp1.font.name = FONT_NAME
    sp1.font.size = Pt(9.5)
    sp1.font.color.rgb = C_MUTED

    actors = [
        {
            "title": "1. Student / Applicant Portal",
            "bg": C_SHADE_BLUE,
            "border": C_BORDER_BLUE,
            "color": C_PRIMARY_DARK,
            "items": [
                ("FR-01/02:", "Registration & login with password policy (>=8 chars, uppercase, special char)."),
                ("FR-03/04:", "Personal bio data capture and academic programme selection."),
                ("FR-05/06:", "Document upload limited strictly to PDF format (<=5MB)."),
                ("FR-08/09:", "Final submission and permanent immutable application locking."),
                ("FR-10/11:", "Personal dashboard displaying live application lifecycle status.")
            ]
        },
        {
            "title": "2. Administrator Workspace",
            "bg": C_SHADE_GREEN,
            "border": C_BORDER_GREEN,
            "color": C_SUCCESS_DARK,
            "items": [
                ("FR-14/15:", "Role-based authentication & full applications triage queue."),
                ("FR-16:", "Instant search & filtering by candidate name, course, or status."),
                ("FR-17/18:", "Deep application inspection and direct PDF marksheet download."),
                ("FR-19:", "State transition execution (Under Review, Accepted, Rejected)."),
                ("NFR-03:", "Dual view toggle: Compact Table Mode vs Detailed Card View.")
            ]
        },
        {
            "title": "3. Executive Director Oversight",
            "bg": C_SHADE_AMBER,
            "border": C_BORDER_AMBER,
            "color": C_WARNING_DARK,
            "items": [
                ("FR-20:", "Executive dashboard summarizing real-time admission counts by status."),
                ("FR-12:", "One-click CSV data export of applicant records for offline analysis."),
                ("Role Guard:", "Enforced read-only mode preventing unauthorized status changes."),
                ("Ergonomics:", "Designed specifically for rapid executive reviews without deep triage.")
            ]
        }
    ]

    act_w = Inches(3.77)
    act_gap = Inches(0.21)
    for i, a in enumerate(actors):
        a_box = add_container(s3, Inches(0.8) + i * (act_w + act_gap), Inches(2.60), act_w, Inches(3.00),
                              bg_color=a["bg"], border_color=a["border"])
        add_container_content(a_box, a["title"], a["items"], title_color=a["color"],
                              item_size=Pt(9.5), prefix_size=Pt(10.0), title_size=Pt(12.5))

    nfr_box = add_container(s3, Inches(0.8), Inches(5.75), Inches(11.733), Inches(1.10),
                            bg_color=C_SHADE_INDIGO, border_color=C_BORDER_INDIGO)
    ntf = nfr_box.text_frame
    ntf.word_wrap = True
    ntf.margin_left = Inches(0.2)
    ntf.margin_top = Inches(0.10)
    np0 = ntf.paragraphs[0]
    np0.text = "Non-Functional Quality Benchmarks (NFR Compliance)"
    np0.font.name = FONT_NAME
    np0.font.size = Pt(11.0)
    np0.font.bold = True
    np0.font.color.rgb = C_PRIMARY_DARK
    np0.space_after = Pt(2)

    np1 = ntf.add_paragraph()
    np1.text = "• NFR-01 (Performance): Dashboard loads in <3s   • NFR-02 (Security): Salted PBKDF2 cryptography & JWT tokens   • NFR-03 (Usability): Search filter in <1s with dual view toggle\n• NFR-04 (Reliability): 98%+ PDF upload success rate   • NFR-05 (Compatibility): Windows 11 Chrome & Edge"
    np1.font.name = FONT_NAME
    np1.font.size = Pt(9.5)
    np1.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 4: Architecture & Dual-Engine Persistence
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "System Architecture & Dual-Engine Database Abstraction", "High-Level Architecture (HLD)", 4)

    # Embed High-Resolution Architecture Diagram on Left with EXACT HEIGHT
    diag_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig1_architecture.png")
    if os.path.exists(diag_path):
        s4.shapes.add_picture(diag_path, Inches(0.8), Inches(1.45), height=Inches(5.35))

    # Right Column: 3 Light-Shaded Explanatory Containers
    r_box1 = add_container(s4, Inches(5.80), Inches(1.45), Inches(6.733), Inches(1.65),
                           bg_color=C_SHADE_BLUE, border_color=C_BORDER_BLUE)
    add_container_content(r_box1, "Presentation & Application Tiers", [
        ("Presentation Layer:", "Responsive Single Page Application (SPA) in Chrome/Edge on Windows 11 using asynchronous JSON REST over TLS."),
        ("FastAPI ASGI Server:", "High-concurrency microservice with Pydantic validation schemas, RBAC auth middleware, and CORS security.")
    ], title_color=C_PRIMARY_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    r_box2 = add_container(s4, Inches(5.80), Inches(3.30), Inches(6.733), Inches(2.00),
                           bg_color=C_SHADE_AMBER, border_color=C_BORDER_AMBER)
    add_container_content(r_box2, "Dual-Engine Database Abstraction Layer", [
        ("Intelligent Router:", "Unified database layer in database.py encapsulating both MongoDB Atlas Cloud and SQLite3 embedded engines."),
        ("Automatic DNS Resolution:", "Injects public nameservers (8.8.8.8, 1.1.1.1) to overcome Windows SRV DNS record failures in campus networks."),
        ("Zero-Downtime Failover:", "If MongoDB ping fails or exceeds 4000ms, seamlessly defaults to SQLite (iem_admission.db) without dropping requests.")
    ], title_color=C_WARNING_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    r_box3 = add_container(s4, Inches(5.80), Inches(5.50), Inches(6.733), Inches(1.35),
                           bg_color=C_SHADE_GREEN, border_color=C_BORDER_GREEN)
    add_container_content(r_box3, "Decoupled Document Storage Subsystem", [
        ("MIME & Boundary Guard:", "Verifies magic byte headers to prevent malicious execution and enforces 5MB limit."),
        ("Hybrid Persistence:", "Saves files to local /uploads or serverless /tmp, storing lightweight URI references in DB.")
    ], title_color=C_SUCCESS_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    # =========================================================================
    # SLIDE 5: Data Flow Architecture (DFD)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Data Flow Architecture & Subsystem Interaction (DFD)", "System Data Flow & Stores", 5)

    dfd_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slide_dfd_diagram.png")
    if os.path.exists(dfd_path):
        s5.shapes.add_picture(dfd_path, Inches(2.35), Inches(1.40), height=Inches(2.25))

    # 3 Light-Shaded Containers below DFD Diagram
    c5_1 = add_container(s5, Inches(0.8), Inches(3.85), act_w, Inches(3.00),
                         bg_color=C_SHADE_BLUE, border_color=C_BORDER_BLUE)
    add_container_content(c5_1, "1.0 - 3.0 Core Admission Pipeline", [
        ("1.0 Manage Auth:", "Verifies credentials, hashes passwords, reads/writes D1, and issues signed JWT tokens."),
        ("2.0 Manage Details:", "Validates personal details, Class 10/12 marks, and course selection; updates draft in D1."),
        ("3.0 Process Upload:", "Validates PDF stream, writes binary to D2 Document Storage, and links URI in D1.")
    ], title_color=C_PRIMARY_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    c5_2 = add_container(s5, Inches(0.8) + act_w + act_gap, Inches(3.85), act_w, Inches(3.00),
                         bg_color=C_SHADE_GREEN, border_color=C_BORDER_GREEN)
    add_container_content(c5_2, "4.0 - 5.0 Submission & Triage", [
        ("4.0 Manage Submission:", "Freezes draft, stamps submission timestamp, and irreversibly sets status to 'Submitted'."),
        ("5.0 Status Management:", "Enables admin to search/filter candidates, inspect marksheets from D2, and update status with audit logs."),
        ("Executive Queries:", "Director requests aggregated metrics and downloads filtered CSV reports directly from 5.0.")
    ], title_color=C_SUCCESS_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    c5_3 = add_container(s5, Inches(0.8) + 2 * (act_w + act_gap), Inches(3.85), act_w, Inches(3.00),
                         bg_color=C_SHADE_AMBER, border_color=C_BORDER_AMBER)
    add_container_content(c5_3, "Data Stores D1 & D2 Specifications", [
        ("D1: Student/Application Data:", "Persists user credentials, applicant profiles, academic percentages, application statuses, and audit logs."),
        ("D2: Document Storage:", "Physical filesystem (/uploads) storing PDF marksheets with sanitized unique identifiers."),
        ("Referential Integrity:", "D1 holds relative URI path references to D2 file objects.")
    ], title_color=C_WARNING_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    # =========================================================================
    # SLIDE 6: State Machine & Business Rules
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Admission Workflow Engine & Finite-State Machine", "State Machine & Business Logic", 6)

    sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slide_state_machine.png")
    if os.path.exists(sm_path):
        s6.shapes.add_picture(sm_path, Inches(2.55), Inches(1.40), height=Inches(2.25))

    c6_1 = add_container(s6, Inches(0.8), Inches(3.85), act_w, Inches(3.00),
                         bg_color=C_SHADE_BLUE, border_color=C_BORDER_BLUE)
    add_container_content(c6_1, "BR-01 & BR-02: Form Immutability", [
        ("BR-01 Password Policy:", "Passwords must be >=8 characters, contain >=1 uppercase letter, and >=1 special character."),
        ("BR-02 Application Edit Lock:", "Once an applicant submits, personal details, academic scores, and documents are locked permanently."),
        ("Server-Side Guard:", "Any post-submission mutation attempts trigger HTTP 403 Forbidden.")
    ], title_color=C_PRIMARY_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    c6_2 = add_container(s6, Inches(0.8) + act_w + act_gap, Inches(3.85), act_w, Inches(3.00),
                         bg_color=C_SHADE_AMBER, border_color=C_BORDER_AMBER)
    add_container_content(c6_2, "BR-03: Legal State Transitions", [
        ("Valid Workflow:", "Draft -> Submitted -> Under Review -> Accepted / Rejected."),
        ("Direct Rejection Guard:", "Applications in 'Submitted' state may be rejected directly ONLY if explanatory remarks are provided."),
        ("Terminal States:", "Both 'Accepted' and 'Rejected' are terminal; no further status reversals are permitted.")
    ], title_color=C_WARNING_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    c6_3 = add_container(s6, Inches(0.8) + 2 * (act_w + act_gap), Inches(3.85), act_w, Inches(3.00),
                         bg_color=C_SHADE_GREEN, border_color=C_BORDER_GREEN)
    add_container_content(c6_3, "BR-04 & Audit Trail Logging", [
        ("BR-04 Academic Score Bounds:", "Class 10 and 12 percentages must fall strictly between 0.0% and 100.0%."),
        ("Audit Trail Logging:", "Every state change records timestamp, actor email, previous state, new state, and remarks."),
        ("Compliance:", "Guarantees transparency and audit-readiness for university accreditation.")
    ], title_color=C_SUCCESS_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    # =========================================================================
    # SLIDE 7: UI/UX Wireframes & Ergonomics
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "UI/UX Architecture & Responsive Desktop Interfaces", "Frontend Engineering & Ergonomics", 7)

    grid_w = Inches(5.75)
    grid_h = Inches(2.55)
    gx_gap = Inches(0.23)
    gy_gap = Inches(0.25)

    u1 = add_container(s7, Inches(0.8), Inches(1.45), grid_w, grid_h,
                       bg_color=C_SHADE_BLUE, border_color=C_BORDER_BLUE)
    add_container_content(u1, "1. Authentication & Onboarding Portal", [
        ("Institutional Branding:", "Displays the official IEM laurel wreath crest and professional Google Sans typography."),
        ("Domain Validation:", "Enforces @gmail.com email domain constraints and client-side password strength checking."),
        ("Session Security:", "Stores authenticated session tokens securely, redirecting students to dashboard upon login.")
    ], title_color=C_PRIMARY_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    u2 = add_container(s7, Inches(0.8) + grid_w + gx_gap, Inches(1.45), grid_w, grid_h,
                       bg_color=C_SHADE_INDIGO, border_color=C_BORDER_INDIGO)
    add_container_content(u2, "2. 4-Step Student Application Wizard", [
        ("Guided Stepper:", "Step 1: Personal Details • Step 2: Academic Scores • Step 3: Document Upload • Step 4: Final Review."),
        ("Interactive Progress Bar:", "Visual step indicators guide students with real-time feedback on mandatory form fields."),
        ("Drag-and-Drop Upload:", "Intuitive PDF upload container with live size validation and file replacement preview.")
    ], title_color=C_PRIMARY_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    u3 = add_container(s7, Inches(0.8), Inches(1.45) + grid_h + gy_gap, grid_w, grid_h,
                       bg_color=C_SHADE_GREEN, border_color=C_BORDER_GREEN)
    add_container_content(u3, "3. Student Application Status Dashboard", [
        ("Live Timeline Tracker:", "Chronological progress stepper showing submission date, document verification, and final decision."),
        ("Application Summary Card:", "Displays unique Application ID (e.g. IEM-2026-0847), chosen course, and submitted scores."),
        ("Integrated Document Viewer:", "One-click preview and download of uploaded PDF marksheets directly from the browser.")
    ], title_color=C_SUCCESS_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    u4 = add_container(s7, Inches(0.8) + grid_w + gx_gap, Inches(1.45) + grid_h + gy_gap, grid_w, grid_h,
                       bg_color=C_SHADE_AMBER, border_color=C_BORDER_AMBER)
    add_container_content(u4, "4. Administrator Workspace & Dual View Modes", [
        ("Real-time Metric Cards:", "Top KPI counters showing Total, Pending Review, Accepted, and Rejected application volumes."),
        ("Dual View Toggle (NFR-03):", "Switch smoothly between Compact Table Mode (fast triage) and Detailed Card Mode (in-depth inspection)."),
        ("Live Search & Status Updater:", "Instant sub-second applicant search with modal dialog for status updates, remarks, and CSV export.")
    ], title_color=C_WARNING_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    # =========================================================================
    # SLIDE 8: Software Verification & Quality Assurance
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Software Verification, Testing Strategy & Quality Metrics", "Testing Strategy & Quality Governance", 8)

    t_box1 = add_container(s8, Inches(0.8), Inches(1.45), Inches(5.7), Inches(2.60),
                           bg_color=C_SHADE_BLUE, border_color=C_BORDER_BLUE)
    add_container_content(t_box1, "White-Box Testing: McCabe's Basis Path Analysis", [
        ("Target Logic Module:", "validate_status_transition(current, new, remarks) in backend/workflow.py."),
        ("Control Flow Graph (CFG):", "Nodes (N) = 20, Edges (E) = 27, Decision Predicates (P) = 9."),
        ("Cyclomatic Complexity:", "V(G) = E - N + 2P = 27 - 20 + 2(1) = 9 (or P + 1 = 10 independent paths)."),
        ("100% Path Coverage:", "Codified all 10 linearly independent paths into automated unit test assertions.")
    ], title_color=C_PRIMARY_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    t_box2 = add_container(s8, Inches(0.8), Inches(4.25), Inches(5.7), Inches(2.60),
                           bg_color=C_SHADE_SLATE, border_color=C_BORDER_SLATE)
    add_container_content(t_box2, "Black-Box Test Design (BVA & ECP)", [
        ("Equivalence Partitioning:", "Password complexity (min 8 chars, uppercase, special character) and phone format partitions."),
        ("Boundary Value Analysis:", "Academic percentages tested at 0.0%, 100.0%, -0.1%, and 100.1%."),
        ("File Upload Thresholds:", "Tested 4.99MB (accepted), 5.00MB (accepted boundary), and 5.01MB (rejected with HTTP 422).")
    ], title_color=C_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    t_box3 = add_container(s8, Inches(6.83), Inches(1.45), Inches(5.70), Inches(2.60),
                           bg_color=C_SHADE_GREEN, border_color=C_BORDER_GREEN)
    add_container_content(t_box3, "Automated Test Suite (backend/test_suite.py)", [
        ("Test Execution Status:", "16 out of 16 Automated Test Fixtures Passing (100% Pass Rate)."),
        ("Multi-Database Parity:", "Executed identically against both SQLite3 and live MongoDB Atlas without regressions."),
        ("Sandwich Integration:", "Lightweight synthetic JWT tokens and mock PDF byte buffers used as stubs and drivers."),
        ("Zero Defect Escape:", "Automated regression suite executed on every code commit.")
    ], title_color=C_SUCCESS_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    t_box4 = add_container(s8, Inches(6.83), Inches(4.25), Inches(5.70), Inches(2.60),
                           bg_color=C_SHADE_AMBER, border_color=C_BORDER_AMBER)
    add_container_content(t_box4, "Test Governance & Roles", [
        ("Unit Testing:", "Executed by Sreejita Dey (Backend) and Debadrita Dutta (Test Lead)."),
        ("Integration Testing:", "Managed by Susnata Maiti (Frontend/Integration) and Sreejita Dey (Backend)."),
        ("System Testing:", "Managed by Debadrita Dutta; verified against all 20 FRs and 5 NFRs on Windows 11 with sponsor sign-off.")
    ], title_color=C_WARNING_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    # =========================================================================
    # SLIDE 9: Cloud Deployment & Live Demonstration (Spacious Diagram)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Cloud Deployment, Serverless Edge & Live Demonstration", "Cloud Architecture & Live Demonstration", 9)

    # Deployment Graphic (Enhanced spacious layout, width ~ 6.5 in, height 2.35 in, centered)
    dep_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slide_deployment_diagram.png")
    if os.path.exists(dep_path):
        s9.shapes.add_picture(dep_path, Inches(3.42), Inches(1.35), height=Inches(2.35))

    # 3 Light-Shaded Containers below Deployment Diagram (Starting safely at 3.90 in)
    c9_1 = add_container(s9, Inches(0.8), Inches(3.90), act_w, Inches(2.95),
                         bg_color=C_SHADE_BLUE, border_color=C_BORDER_BLUE)
    add_container_content(c9_1, "Live Production Deployment", [
        ("Live Vercel Production URL:", "https://iem-admission-system-nexus-p4.vercel.app/"),
        ("Global CDN Edge Routing:", "Static assets served from global edge caches with automated HTTPS/TLS 1.3 termination."),
        ("Serverless ASGI Handler:", "api/index.py bridges Vercel serverless requests into the FastAPI ASGI application seamlessly.")
    ], title_color=C_PRIMARY_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    c9_2 = add_container(s9, Inches(0.8) + act_w + act_gap, Inches(3.90), act_w, Inches(2.95),
                         bg_color=C_SHADE_GREEN, border_color=C_BORDER_GREEN)
    add_container_content(c9_2, "Hybrid Execution & Portability", [
        ("Dual Environment Parity:", "Runs identically locally on Windows 11 via python run_server.py and on Vercel Cloud Serverless."),
        ("Zero Code Mutation:", "Dynamic environment inspection detects host runtime and adjusts static routes automatically."),
        ("Ephemeral File Handling:", "Utilizes /tmp on serverless instances to ensure PDF processing without local disk dependency.")
    ], title_color=C_SUCCESS_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    c9_3 = add_container(s9, Inches(0.8) + 2 * (act_w + act_gap), Inches(3.90), act_w, Inches(2.95),
                         bg_color=C_SHADE_AMBER, border_color=C_BORDER_AMBER)
    add_container_content(c9_3, "Fault Isolation & Resilience", [
        ("MongoDB Atlas Connectivity:", "Connects to cloud replica set; auto-injects public DNS to bypass SRV query failures."),
        ("Offline Graceful Fallback:", "If network isolation occurs, application continues servicing requests using local SQLite storage."),
        ("Zero Data Loss Guarantee:", "Student submissions and audit trails remain intact across all failure scenarios.")
    ], title_color=C_WARNING_DARK, item_size=Pt(9.8), prefix_size=Pt(10.5))

    # =========================================================================
    # SLIDE 10: Milestones, Conclusion & Roadmap
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Project Milestones, Value Delivered & Future Roadmap", "Project Evaluation & Next Steps", 10)

    m_box = add_container(s10, Inches(0.8), Inches(1.45), Inches(11.733), Inches(1.90),
                          bg_color=C_SHADE_SLATE, border_color=C_BORDER_SLATE)
    mtf = m_box.text_frame
    mtf.word_wrap = True
    mtf.margin_left = Inches(0.2)
    mtf.margin_top = Inches(0.12)
    mp0 = mtf.paragraphs[0]
    mp0.text = "20-Day Project Milestone Execution Schedule (100% Completed on Schedule)"
    mp0.font.name = FONT_NAME
    mp0.font.size = Pt(12)
    mp0.font.bold = True
    mp0.font.color.rgb = C_PRIMARY_DARK
    mp0.space_after = Pt(4)

    milestones = [
        ("Days 1–3 (Planning):", "Requirements gathering, Project Charter sign-off, SRS & HLD drafting, UML modeling."),
        ("Days 4–10 (Frontend):", "Figma wireframe alignment, responsive UI development, 4-step wizard form building."),
        ("Days 11–15 (Backend & DB):", "FastAPI endpoints, PBKDF2 hashing, dual-engine DB abstraction, PDF upload handling."),
        ("Days 16–18 (Testing & QA):", "End-to-end integration, Basis Path analysis (10 paths), 16 automated tests execution."),
        ("Days 19–20 (Delivery):", "Final documentation, user acceptance testing on Windows 11, and Vercel cloud deployment.")
    ]
    for m_phase, m_desc in milestones:
        mp = mtf.add_paragraph()
        r1 = mp.add_run()
        r1.text = "• " + m_phase + " "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = C_DARK
        r2 = mp.add_run()
        r2.text = m_desc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_MUTED

    ach_box = add_container(s10, Inches(0.8), Inches(3.55), Inches(5.75), Inches(2.35),
                            bg_color=C_SHADE_GREEN, border_color=C_BORDER_GREEN)
    add_container_content(ach_box, "Key Achievements & Value Delivered", [
        ("Academic Excellence:", "Engineered a robust admissions system fulfilling all 20 FRs and 5 NFRs within 20 days."),
        ("Fault Tolerant Persistence:", "Dual-engine persistence layer eliminates downtime risks from campus DNS outages."),
        ("Rigorous Quality Assurance:", "100% pass rate across automated regression fixtures with complete basis path coverage."),
        ("Stakeholder Alignment:", "Delivered dedicated workspaces for Students, Admins, and Executive Directors.")
    ], title_color=C_SUCCESS_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    fut_box = add_container(s10, Inches(6.78), Inches(3.55), Inches(5.75), Inches(2.35),
                            bg_color=C_SHADE_BLUE, border_color=C_BORDER_BLUE)
    add_container_content(fut_box, "Future Roadmap & Technological Extensions", [
        ("Online Payment Gateway:", "Integrate Razorpay/Stripe API for automated admission fee processing with digital receipts."),
        ("Multichannel Alerts:", "Automated SMS, WhatsApp, and Email triggers for real-time application milestone notifications."),
        ("AI Document Verification:", "Deploy Vision OCR microservices to automatically parse and verify marks from marksheets."),
        ("Enrolment Analytics:", "Predictive enrolment yield modeling for academic department capacity planning.")
    ], title_color=C_PRIMARY_DARK, item_size=Pt(9.6), prefix_size=Pt(10.2))

    t_box = add_container(s10, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.80),
                          bg_color=C_SHADE_INDIGO, border_color=C_BORDER_INDIGO)
    ttf = t_box.text_frame
    ttf.word_wrap = True
    ttf.margin_left = Inches(0.2)
    ttf.margin_top = Inches(0.08)
    tp = ttf.paragraphs[0]
    tp.alignment = PP_ALIGN.CENTER
    tp.text = "Thank You! Questions & Discussion"
    tp.font.name = FONT_NAME
    tp.font.size = Pt(13.5)
    tp.font.bold = True
    tp.font.color.rgb = C_PRIMARY_DARK

    tp_sub = ttf.add_paragraph()
    tp_sub.alignment = PP_ALIGN.CENTER
    tp_sub.text = "Team Nexus (P4)  •  Susnata Maiti  |  Sreejita Dey  |  Swapnil Ghosh  |  Debadrita Dutta"
    tp_sub.font.name = FONT_NAME
    tp_sub.font.size = Pt(9.8)
    tp_sub.font.color.rgb = C_MUTED

    prs.save(out_path)
    print(f"Presentation successfully updated at: {out_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(out_dir, "IEM_Admission_System_Presentation.pptx")
    build_presentation(out_file)
