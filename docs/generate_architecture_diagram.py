import os
import tempfile
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_architecture_diagram(output_image_path):
    # Dimensions suited for IEEE column width (approx 3.38 - 3.45 inches)
    # 7.2 x 8.0 inches at 300 DPI gives ultra-sharp 2160 x 2400 resolution
    fig, ax = plt.subplots(figsize=(7.2, 8.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette: Clean IEEE Engineering / ACM Publication Style
    c_client = "#f8fafc"       # Slate light
    c_app = "#eff6ff"          # Soft blue
    c_db_layer = "#fefce8"     # Soft amber
    c_storage = "#f0fdf4"      # Soft emerald / green
    c_primary = "#ecfdf5"      # Mint / emerald
    c_fallback = "#fff7ed"     # Orange / warm amber
    c_disk = "#f8fafc"         # Slate neutral
    
    text_dark = "#0f172a"      # High contrast slate 900
    text_sub = "#334155"       # Subtitle slate 700
    arrow_color = "#1e293b"    # Slate 800

    font_family = "Times New Roman"

    def draw_box(x, y, w, h, subtitle, title, bg_color="#ffffff", border_color="#1e293b", dashed=False):
        ls = "--" if dashed else "-"
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.6,rounding_size=1.5",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=1.4,
            linestyle=ls,
            zorder=3
        )
        ax.add_patch(box)
        
        cx = x + w / 2.0
        if subtitle:
            # Multi-line title & subtitle
            ax.text(cx, y + h * 0.68, title, ha='center', va='center',
                    fontsize=11.2, fontweight='bold', color=text_dark, fontfamily=font_family, zorder=4)
            ax.text(cx, y + h * 0.30, subtitle, ha='center', va='center',
                    fontsize=9.2, color=text_sub, fontfamily=font_family, zorder=4)
        else:
            ax.text(cx, y + h / 2.0, title, ha='center', va='center',
                    fontsize=10.5, fontweight='bold', color=text_dark, fontfamily=font_family, zorder=4)

    # -------------------------------------------------------------
    # 1. PRESENTATION TIER (x: 6 to 94, width: 88, center: 50)
    # -------------------------------------------------------------
    draw_box(
        6, 86.5, 88, 9.5,
        "Google Chrome / Microsoft Edge (Windows 11) • Responsive Single Page Application (SPA)",
        "Presentation Tier: Client Web Browser",
        bg_color=c_client, border_color="#0284c7"
    )

    # Arrow 1: Presentation -> Application Tier (at center x = 50)
    ax.annotate(
        "", xy=(50, 73.0), xytext=(50, 86.5),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.6, mutation_scale=14),
        zorder=2
    )
    # Centered Badge for Arrow 1
    ax.text(
        50, 79.75, "  HTTP / REST (JSON Payload + Bearer Token)  ",
        ha='center', va='center', fontsize=9.2, fontweight='bold',
        color="#0369a1", fontfamily=font_family,
        bbox=dict(boxstyle="round,pad=0.25,rounding_size=0.4", facecolor="#ffffff", edgecolor="#94a3b8", lw=0.9, zorder=5)
    )

    # -------------------------------------------------------------
    # 2. APPLICATION TIER (x: 6 to 94, width: 88, center: 50)
    # -------------------------------------------------------------
    draw_box(
        6, 61.5, 88, 11.5,
        "FastAPI ASGI Microservice • RBAC Middleware • Finite-State Machine Workflow Engine",
        "Application Tier: FastAPI Backend Server",
        bg_color=c_app, border_color="#2563eb"
    )

    # Arrow 2: Application Tier -> Database Abstraction Layer (at center x = 34)
    ax.annotate(
        "", xy=(34, 46.5), xytext=(34, 61.5),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.6, mutation_scale=14),
        zorder=2
    )
    ax.text(
        34, 54.0, "  Data Query / Transaction Sync  ",
        ha='center', va='center', fontsize=8.8, fontweight='bold',
        color="#1d4ed8", fontfamily=font_family,
        bbox=dict(boxstyle="round,pad=0.2,rounding_size=0.4", facecolor="#ffffff", edgecolor="#94a3b8", lw=0.9, zorder=5)
    )

    # Arrow 3: Application Tier -> Document Storage Handler (at center x = 80)
    ax.annotate(
        "", xy=(80, 46.5), xytext=(80, 61.5),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.6, mutation_scale=14),
        zorder=2
    )
    ax.text(
        80, 54.0, "  PDF Marksheet Upload (<5MB)  ",
        ha='center', va='center', fontsize=8.8, fontweight='bold',
        color="#334155", fontfamily=font_family,
        bbox=dict(boxstyle="round,pad=0.2,rounding_size=0.4", facecolor="#ffffff", edgecolor="#94a3b8", lw=0.9, zorder=5)
    )

    # -------------------------------------------------------------
    # 3. INTERMEDIATE SUBSYSTEMS (y: 33.0 to 46.5, height: 13.5)
    # Left: Database Abstraction (x: 6 to 62, width: 56, center: 34)
    # Right: Document Storage Handler (x: 66 to 94, width: 28, center: 80)
    # -------------------------------------------------------------
    draw_box(
        6, 33.0, 56, 13.5,
        "Intelligent Dual-Engine Router (backend/database.py)\npymongo[srv] with Auto DNS SRV Fallback & Health Probing",
        "Database Abstraction Layer",
        bg_color=c_db_layer, border_color="#d97706"
    )

    draw_box(
        66, 33.0, 28, 13.5,
        "Multipart Stream Parser\nMIME Type & Size Validator\nRelative Path DB Linking",
        "Document Storage Handler",
        bg_color=c_storage, border_color="#16a34a"
    )

    # Arrow 4: Database Abstraction -> MongoDB Atlas (at center x = 19)
    ax.annotate(
        "", xy=(19, 18.0), xytext=(19, 33.0),
        arrowprops=dict(arrowstyle="-|>", color="#15803d", lw=1.7, mutation_scale=14),
        zorder=2
    )
    ax.text(
        19, 25.5, "  [Primary Engine]  ",
        ha='center', va='center', fontsize=8.6, fontweight='bold',
        color="#15803d", fontfamily=font_family,
        bbox=dict(boxstyle="round,pad=0.2,rounding_size=0.4", facecolor="#ffffff", edgecolor="#86efac", lw=1.0, zorder=5)
    )

    # Arrow 5: Database Abstraction -> SQLite3 DB (at center x = 49)
    ax.annotate(
        "", xy=(49, 18.0), xytext=(49, 33.0),
        arrowprops=dict(arrowstyle="-|>", color="#c2410c", lw=1.7, ls="--", mutation_scale=14),
        zorder=2
    )
    ax.text(
        49, 25.5, "  [Failover Engine]  ",
        ha='center', va='center', fontsize=8.6, fontweight='bold',
        color="#c2410c", fontfamily=font_family,
        bbox=dict(boxstyle="round,pad=0.2,rounding_size=0.4", facecolor="#ffffff", edgecolor="#fdba74", lw=1.0, zorder=5)
    )

    # Arrow 6: Document Storage Handler -> Disk Storage (at center x = 80)
    ax.annotate(
        "", xy=(80, 18.0), xytext=(80, 33.0),
        arrowprops=dict(arrowstyle="-|>", color="#059669", lw=1.7, mutation_scale=14),
        zorder=2
    )
    ax.text(
        80, 25.5, "  [Local /tmp Write]  ",
        ha='center', va='center', fontsize=8.6, fontweight='bold',
        color="#047857", fontfamily=font_family,
        bbox=dict(boxstyle="round,pad=0.2,rounding_size=0.4", facecolor="#ffffff", edgecolor="#6ee7b7", lw=1.0, zorder=5)
    )

    # -------------------------------------------------------------
    # 4. PERSISTENCE & STORAGE TARGETS (y: 3.5 to 18.0, height: 14.5)
    # Left: MongoDB Atlas (x: 6 to 32, width: 26, center: 19)
    # Middle: SQLite3 Relational (x: 36 to 62, width: 26, center: 49)
    # Right: Physical Filesystem (x: 66 to 94, width: 28, center: 80)
    # -------------------------------------------------------------
    draw_box(
        6, 3.5, 26, 14.5,
        "Cloud Replica Set Cluster\nCollections: users, apps\nBSON Document Store",
        "MongoDB Atlas\n(Cloud NoSQL)",
        bg_color=c_primary, border_color="#16a34a"
    )

    draw_box(
        36, 3.5, 26, 14.5,
        "File: iem_admission.db\nRelational Schema\nZero-Dependency Backup",
        "SQLite3\n(Embedded ACID)",
        bg_color=c_fallback, border_color="#ea580c"
    )

    draw_box(
        66, 3.5, 28, 14.5,
        "Local Directory: /uploads\nServerless: /tmp (Ephemeral)\nStatic File Mount (/uploads)",
        "Document Storage Target\n(Physical Filesystem)",
        bg_color=c_disk, border_color="#059669"
    )

    # Visual Grouping Background for Persistence Tier
    bg_group = patches.FancyBboxPatch(
        (4, 1.8), 92, 47.0,
        boxstyle="round,pad=0.5,rounding_size=2.0",
        facecolor="#f8fafc",
        edgecolor="#cbd5e1",
        linewidth=1.0,
        linestyle=":",
        zorder=1
    )
    ax.add_patch(bg_group)
    ax.text(
        5, 47.2, "Persistence & Storage Subsystem Boundary",
        ha='left', va='bottom', fontsize=7.5, fontweight='bold', fontstyle='italic',
        color="#64748b", fontfamily=font_family, zorder=4
    )

    plt.tight_layout()
    plt.savefig(output_image_path, format="png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Diagram successfully generated at: {output_image_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig1_architecture.png")
    draw_architecture_diagram(out)
