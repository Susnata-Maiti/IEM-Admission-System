import os
import tempfile
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_architecture_graphic(out_path):
    # Dimensions: 8.2 x 5.4 inches.
    # When scaled to 487pt (6.76 in) in ReportLab: scale = 6.76 / 8.2 = 0.824
    # Font sizes:
    # 13pt -> 10.7pt in PDF
    # 11pt -> 9.1pt in PDF
    # 9.8pt -> 8.1pt in PDF
    # 9.2pt -> 7.6pt in PDF
    # This guarantees large, crisp, perfectly readable text without any tofu or clipping!
    fig, ax = plt.subplots(figsize=(8.4, 5.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    font_main = 'Segoe UI'

    # Outer border container
    outer_box = patches.FancyBboxPatch(
        (0.6, 0.6), 98.8, 98.8,
        boxstyle="round,pad=0.4,rounding_size=1.2",
        facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.2, zorder=0
    )
    ax.add_patch(outer_box)

    # =========================================================================
    # 1. TIER 1: ANGULAR 17+ CLIENT SPA
    # =========================================================================
    t1_box = patches.FancyBboxPatch(
        (2.8, 76.2), 94.4, 21.0,
        boxstyle="round,pad=0.5,rounding_size=1.2",
        facecolor="#eff6ff", edgecolor="#2563eb", linewidth=1.8, zorder=2
    )
    ax.add_patch(t1_box)

    # Title & Subtitle
    ax.text(4.8, 93.5, "CLIENT TIER: Angular 17+ Single Page Application (Port 4200)",
            fontsize=11.8, fontweight='bold', color="#1e3a8a", fontfamily=font_main, zorder=4)
    ax.text(4.8, 90.2, "Directory: client/src/app/ • Reactive Component Tree & Signal Architecture",
            fontsize=9.2, fontweight='bold', color="#3b82f6", fontfamily=font_main, zorder=4)

    # Sub-card Left: Reactive UI
    c_ang_l = patches.FancyBboxPatch(
        (4.8, 78.0), 43.5, 10.5,
        boxstyle="round,pad=0.3,rounding_size=0.8",
        facecolor="#ffffff", edgecolor="#bfdbfe", linewidth=1.0, zorder=3
    )
    ax.add_patch(c_ang_l)
    ax.text(6.2, 85.8, "Reactive UI & Components",
            fontsize=9.6, fontweight='bold', color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(6.2, 82.8, "• Standalone Components & Two-way Binding",
            fontsize=8.8, color="#334155", fontfamily=font_main, zorder=4)
    ax.text(6.2, 79.8, "• Role-Gated Dynamic Views (Student/Admin)",
            fontsize=8.8, color="#334155", fontfamily=font_main, zorder=4)

    # Sub-card Right: RxJS Service
    c_ang_r = patches.FancyBboxPatch(
        (51.7, 78.0), 43.5, 10.5,
        boxstyle="round,pad=0.3,rounding_size=0.8",
        facecolor="#ffffff", edgecolor="#bfdbfe", linewidth=1.0, zorder=3
    )
    ax.add_patch(c_ang_r)
    ax.text(53.1, 85.8, "AdmissionService & Network Layer",
            fontsize=9.6, fontweight='bold', color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(53.1, 82.8, "• RxJS Observables with HttpClient Streams",
            fontsize=8.8, color="#334155", fontfamily=font_main, zorder=4)
    ax.text(53.1, 79.8, "• Injects JWT Bearer Header & FormData for PDF",
            fontsize=8.8, color="#334155", fontfamily=font_main, zorder=4)

    # =========================================================================
    # CONNECTOR 1: Client -> Server
    # =========================================================================
    ax.annotate("", xy=(50.0, 68.2), xytext=(50.0, 76.0),
                arrowprops=dict(arrowstyle="-|>", color="#1d4ed8", lw=2.2, mutation_scale=15), zorder=5)

    pill1 = patches.FancyBboxPatch(
        (16.5, 70.3), 67.0, 3.8,
        boxstyle="round,pad=0.2,rounding_size=0.7",
        facecolor="#ffffff", edgecolor="#2563eb", linewidth=1.2, zorder=6
    )
    ax.add_patch(pill1)
    ax.text(50.0, 72.2, "Asynchronous HTTP REST (JSON / Multipart FormData + Bearer JWT Token)",
            ha='center', va='center', fontsize=9.0, fontweight='bold', color="#1e40af", fontfamily=font_main, zorder=7)

    # =========================================================================
    # 2. TIER 2: NODE.JS RUNTIME + EXPRESS.JS SERVER
    # =========================================================================
    t2_box = patches.FancyBboxPatch(
        (2.8, 33.2), 94.4, 34.6,
        boxstyle="round,pad=0.5,rounding_size=1.2",
        facecolor="#f1f5f9", edgecolor="#0f172a", linewidth=1.8, zorder=2
    )
    ax.add_patch(t2_box)

    ax.text(4.8, 64.2, "APPLICATION TIER: Node.js Runtime + Express.js API Server (Port 5000)",
            fontsize=11.8, fontweight='bold', color="#0f172a", fontfamily=font_main, zorder=4)
    ax.text(4.8, 61.2, "Single-Threaded Event Loop Engine • Non-Blocking Asynchronous I/O Pipeline",
            fontsize=9.2, fontweight='bold', color="#475569", fontfamily=font_main, zorder=4)

    # Sub-card Left: Sequential Middleware Pipeline
    c_exp_l = patches.FancyBboxPatch(
        (4.8, 35.0), 43.5, 24.5,
        boxstyle="round,pad=0.3,rounding_size=0.8",
        facecolor="#ffffff", edgecolor="#94a3b8", linewidth=1.0, zorder=3
    )
    ax.add_patch(c_exp_l)
    ax.text(6.2, 56.6, "Sequential Middleware Pipeline",
            fontsize=10.0, fontweight='bold', color="#1e3a8a", fontfamily=font_main, zorder=4)
    ax.text(6.2, 53.6, "1. cors(): Origin whitelist (client:4200)",
            fontsize=8.6, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(6.2, 49.8, "2. express.json(): JSON body parser (req.body)",
            fontsize=8.6, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(6.2, 46.0, "3. authenticateToken: JWT verification guard",
            fontsize=8.6, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(6.2, 42.2, "4. requireRole([roles]): Server-side RBAC check",
            fontsize=8.6, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(6.2, 38.4, "5. multer: 5MB size limit & PDF MIME validator",
            fontsize=8.6, color="#1e293b", fontfamily=font_main, zorder=4)

    # Sub-card Right: Business Logic & State Machine
    c_exp_r = patches.FancyBboxPatch(
        (51.7, 35.0), 43.5, 24.5,
        boxstyle="round,pad=0.3,rounding_size=0.8",
        facecolor="#ffffff", edgecolor="#94a3b8", linewidth=1.0, zorder=3
    )
    ax.add_patch(c_exp_r)
    ax.text(53.1, 56.6, "Business Controllers & Validation Logic",
            fontsize=10.0, fontweight='bold', color="#1e3a8a", fontfamily=font_main, zorder=4)
    ax.text(53.1, 53.6, "• State Machine: Legal status transitions (V(G)=10)",
            fontsize=8.6, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(53.1, 49.8, "• Audit Trail: Mutation logger with timestamp/actor",
            fontsize=8.6, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(53.1, 46.0, "• Aggregation Engine: Native $match & $group metrics",
            fontsize=8.6, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(53.1, 42.2, "• Security Controller: bcrypt (10 rounds) & JWT signer",
            fontsize=8.6, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(53.1, 38.4, "• Mongoose ODM Interface: Strict schema queries",
            fontsize=8.6, color="#1e293b", fontfamily=font_main, zorder=4)

    # =========================================================================
    # CONNECTOR 2: Dual Persistence Split
    # =========================================================================
    # Branch A: Down to Filesystem
    ax.annotate("", xy=(26.5, 24.2), xytext=(26.5, 33.0),
                arrowprops=dict(arrowstyle="-|>", color="#d97706", lw=2.2, mutation_scale=15), zorder=5)

    pill2a = patches.FancyBboxPatch(
        (9.5, 27.0), 34.0, 3.6,
        boxstyle="round,pad=0.2,rounding_size=0.7",
        facecolor="#ffffff", edgecolor="#f59e0b", linewidth=1.2, zorder=6
    )
    ax.add_patch(pill2a)
    ax.text(26.5, 28.8, "Multer Raw Disk Binary Stream",
            ha='center', va='center', fontsize=8.6, fontweight='bold', color="#b45309", fontfamily=font_main, zorder=7)

    # Branch B: Down to MongoDB
    ax.annotate("", xy=(73.5, 24.2), xytext=(73.5, 33.0),
                arrowprops=dict(arrowstyle="-|>", color="#16a34a", lw=2.2, mutation_scale=15), zorder=5)

    pill2b = patches.FancyBboxPatch(
        (56.5, 27.0), 34.0, 3.6,
        boxstyle="round,pad=0.2,rounding_size=0.7",
        facecolor="#ffffff", edgecolor="#22c55e", linewidth=1.2, zorder=6
    )
    ax.add_patch(pill2b)
    ax.text(73.5, 28.8, "Mongoose ODM Structured BSON CRUD",
            ha='center', va='center', fontsize=8.6, fontweight='bold', color="#15803d", fontfamily=font_main, zorder=7)

    # =========================================================================
    # 3. TIER 3: DUAL STORAGE SUBSYSTEMS (DECOUPLED DESIGN)
    # =========================================================================
    # 3A. File System Box (Left)
    t3a_box = patches.FancyBboxPatch(
        (2.8, 2.5), 45.5, 21.0,
        boxstyle="round,pad=0.5,rounding_size=1.2",
        facecolor="#fefce8", edgecolor="#ca8a04", linewidth=1.8, zorder=2
    )
    ax.add_patch(t3a_box)

    ax.text(4.8, 20.0, "STORAGE: Local File System (/uploads)",
            fontsize=10.8, fontweight='bold', color="#854d0e", fontfamily=font_main, zorder=4)
    ax.text(4.8, 17.2, "Decoupled Binary Storage Pattern (Raw Files)",
            fontsize=8.8, fontweight='bold', color="#a16207", fontfamily=font_main, zorder=4)
    ax.text(4.8, 14.0, "• Direct disk storage for 5MB PDF marksheets",
            fontsize=8.5, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(4.8, 11.2, "• Circumvents MongoDB 16MB document boundary",
            fontsize=8.5, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(4.8, 8.4, "• Prevents WiredTiger RAM buffer cache thrashing",
            fontsize=8.5, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(4.8, 5.6, "• Static route mount: express.static('uploads')",
            fontsize=8.5, color="#1e293b", fontfamily=font_main, zorder=4)

    # 3B. MongoDB Box (Right)
    t3b_box = patches.FancyBboxPatch(
        (51.7, 2.5), 45.5, 21.0,
        boxstyle="round,pad=0.5,rounding_size=1.2",
        facecolor="#f0fdf4", edgecolor="#16a34a", linewidth=1.8, zorder=2
    )
    ax.add_patch(t3b_box)

    ax.text(53.7, 20.0, "DATABASE: MongoDB Atlas / Local Engine",
            fontsize=10.8, fontweight='bold', color="#166534", fontfamily=font_main, zorder=4)
    ax.text(53.7, 17.2, "Mongoose ODM Document Models (Structured BSON)",
            fontsize=8.8, fontweight='bold', color="#15803d", fontfamily=font_main, zorder=4)
    ax.text(53.7, 14.0, "• users: Unique email index, salted bcrypt hashes",
            fontsize=8.5, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(53.7, 11.2, "• applications: Bio-data, marks bounded (0..100)",
            fontsize=8.5, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(53.7, 8.4, "• docReference: File metadata (size, path, mime)",
            fontsize=8.5, color="#1e293b", fontfamily=font_main, zorder=4)
    ax.text(53.7, 5.6, "• auditTrail[]: Embedded chronological log array",
            fontsize=8.5, color="#1e293b", fontfamily=font_main, zorder=4)

    plt.tight_layout()
    plt.savefig(out_path, format="png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Architecture graphic successfully generated at: {out_path}")

if __name__ == "__main__":
    target = os.path.join(os.path.dirname(__file__), "mean_architecture_overview.png")
    generate_architecture_graphic(target)
