import os
import base64

def get_base64_img(path):
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

def build_html_presentation(out_path):
    docs_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(docs_dir)

    fig1_b64 = get_base64_img(os.path.join(docs_dir, "fig1_architecture.png"))
    sm_b64 = get_base64_img(os.path.join(docs_dir, "slide_state_machine.png"))
    dfd_b64 = get_base64_img(os.path.join(docs_dir, "slide_dfd_diagram.png"))
    dep_b64 = get_base64_img(os.path.join(docs_dir, "slide_deployment_diagram.png"))

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IEM Admission System - Project Presentation</title>
  <!-- Google Sans / Open Sans Font -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --font-family: 'Google Sans', 'Open Sans', system-ui, -apple-system, sans-serif;
      --bg-canvas: #0b1120;
      --bg-slide: #f8fafc;
      --text-dark: #0f172a;
      --text-muted: #334155;
      --primary: #2563eb;
      --primary-dark: #1e3a8a;
      
      /* Light Shaded Container Palette */
      --shade-slate: #f1f5f9;
      --border-slate: #cbd5e1;
      
      --shade-blue: #eff6ff;
      --border-blue: #93c5fd;
      
      --shade-green: #f0fdf4;
      --border-green: #86efac;
      
      --shade-amber: #fefce8;
      --border-amber: #fde047;
      
      --shade-purple: #faf5ff;
      --border-purple: #d8b4fe;

      --shade-indigo: #eef2ff;
      --border-indigo: #a5b4fc;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-family);
      background-color: var(--bg-canvas);
      color: var(--text-dark);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      overflow: hidden;
    }}

    /* Presentation Frame (16:9 Widescreen) */
    .deck-container {{
      position: relative;
      width: 96vw;
      max-width: 1420px;
      height: 54vw;
      max-height: 798px;
      background: var(--bg-slide);
      border-radius: 16px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}

    .slide {{
      display: none;
      flex-direction: column;
      width: 100%;
      height: 100%;
      padding: 26px 36px 16px 36px;
      overflow: hidden;
    }}

    .slide.active {{
      display: flex;
      animation: fadeIn 0.22s ease-out;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: scale(0.995); }}
      to {{ opacity: 1; transform: scale(1); }}
    }}

    /* Slide Header */
    .slide-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
      flex-shrink: 0;
    }}

    .category-badge {{
      display: inline-block;
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--primary);
      margin-bottom: 3px;
    }}

    .slide-title {{
      font-size: 1.68rem;
      font-weight: 700;
      color: var(--text-dark);
      line-height: 1.2;
    }}

    .slide-num {{
      font-size: 0.88rem;
      font-weight: 700;
      color: #475569;
      background: #e2e8f0;
      padding: 5px 12px;
      border-radius: 20px;
    }}

    /* Slide Content & Containers */
    .slide-body {{
      flex: 1;
      display: flex;
      gap: 16px;
      min-height: 0;
    }}

    .col {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      min-height: 0;
    }}

    .col-half {{ flex: 1; }}
    .col-3 {{ flex: 1; }}
    .col-4 {{ flex: 1; }}

    /* Light Shaded Container Styling */
    .container-box {{
      border-radius: 12px;
      padding: 13px 16px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
      display: flex;
      flex-direction: column;
      gap: 5px;
      overflow: hidden;
      border: 1.5px solid var(--border-slate);
      background: var(--shade-slate);
    }}

    .container-box.shade-blue {{
      background: var(--shade-blue);
      border-color: var(--border-blue);
    }}

    .container-box.shade-green {{
      background: var(--shade-green);
      border-color: var(--border-green);
    }}

    .container-box.shade-amber {{
      background: var(--shade-amber);
      border-color: var(--border-amber);
    }}

    .container-box.shade-purple {{
      background: var(--shade-purple);
      border-color: var(--border-purple);
    }}

    .container-box.shade-indigo {{
      background: var(--shade-indigo);
      border-color: var(--border-indigo);
    }}

    .container-box.shade-slate {{
      background: var(--shade-slate);
      border-color: var(--border-slate);
    }}

    .container-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-dark);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .container-title .badge {{
      font-size: 0.72rem;
      padding: 2px 8px;
      border-radius: 12px;
      font-weight: 600;
    }}

    .badge-blue {{ background: #dbeafe; color: #1e40af; }}
    .badge-green {{ background: #dcfce7; color: #15803d; }}
    .badge-amber {{ background: #fef3c7; color: #b45309; }}
    .badge-purple {{ background: #f3e8ff; color: #7e22ce; }}

    .item-list {{
      display: flex;
      flex-direction: column;
      gap: 5px;
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.38;
    }}

    .item-row {{
      display: flex;
      align-items: flex-start;
      gap: 6px;
    }}

    .item-row strong {{
      color: var(--text-dark);
      font-weight: 700;
      white-space: nowrap;
    }}

    /* Graphic Displays */
    .diagram-img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      border-radius: 8px;
    }}

    /* Slide Footer */
    .slide-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 8px;
      border-top: 1px solid var(--border-slate);
      font-size: 0.78rem;
      color: #64748b;
      flex-shrink: 0;
    }}

    /* Nav Bar Controls */
    .controls {{
      margin-top: 14px;
      display: flex;
      gap: 12px;
      align-items: center;
    }}

    .btn {{
      background: #1e293b;
      color: #ffffff;
      border: 1px solid #334155;
      padding: 8px 18px;
      border-radius: 8px;
      font-family: var(--font-family);
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .btn:hover {{
      background: var(--primary);
      border-color: var(--primary);
    }}

    .btn:disabled {{
      opacity: 0.4;
      cursor: not-allowed;
    }}

    .indicator {{
      color: #94a3b8;
      font-size: 0.88rem;
      font-weight: 500;
      min-width: 90px;
      text-align: center;
    }}
  </style>
</head>
<body>

  <div class="deck-container" id="deckContainer">

    <!-- SLIDE 1: Title & Team Nexus -->
    <div class="slide active" id="slide-1">
      <div class="container-box shade-blue" style="padding: 16px 24px; margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div class="category-badge">PCCCS504 Software Engineering & Project Management Lab • AY 2026-27</div>
            <div style="font-size: 1.85rem; font-weight: 700; color: var(--primary-dark); line-height: 1.2;">IEM Admission System Software</div>
            <div style="font-size: 1.0rem; color: var(--text-muted); margin-top: 3px;">A Resilient, Dual-Engine College Admissions & Verification Platform</div>
          </div>
          <div style="text-align: right;">
            <div class="badge badge-blue" style="font-size: 0.85rem; padding: 4px 12px;">Team P4 : Nexus</div>
            <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 4px;">Batch: 2024-2028 | 5th Semester</div>
          </div>
        </div>
      </div>

      <!-- 4 Light-Shaded Team Member Cards -->
      <div class="slide-body" style="gap: 12px; margin-bottom: 12px;">
        <!-- Susnata Maiti -->
        <div class="container-box col-4 shade-blue" style="border-top: 4px solid var(--primary);">
          <div style="font-size: 1.15rem; font-weight: 700; color: var(--text-dark);">Susnata Maiti</div>
          <div style="font-size: 0.82rem; color: #64748b;">Roll: A-11 • CSE</div>
          <div class="badge badge-blue" style="width: fit-content; margin: 4px 0; font-size: 0.78rem;">Role: Frontend Developer</div>
          <div style="font-size: 0.78rem; color: var(--primary); word-break: break-all; font-weight: 600;">maitisusnata135531@gmail.com</div>
          <div class="item-list" style="margin-top: 8px;">
            <div class="item-row"><strong>Focus:</strong> Responsive SPA UI/UX, Google Sans design, 4-step wizard form, client-side validation.</div>
            <div class="item-row"><strong>Deliverables:</strong> REST API client, error toasts, and real-time student dashboard.</div>
          </div>
        </div>

        <!-- Sreejita Dey -->
        <div class="container-box col-4 shade-green" style="border-top: 4px solid #10b981;">
          <div style="font-size: 1.15rem; font-weight: 700; color: var(--text-dark);">Sreejita Dey</div>
          <div style="font-size: 0.82rem; color: #64748b;">Roll: A-29 • CSE</div>
          <div class="badge badge-green" style="width: fit-content; margin: 4px 0; font-size: 0.78rem;">Role: Backend Developer</div>
          <div style="font-size: 0.78rem; color: #047857; word-break: break-all; font-weight: 600;">sreejitad05@gmail.com</div>
          <div class="item-list" style="margin-top: 8px;">
            <div class="item-row"><strong>Focus:</strong> FastAPI ASGI service, PBKDF2 password hashing, JWT bearer tokens, RBAC security.</div>
            <div class="item-row"><strong>Deliverables:</strong> Finite-state machine workflow engine and audit trail logging.</div>
          </div>
        </div>

        <!-- Swapnil Ghosh -->
        <div class="container-box col-4 shade-amber" style="border-top: 4px solid #f59e0b;">
          <div style="font-size: 1.15rem; font-weight: 700; color: var(--text-dark);">Swapnil Ghosh</div>
          <div style="font-size: 0.82rem; color: #64748b;">Roll: A-04 • CSE</div>
          <div class="badge badge-amber" style="width: fit-content; margin: 4px 0; font-size: 0.78rem;">Role: Database Lead</div>
          <div style="font-size: 0.78rem; color: #b45309; word-break: break-all; font-weight: 600;">swapnilghosh2005@gmail.com</div>
          <div class="item-list" style="margin-top: 8px;">
            <div class="item-row"><strong>Focus:</strong> Dual-engine database abstraction layer (MongoDB Atlas + SQLite3 embedded failover).</div>
            <div class="item-row"><strong>Deliverables:</strong> Auto DNS SRV resolver recovery, schemas, document storage (/uploads).</div>
          </div>
        </div>

        <!-- Debadrita Dutta -->
        <div class="container-box col-4 shade-purple" style="border-top: 4px solid #9333ea;">
          <div style="font-size: 1.15rem; font-weight: 700; color: var(--text-dark);">Debadrita Dutta</div>
          <div style="font-size: 0.82rem; color: #64748b;">Roll: A-12 • CSE</div>
          <div class="badge badge-purple" style="width: fit-content; margin: 4px 0; font-size: 0.78rem;">Role: Test Lead</div>
          <div style="font-size: 0.78rem; color: #7e22ce; word-break: break-all; font-weight: 600;">debadritadutta831@gmail.com</div>
          <div class="item-list" style="margin-top: 8px;">
            <div class="item-row"><strong>Focus:</strong> Software test strategy & plan, McCabe's basis path testing, black-box BVA/ECP design.</div>
            <div class="item-row"><strong>Deliverables:</strong> 16-fixture automated regression runner, 100% path coverage, defect log.</div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div>Faculty In-Charge: <strong>Prof. Sangeeta Sarkar</strong> & <strong>Prof. Saikat Dutta</strong></div>
        <div>Project Sponsor & Director, IEM: <strong>Dr. Satyajit Chakrabarti</strong></div>
      </div>
    </div>

    <!-- SLIDE 2: Problem Statement & Charter -->
    <div class="slide" id="slide-2">
      <div class="slide-header">
        <div>
          <div class="category-badge">Project Scope & Charter Baseline</div>
          <div class="slide-title">Problem Statement & 6-Stage Admission Lifecycle</div>
        </div>
        <div class="slide-num">Slide 2 / 10</div>
      </div>
      <div class="slide-body">
        <div class="col col-half">
          <div class="container-box shade-slate" style="flex: 1;">
            <div class="container-title" style="color: var(--primary-dark);">The Problem & Operational Challenges</div>
            <div class="item-list">
              <div class="item-row"><strong>Legacy Inefficiencies:</strong> Manual paper forms and unvalidated portals cause application loss and processing delays.</div>
              <div class="item-row"><strong>Network Fragility:</strong> Institutional campus networks frequently drop cloud database connections during peak admission rush.</div>
              <div class="item-row"><strong>Upload Risks:</strong> Corrupt non-PDF documents and oversized files crash application handlers and consume disk storage.</div>
              <div class="item-row"><strong>Core Mission:</strong> Deliver a self-contained, dual-engine admissions system with zero downtime and immutable data governance.</div>
            </div>
          </div>
          <div class="container-box shade-blue" style="flex: 1;">
            <div class="container-title" style="color: var(--primary);">Project Charter Constraints & Governance</div>
            <div class="item-list">
              <div class="item-row"><strong>Timeline:</strong> Strict 20-day delivery lifecycle from charter sign-off to full production deployment.</div>
              <div class="item-row"><strong>Target Platform:</strong> Windows 11 Desktop running Google Chrome or Microsoft Edge (1366×768+).</div>
              <div class="item-row"><strong>Technology Stack:</strong> Next.js / Vanilla JS Frontend, FastAPI ASGI backend, and Dual DB layer.</div>
              <div class="item-row"><strong>Operating Policy:</strong> Autonomous separation of duties across Frontend, Backend, Database, and Testing teams.</div>
            </div>
          </div>
        </div>
        <div class="col col-half">
          <div class="container-box shade-amber" style="flex: 1;">
            <div class="container-title" style="color: #92400e;">6-Stage End-to-End Admission Workflow</div>
            <div class="item-list">
              <div class="item-row"><strong>1. Registration & Auth:</strong> Salted password hashing via PBKDF2; @gmail.com email domain enforcement.</div>
              <div class="item-row"><strong>2. 4-Step Form Wizard:</strong> Student inputs personal details, academic scores (Class 10/12), and course selection.</div>
              <div class="item-row"><strong>3. PDF Marksheet Upload:</strong> Strict MIME header verification and 5MB size limit before saving.</div>
              <div class="item-row"><strong>4. Immutable Lock:</strong> Timestamped final submit locks all form fields against subsequent modification.</div>
              <div class="item-row"><strong>5. Admin Triage:</strong> Admission officers filter applications, inspect documents, and update status with remarks.</div>
              <div class="item-row"><strong>6. Live Tracking:</strong> Real-time student tracking timeline displaying decision progress (Under Review, Accepted, Rejected).</div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div>IEM Admission System • Team Nexus (P4)</div>
        <div>PCCCS504 Software Engineering & Project Management Lab</div>
      </div>
    </div>

    <!-- SLIDE 3: SRS & Multi-Actor Matrix -->
    <div class="slide" id="slide-3">
      <div class="slide-header">
        <div>
          <div class="category-badge">Software Requirements Specification (SRS)</div>
          <div class="slide-title">System Requirements Baseline & Multi-Actor Matrix</div>
        </div>
        <div class="slide-num">Slide 3 / 10</div>
      </div>
      <div class="slide-body" style="flex-direction: column;">
        <div class="container-box shade-slate" style="padding: 10px 16px;">
          <div style="font-size: 0.95rem; font-weight: 700; color: var(--primary-dark);">Scope Baseline: 20 Functional Requirements (FR-01 to FR-20) + 5 Non-Functional Requirements (NFR-01 to NFR-05)</div>
          <div style="font-size: 0.82rem; color: #475569;">Out-of-Scope: Online payment gateways, SMS/OTP gateways, biometric auth, and screen resolutions below 1366×768.</div>
        </div>

        <div style="display: flex; gap: 12px; flex: 1;">
          <div class="container-box col-3 shade-blue">
            <div class="container-title" style="color: var(--primary);">Student / Applicant Portal <span class="badge badge-blue">FR-01 to FR-11</span></div>
            <div class="item-list">
              <div class="item-row"><strong>FR-01/02:</strong> Registration & login with password policy (>=8 chars, uppercase, special char).</div>
              <div class="item-row"><strong>FR-03/04:</strong> Personal bio-data form and course choice from predefined options.</div>
              <div class="item-row"><strong>FR-05/06:</strong> Supporting PDF upload (<=5MB) linked to application record.</div>
              <div class="item-row"><strong>FR-08/09:</strong> Immutable submission lock preventing post-submission edits.</div>
              <div class="item-row"><strong>FR-10/11:</strong> Personal dashboard displaying live application lifecycle status.</div>
            </div>
          </div>

          <div class="container-box col-3 shade-green">
            <div class="container-title" style="color: #065f46;">Administrator Workspace <span class="badge badge-green">FR-14 to FR-19</span></div>
            <div class="item-list">
              <div class="item-row"><strong>FR-14/15:</strong> Authenticated triage console with complete candidate application list.</div>
              <div class="item-row"><strong>FR-16:</strong> Live multi-parameter search and filtering by name, course, and status.</div>
              <div class="item-row"><strong>FR-17/18:</strong> Deep candidate inspection and direct PDF marksheet preview/download.</div>
              <div class="item-row"><strong>FR-19:</strong> Status transitions (Under Review, Accepted, Rejected) with mandatory remarks.</div>
              <div class="item-row"><strong>NFR-03:</strong> Dual view toggle: Compact Table Mode vs Detailed Card View.</div>
            </div>
          </div>

          <div class="container-box col-3 shade-amber">
            <div class="container-title" style="color: #92400e;">Executive Director Oversight <span class="badge badge-amber">FR-12 & FR-20</span></div>
            <div class="item-list">
              <div class="item-row"><strong>FR-20:</strong> Executive dashboard summarizing application volume by status.</div>
              <div class="item-row"><strong>FR-12:</strong> One-click CSV export of full or filtered application records for offline audits.</div>
              <div class="item-row"><strong>Role Isolation:</strong> Enforced read-only mode preventing unauthorized status changes.</div>
              <div class="item-row"><strong>Rapid Review:</strong> Clean visual KPI cards tailored for university executives.</div>
            </div>
          </div>
        </div>

        <div class="container-box shade-indigo" style="padding: 10px 16px;">
          <div style="font-size: 0.90rem; font-weight: 700; color: var(--primary-dark);">Non-Functional Benchmarks (NFR Compliance)</div>
          <div style="font-size: 0.82rem; color: #475569;">
            • NFR-01 (Performance): Dashboard loads in <3s • NFR-02 (Security): Salted PBKDF2 cryptography & JWT tokens • NFR-03 (Usability): Search filter updates in <1s • NFR-04 (Reliability): 98%+ PDF upload success • NFR-05 (Compatibility): Windows 11 Chrome & Edge
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div>IEM Admission System • Team Nexus (P4)</div>
        <div>PCCCS504 Software Engineering & Project Management Lab</div>
      </div>
    </div>

    <!-- SLIDE 4: System Architecture & Dual Engine -->
    <div class="slide" id="slide-4">
      <div class="slide-header">
        <div>
          <div class="category-badge">High-Level Design (HLD)</div>
          <div class="slide-title">System Architecture & Dual-Engine Persistence</div>
        </div>
        <div class="slide-num">Slide 4 / 10</div>
      </div>
      <div class="slide-body">
        <div style="flex: 1.1; display: flex; align-items: center; justify-content: center; background: #ffffff; border: 1.5px solid var(--border-slate); border-radius: 12px; padding: 10px;">
          <img src="{fig1_b64}" class="diagram-img" alt="System Architecture Diagram">
        </div>
        <div class="col" style="flex: 1;">
          <div class="container-box shade-blue" style="flex: 1;">
            <div class="container-title" style="color: var(--primary-dark);">Presentation & Application Tiers</div>
            <div class="item-list">
              <div class="item-row"><strong>Presentation Tier:</strong> Responsive SPA rendered on Chrome/Edge (Windows 11) using modern asynchronous fetch requests over TLS.</div>
              <div class="item-row"><strong>FastAPI ASGI Service:</strong> High-performance async microservice with Pydantic validation schemas, RBAC auth middleware, and CORS security.</div>
            </div>
          </div>
          <div class="container-box shade-amber" style="flex: 1.3;">
            <div class="container-title" style="color: #92400e;">Intelligent Dual-Engine DB Abstraction</div>
            <div class="item-list">
              <div class="item-row"><strong>Unified Abstraction:</strong> database.py encapsulates both MongoDB Atlas (Cloud NoSQL) and SQLite3 (Embedded ACID engine).</div>
              <div class="item-row"><strong>Auto DNS Resolution:</strong> Injects Google (8.8.8.8) and Cloudflare (1.1.1.1) nameservers to resolve Windows SRV query failures.</div>
              <div class="item-row"><strong>Zero-Downtime Failover:</strong> If MongoDB Atlas ping exceeds 4000ms, seamlessly defaults to SQLite (iem_admission.db) without service disruption.</div>
            </div>
          </div>
          <div class="container-box shade-green" style="flex: 1;">
            <div class="container-title" style="color: #065f46;">Decoupled Document Storage</div>
            <div class="item-list">
              <div class="item-row"><strong>MIME & Size Validator:</strong> Multipart parser checks PDF magic headers and rejects files over 5MB.</div>
              <div class="item-row"><strong>Hybrid Storage:</strong> Writes files to local /uploads or serverless /tmp, storing lightweight URI references in the active database.</div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div>IEM Admission System • Team Nexus (P4)</div>
        <div>PCCCS504 Software Engineering & Project Management Lab</div>
      </div>
    </div>

    <!-- SLIDE 5: Data Flow Architecture (DFD) -->
    <div class="slide" id="slide-5">
      <div class="slide-header">
        <div>
          <div class="category-badge">System Data Flow & Data Stores</div>
          <div class="slide-title">Data Flow Architecture & Subsystem Interaction (DFD)</div>
        </div>
        <div class="slide-num">Slide 5 / 10</div>
      </div>
      <div class="slide-body" style="flex-direction: column;">
        <div style="height: 195px; display: flex; align-items: center; justify-content: center; background: #ffffff; border: 1.5px solid var(--border-slate); border-radius: 12px; padding: 6px;">
          <img src="{dfd_b64}" class="diagram-img" alt="DFD Diagram">
        </div>
        <div style="display: flex; gap: 12px; flex: 1;">
          <div class="container-box col-3 shade-blue">
            <div class="container-title" style="color: var(--primary);">1.0 - 3.0 Core Admission Pipeline</div>
            <div class="item-list">
              <div class="item-row"><strong>1.0 Manage Auth:</strong> Verifies credentials, hashes passwords, reads/writes D1, and issues signed JWT tokens.</div>
              <div class="item-row"><strong>2.0 Manage Details:</strong> Validates personal details, Class 10/12 marks, and course selection; updates draft application in D1.</div>
              <div class="item-row"><strong>3.0 Process Upload:</strong> Validates PDF stream, writes binary to D2 Document Storage, and links URI in D1.</div>
            </div>
          </div>
          <div class="container-box col-3 shade-green">
            <div class="container-title" style="color: #065f46;">4.0 - 5.0 Submission & Triage</div>
            <div class="item-list">
              <div class="item-row"><strong>4.0 Manage Submission:</strong> Freezes draft, stamps submission timestamp, and irreversibly sets status to 'Submitted'.</div>
              <div class="item-row"><strong>5.0 Status Management:</strong> Enables admin to search/filter candidates, inspect marksheets from D2, and update status with audit logs.</div>
              <div class="item-row"><strong>Executive Analytics:</strong> Director queries aggregated metrics and generates filtered CSV reports directly from 5.0.</div>
            </div>
          </div>
          <div class="container-box col-3 shade-amber">
            <div class="container-title" style="color: #92400e;">Data Stores D1 & D2 Specifications</div>
            <div class="item-list">
              <div class="item-row"><strong>D1: Student/Application Data:</strong> Persists user credentials, applicant profiles, academic percentages, application statuses, and audit logs.</div>
              <div class="item-row"><strong>D2: Document Storage:</strong> Physical filesystem (/uploads) storing PDF marksheets with sanitized unique identifiers.</div>
              <div class="item-row"><strong>Referential Integrity:</strong> D1 holds relative URI path references to D2 file objects.</div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div>IEM Admission System • Team Nexus (P4)</div>
        <div>PCCCS504 Software Engineering & Project Management Lab</div>
      </div>
    </div>

    <!-- SLIDE 6: State Machine & Business Rules -->
    <div class="slide" id="slide-6">
      <div class="slide-header">
        <div>
          <div class="category-badge">Finite State Machine & Validation Engine</div>
          <div class="slide-title">Admission Lifecycle State Machine & Business Rules</div>
        </div>
        <div class="slide-num">Slide 6 / 10</div>
      </div>
      <div class="slide-body" style="flex-direction: column;">
        <div style="height: 195px; display: flex; align-items: center; justify-content: center; background: #ffffff; border: 1.5px solid var(--border-slate); border-radius: 12px; padding: 6px;">
          <img src="{sm_b64}" class="diagram-img" alt="State Machine Diagram">
        </div>
        <div style="display: flex; gap: 12px; flex: 1;">
          <div class="container-box col-3 shade-blue">
            <div class="container-title" style="color: var(--primary);">BR-01 & BR-02: Form Immutability</div>
            <div class="item-list">
              <div class="item-row"><strong>BR-01 Password Policy:</strong> Passwords must be >=8 characters, contain >=1 uppercase letter, and >=1 special character.</div>
              <div class="item-row"><strong>BR-02 Application Edit Lock:</strong> Once an applicant submits, personal details, academic scores, and documents are locked permanently.</div>
              <div class="item-row"><strong>Server-Side Guard:</strong> Any post-submission mutation attempts trigger HTTP 403 Forbidden.</div>
            </div>
          </div>
          <div class="container-box col-3 shade-amber">
            <div class="container-title" style="color: #92400e;">BR-03: Legal State Transitions</div>
            <div class="item-list">
              <div class="item-row"><strong>Valid Workflow:</strong> Draft -> Submitted -> Under Review -> Accepted / Rejected.</div>
              <div class="item-row"><strong>Direct Rejection Guard:</strong> Applications in 'Submitted' state may be rejected directly ONLY if explanatory remarks are provided.</div>
              <div class="item-row"><strong>Terminal States:</strong> 'Accepted' and 'Rejected' are terminal; no further status reversals are permitted.</div>
            </div>
          </div>
          <div class="container-box col-3 shade-green">
            <div class="container-title" style="color: #065f46;">BR-04 & Audit Trail Logging</div>
            <div class="item-list">
              <div class="item-row"><strong>BR-04 Academic Score Bounds:</strong> Class 10 and 12 percentages must fall strictly between 0.0% and 100.0%.</div>
              <div class="item-row"><strong>Audit Trail Logging:</strong> Every state change records timestamp, actor email, previous state, new state, and remarks.</div>
              <div class="item-row"><strong>Compliance:</strong> Guarantees transparency and audit-readiness for university accreditation.</div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div>IEM Admission System • Team Nexus (P4)</div>
        <div>PCCCS504 Software Engineering & Project Management Lab</div>
      </div>
    </div>

    <!-- SLIDE 7: UI/UX Wireframes & Ergonomics -->
    <div class="slide" id="slide-7">
      <div class="slide-header">
        <div>
          <div class="category-badge">Frontend Engineering & Wireframes</div>
          <div class="slide-title">UI/UX Design, Ergonomics & Dual-Mode Workspaces</div>
        </div>
        <div class="slide-num">Slide 7 / 10</div>
      </div>
      <div class="slide-body">
        <div class="col col-half">
          <div class="container-box shade-blue" style="flex: 1;">
            <div class="container-title" style="color: var(--primary-dark);">1. Authentication & Onboarding Portal</div>
            <div class="item-list">
              <div class="item-row"><strong>Institutional Branding:</strong> Displays the official IEM laurel wreath crest and professional Google Sans typography.</div>
              <div class="item-row"><strong>Domain Validation:</strong> Enforces @gmail.com email domain constraints and client-side password strength checking.</div>
              <div class="item-row"><strong>Session Security:</strong> Stores authenticated session tokens securely, redirecting students to their dashboard upon login.</div>
            </div>
          </div>
          <div class="container-box shade-indigo" style="flex: 1;">
            <div class="container-title" style="color: #3730a3;">2. 4-Step Student Application Wizard</div>
            <div class="item-list">
              <div class="item-row"><strong>Guided Stepper:</strong> Step 1: Personal Details • Step 2: Academic Scores • Step 3: Document Upload • Step 4: Final Review.</div>
              <div class="item-row"><strong>Interactive Progress Bar:</strong> Visual step indicators guide students with real-time feedback on mandatory form fields.</div>
              <div class="item-row"><strong>Drag-and-Drop Upload:</strong> Intuitive PDF upload container with live size validation and file replacement preview.</div>
            </div>
          </div>
        </div>

        <div class="col col-half">
          <div class="container-box shade-green" style="flex: 1;">
            <div class="container-title" style="color: #065f46;">3. Student Application Status Dashboard</div>
            <div class="item-list">
              <div class="item-row"><strong>Live Timeline Tracker:</strong> Chronological progress stepper showing submission date, document verification, and final decision.</div>
              <div class="item-row"><strong>Application Summary Card:</strong> Displays unique Application ID (e.g. IEM-2026-0847), chosen course, and submitted scores.</div>
              <div class="item-row"><strong>Integrated Document Viewer:</strong> One-click preview and download of uploaded PDF marksheets directly from the browser.</div>
            </div>
          </div>
          <div class="container-box shade-amber" style="flex: 1;">
            <div class="container-title" style="color: #92400e;">4. Administrator Workspace & Dual View Modes</div>
            <div class="item-list">
              <div class="item-row"><strong>Real-time Metric Cards:</strong> Top KPI counters showing Total, Pending Review, Accepted, and Rejected application volumes.</div>
              <div class="item-row"><strong>Dual View Toggle (NFR-03):</strong> Switch smoothly between Compact Table Mode (fast triage) and Detailed Card Mode (in-depth inspection).</div>
              <div class="item-row"><strong>Live Search & Status Updater:</strong> Instant sub-second applicant search with modal dialog for status updates, remarks, and CSV export.</div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div>IEM Admission System • Team Nexus (P4)</div>
        <div>PCCCS504 Software Engineering & Project Management Lab</div>
      </div>
    </div>

    <!-- SLIDE 8: Software Verification & Quality Assurance -->
    <div class="slide" id="slide-8">
      <div class="slide-header">
        <div>
          <div class="category-badge">Software Verification & Test Strategy</div>
          <div class="slide-title">Testing Strategy, Basis Path Analysis & Quality Metrics</div>
        </div>
        <div class="slide-num">Slide 8 / 10</div>
      </div>
      <div class="slide-body">
        <div class="col col-half">
          <div class="container-box shade-blue" style="flex: 1.1;">
            <div class="container-title" style="color: var(--primary-dark);">White-Box Testing: McCabe's Basis Path Analysis</div>
            <div class="item-list">
              <div class="item-row"><strong>Target Logic Module:</strong> validate_status_transition(current, new, remarks) in backend/workflow.py.</div>
              <div class="item-row"><strong>Control Flow Graph (CFG):</strong> Nodes (N) = 20, Edges (E) = 27, Decision Predicates (P) = 9.</div>
              <div class="item-row"><strong>Cyclomatic Complexity:</strong> V(G) = E - N + 2P = 27 - 20 + 2(1) = 9 (or P + 1 = 10 independent paths).</div>
              <div class="item-row"><strong>100% Path Coverage:</strong> Codified all 10 linearly independent basis paths into automated unit test fixtures.</div>
            </div>
          </div>
          <div class="container-box shade-slate" style="flex: 1;">
            <div class="container-title" style="color: var(--text-dark);">Black-Box Test Design (BVA & ECP)</div>
            <div class="item-list">
              <div class="item-row"><strong>Equivalence Partitioning:</strong> Password complexity (min 8 chars, uppercase, special char) and phone format partitions.</div>
              <div class="item-row"><strong>Boundary Value Analysis:</strong> Percentage inputs tested at 0.0%, 100.0%, -0.1%, and 100.1%.</div>
              <div class="item-row"><strong>PDF File Size Thresholds:</strong> Tested 4.99MB (accepted), 5.00MB (accepted boundary), and 5.01MB (rejected).</div>
            </div>
          </div>
        </div>

        <div class="col col-half">
          <div class="container-box shade-green" style="flex: 1.1;">
            <div class="container-title" style="color: #065f46;">Automated Test Suite (backend/test_suite.py)</div>
            <div class="item-list">
              <div class="item-row"><strong>Test Execution Status:</strong> 16 out of 16 Automated Test Fixtures Passing (100% Pass Rate).</div>
              <div class="item-row"><strong>Multi-Database Parity:</strong> Executed identically against both SQLite3 and live MongoDB Atlas without regressions.</div>
              <div class="item-row"><strong>Sandwich Integration:</strong> Lightweight synthetic JWT tokens and mock PDF byte buffers used as stubs and drivers.</div>
              <div class="item-row"><strong>Zero Defect Escape:</strong> Automated regression suite executed on every code commit.</div>
            </div>
          </div>
          <div class="container-box shade-amber" style="flex: 1;">
            <div class="container-title" style="color: #92400e;">Testing Roles & Governance</div>
            <div class="item-list">
              <div class="item-row"><strong>Unit Testing:</strong> Executed by Sreejita Dey (Backend) and Debadrita Dutta (Test Lead).</div>
              <div class="item-row"><strong>Integration Testing:</strong> Managed by Susnata Maiti (Frontend/Integration) and Sreejita Dey (Backend).</div>
              <div class="item-row"><strong>System Testing:</strong> Managed by Debadrita Dutta; verified against all 20 FRs and 5 NFRs on Windows 11.</div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div>IEM Admission System • Team Nexus (P4)</div>
        <div>PCCCS504 Software Engineering & Project Management Lab</div>
      </div>
    </div>

    <!-- SLIDE 9: Cloud Deployment & Live Demonstration (Spacious Diagram) -->
    <div class="slide" id="slide-9">
      <div class="slide-header">
        <div>
          <div class="category-badge">Cloud Architecture & Edge Routing</div>
          <div class="slide-title">Cloud Deployment, Serverless Edge & Live Demonstration</div>
        </div>
        <div class="slide-num">Slide 9 / 10</div>
      </div>
      <div class="slide-body" style="flex-direction: column;">
        <div style="height: 195px; display: flex; align-items: center; justify-content: center; background: #ffffff; border: 1.5px solid var(--border-slate); border-radius: 12px; padding: 6px;">
          <img src="{dep_b64}" class="diagram-img" alt="Deployment Diagram">
        </div>
        <div style="display: flex; gap: 12px; flex: 1;">
          <div class="container-box col-3 shade-blue">
            <div class="container-title" style="color: var(--primary);">Live Production Deployment</div>
            <div class="item-list">
              <div class="item-row"><strong>Production URL:</strong> <a href="https://iem-admission-system-nexus-p4.vercel.app/" target="_blank" style="color: var(--primary); font-weight: 700; text-decoration: none;">iem-admission-system-nexus-p4.vercel.app</a></div>
              <div class="item-row"><strong>Global Edge Network:</strong> Fast static asset delivery with automatic SSL/TLS 1.3 termination.</div>
              <div class="item-row"><strong>Serverless ASGI Gateway:</strong> api/index.py bridges Vercel serverless functions directly into FastAPI.</div>
            </div>
          </div>
          <div class="container-box col-3 shade-green">
            <div class="container-title" style="color: #065f46;">Hybrid Execution & Portability</div>
            <div class="item-list">
              <div class="item-row"><strong>Dual Environment Parity:</strong> Operates identically locally via python run_server.py and on Vercel Edge Serverless.</div>
              <div class="item-row"><strong>Zero Code Mutation:</strong> Dynamic environment inspection detects host runtime and adjusts routes automatically.</div>
              <div class="item-row"><strong>Ephemeral File Handling:</strong> Uses /tmp on serverless instances to process uploads without disk lockups.</div>
            </div>
          </div>
          <div class="container-box col-3 shade-amber">
            <div class="container-title" style="color: #92400e;">Fault Isolation & Resilience</div>
            <div class="item-list">
              <div class="item-row"><strong>MongoDB Atlas Connectivity:</strong> Connects to cloud replica set; auto-injects public DNS to bypass SRV query failures.</div>
              <div class="item-row"><strong>Offline Graceful Fallback:</strong> If campus network isolates cloud access, system safely stores data in local SQLite database.</div>
              <div class="item-row"><strong>Zero Data Loss:</strong> Submissions and audit logs remain intact across all failure modes.</div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div>IEM Admission System • Team Nexus (P4)</div>
        <div>PCCCS504 Software Engineering & Project Management Lab</div>
      </div>
    </div>

    <!-- SLIDE 10: Milestones, Conclusion & Roadmap -->
    <div class="slide" id="slide-10">
      <div class="slide-header">
        <div>
          <div class="category-badge">Project Evaluation & Next Steps</div>
          <div class="slide-title">Project Milestones, Value Delivered & Future Roadmap</div>
        </div>
        <div class="slide-num">Slide 10 / 10</div>
      </div>
      <div class="slide-body" style="flex-direction: column;">
        <div class="container-box shade-slate" style="padding: 12px 18px;">
          <div style="font-size: 1.05rem; font-weight: 700; color: var(--primary-dark); margin-bottom: 4px;">20-Day Milestone Execution Schedule (100% Completed on Schedule)</div>
          <div class="item-list">
            <div class="item-row"><strong>Days 1–3 (Planning):</strong> Requirements gathering, Project Charter sign-off, SRS & HLD drafting, UML modeling.</div>
            <div class="item-row"><strong>Days 4–10 (Frontend):</strong> Figma wireframe alignment, responsive UI development, 4-step wizard form building.</div>
            <div class="item-row"><strong>Days 11–15 (Backend & DB):</strong> FastAPI endpoints, PBKDF2 hashing, dual-engine DB abstraction, PDF upload handling.</div>
            <div class="item-row"><strong>Days 16–18 (Testing & QA):</strong> End-to-end integration, Basis Path analysis (10 paths), 16 automated tests execution.</div>
            <div class="item-row"><strong>Days 19–20 (Delivery):</strong> Final documentation, user acceptance testing on Windows 11, and Vercel cloud deployment.</div>
          </div>
        </div>

        <div style="display: flex; gap: 12px; flex: 1;">
          <div class="container-box col-half shade-green">
            <div class="container-title" style="color: #065f46;">Key Achievements & Value Delivered</div>
            <div class="item-list">
              <div class="item-row"><strong>Academic Excellence:</strong> Engineered a robust, production-grade admissions system fulfilling all 20 FRs and 5 NFRs.</div>
              <div class="item-row"><strong>Fault-Tolerant Persistence:</strong> Novel dual-engine persistence layer eliminates downtime risks from campus DNS outages.</div>
              <div class="item-row"><strong>Rigorous Quality Assurance:</strong> 100% pass rate across automated regression suite with complete McCabe basis path coverage.</div>
              <div class="item-row"><strong>Stakeholder Alignment:</strong> Delivered dedicated workspaces tailored to Students, Admins, and Executive Directors.</div>
            </div>
          </div>

          <div class="container-box col-half shade-blue">
            <div class="container-title" style="color: var(--primary-dark);">Future Roadmap & Technological Extensions</div>
            <div class="item-list">
              <div class="item-row"><strong>Online Payment Gateway:</strong> Integrate Razorpay/Stripe API for automated admission fee processing with instant digital receipts.</div>
              <div class="item-row"><strong>Multichannel Alerts:</strong> Automated SMS, WhatsApp, and Email triggers for real-time application milestone notifications.</div>
              <div class="item-row"><strong>AI Document Verification:</strong> Deploy Vision OCR microservices to automatically parse and verify Class 10/12 marks from marksheets.</div>
              <div class="item-row"><strong>Enrolment Analytics:</strong> Predictive enrolment yield modeling for academic department capacity planning.</div>
            </div>
          </div>
        </div>

        <div class="container-box shade-indigo" style="padding: 10px 18px; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <div style="font-size: 1.25rem; font-weight: 700; color: var(--primary-dark);">Thank You! Questions & Discussion</div>
          <div style="font-size: 0.88rem; color: #475569; margin-top: 2px;">Team Nexus (P4) • Susnata Maiti | Sreejita Dey | Swapnil Ghosh | Debadrita Dutta</div>
        </div>
      </div>
      <div class="slide-footer">
        <div>IEM Admission System • Team Nexus (P4)</div>
        <div>PCCCS504 Software Engineering & Project Management Lab</div>
      </div>
    </div>

  </div>

  <!-- Navigation Controls -->
  <div class="controls">
    <button class="btn" id="prevBtn" onclick="prevSlide()">◀ Previous</button>
    <div class="indicator" id="slideIndicator">Slide 1 / 10</div>
    <button class="btn" id="nextBtn" onclick="nextSlide()">Next ▶</button>
    <button class="btn" id="fsBtn" onclick="toggleFullScreen()">⛶ Fullscreen</button>
  </div>

  <script>
    let currentSlide = 1;
    const totalSlides = 10;

    function showSlide(num) {{
      if (num < 1) num = 1;
      if (num > totalSlides) num = totalSlides;
      currentSlide = num;

      for (let i = 1; i <= totalSlides; i++) {{
        const slide = document.getElementById('slide-' + i);
        if (slide) {{
          slide.classList.remove('active');
          if (i === currentSlide) {{
            slide.classList.add('active');
          }}
        }}
      }}

      document.getElementById('slideIndicator').innerText = `Slide ${{currentSlide}} / ${{totalSlides}}`;
      document.getElementById('prevBtn').disabled = (currentSlide === 1);
      document.getElementById('nextBtn').disabled = (currentSlide === totalSlides);
    }}

    function prevSlide() {{
      if (currentSlide > 1) showSlide(currentSlide - 1);
    }}

    function nextSlide() {{
      if (currentSlide < totalSlides) showSlide(currentSlide + 1);
    }}

    function toggleFullScreen() {{
      const elem = document.getElementById('deckContainer');
      if (!document.fullscreenElement) {{
        elem.requestFullscreen().catch(err => {{
          alert(`Error attempting to enable fullscreen: ${{err.message}}`);
        }});
      }} else {{
        document.exitFullscreen();
      }}
    }}

    // Keyboard Navigation
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        nextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'Backspace' || e.key === 'PageUp') {{
        prevSlide();
      }} else if (e.key === 'Home') {{
        showSlide(1);
      }} else if (e.key === 'End') {{
        showSlide(totalSlides);
      }}
    }});

    // Initialize
    showSlide(1);
  </script>
</body>
</html>
"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML presentation successfully built at: {out_path}")

if __name__ == "__main__":
    docs_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(docs_dir)
    build_html_presentation(os.path.join(docs_dir, "presentation.html"))
    build_html_presentation(os.path.join(root_dir, "presentation.html"))
