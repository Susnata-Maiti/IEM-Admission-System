import os
import tempfile
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Enhanced Typography & Font Settings
font_family = 'DejaVu Sans'

def generate_state_machine_graphic(out_path):
    fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    def draw_state(x, y, w, h, title, subtitle, bg, border):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.6,rounding_size=1.5",
            facecolor=bg, edgecolor=border, linewidth=1.8, zorder=3
        )
        ax.add_patch(box)
        cx = x + w / 2.0
        ax.text(cx, y + h * 0.64, title, ha='center', va='center',
                fontsize=11.5, fontweight='bold', color="#0f172a", fontfamily=font_family, zorder=4)
        ax.text(cx, y + h * 0.28, subtitle, ha='center', va='center',
                fontsize=9.2, color="#334155", fontfamily=font_family, zorder=4)

    # 5 Key States (Light-shaded backgrounds)
    draw_state(3, 27, 19, 16, "Draft", "Initial Application Form", "#f1f5f9", "#475569")
    draw_state(34, 27, 23, 16, "Submitted", "Form Locked & Immutable", "#eff6ff", "#2563eb")
    draw_state(70, 27, 27, 16, "Under Review", "Faculty Triage & Verification", "#fefce8", "#ca8a04")
    draw_state(70, 3, 27, 16, "Accepted", "Admission Granted (Terminal)", "#ecfdf5", "#059669")
    draw_state(34, 3, 23, 16, "Rejected", "Denied w/ Remarks (Terminal)", "#fef2f2", "#dc2626")

    # Arrows with generous gaps & readable pill badges
    # Draft -> Submitted
    ax.annotate("", xy=(33.5, 35), xytext=(22.5, 35),
                arrowprops=dict(arrowstyle="-|>", color="#1e293b", lw=2.0, mutation_scale=15), zorder=2)
    ax.text(28, 39.5, "Final Submit", ha='center', va='center', fontsize=8.8, fontweight='bold', color="#1d4ed8",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#93c5fd", lw=1.0, zorder=5))

    # Submitted -> Under Review
    ax.annotate("", xy=(69.5, 35), xytext=(57.5, 35),
                arrowprops=dict(arrowstyle="-|>", color="#1e293b", lw=2.0, mutation_scale=15), zorder=2)
    ax.text(63.5, 39.5, "Start Triage", ha='center', va='center', fontsize=8.8, fontweight='bold', color="#1d4ed8",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#93c5fd", lw=1.0, zorder=5))

    # Submitted -> Rejected (Direct Rejection with remarks)
    ax.annotate("", xy=(45.5, 19.5), xytext=(45.5, 26.5),
                arrowprops=dict(arrowstyle="-|>", color="#dc2626", lw=2.0, mutation_scale=15), zorder=2)
    ax.text(50.0, 23.0, "Reject w/ Remarks", ha='left', va='center', fontsize=8.5, fontweight='bold', color="#b91c1c",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#fca5a5", lw=1.0, zorder=5))

    # Under Review -> Accepted
    ax.annotate("", xy=(83.5, 19.5), xytext=(83.5, 26.5),
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=2.0, mutation_scale=15), zorder=2)
    ax.text(88.0, 23.0, "Approve", ha='left', va='center', fontsize=8.8, fontweight='bold', color="#047857",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#86efac", lw=1.0, zorder=5))

    # Under Review -> Rejected
    ax.annotate("", xy=(57.5, 11), xytext=(69.5, 27),
                arrowprops=dict(arrowstyle="-|>", color="#dc2626", lw=1.8, ls="--", mutation_scale=14), zorder=2)
    ax.text(61.5, 17.5, "Reject w/ Remarks", ha='center', va='center', fontsize=8.2, fontweight='bold', color="#b91c1c",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#fca5a5", lw=1.0, zorder=5))

    plt.tight_layout()
    plt.savefig(out_path, format="png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"State machine diagram saved to {out_path}")

def generate_dfd_graphic(out_path):
    fig, ax = plt.subplots(figsize=(9.5, 4.0), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    def draw_entity(x, y, w, h, title, sub, bg="#f0fdf4", border="#16a34a"):
        box = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="square,pad=0.4",
            facecolor=bg, edgecolor=border, linewidth=1.8, zorder=3
        )
        ax.add_patch(box)
        ax.text(x + w/2, y + h*0.62, title, ha='center', va='center',
                fontsize=10.0, fontweight='bold', color="#0f172a", fontfamily=font_family, zorder=4)
        ax.text(x + w/2, y + h*0.30, sub, ha='center', va='center',
                fontsize=8.5, color="#334155", fontfamily=font_family, zorder=4)

    def draw_proc(x, y, w, h, num, text, bg="#eff6ff", border="#2563eb"):
        box = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.5",
            facecolor=bg, edgecolor=border, linewidth=1.8, zorder=3
        )
        ax.add_patch(box)
        ax.text(x + w/2, y + h*0.68, num, ha='center', va='center',
                fontsize=9.8, fontweight='bold', color="#1d4ed8", fontfamily=font_family, zorder=4)
        ax.text(x + w/2, y + h*0.32, text, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color="#0f172a", fontfamily=font_family, zorder=4)

    def draw_store(x, y, w, h, id_str, name):
        box = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="square,pad=0.4",
            facecolor="#fefce8", edgecolor="#ca8a04", linewidth=1.6, zorder=3
        )
        ax.add_patch(box)
        ax.text(x + w/2, y + h*0.65, id_str, ha='center', va='center',
                fontsize=9.2, fontweight='bold', color="#854d0e", fontfamily=font_family, zorder=4)
        ax.text(x + w/2, y + h*0.30, name, ha='center', va='center',
                fontsize=8.8, fontweight='bold', color="#0f172a", fontfamily=font_family, zorder=4)

    # Entities
    draw_entity(2, 28, 17, 18, "Student", "Applicant", bg="#f0fdf4", border="#15803d")
    draw_entity(81, 28, 17, 18, "Admin /", "Director", bg="#fdf2f8", border="#be185d")

    # 5 Processes
    draw_proc(22, 30, 17, 15, "1.0 Auth", "Login & JWT")
    draw_proc(42, 30, 17, 15, "2.0 Details", "Form Wizard")
    draw_proc(62, 30, 17, 15, "3.0 Upload", "PDF Stream")
    draw_proc(22, 5, 27, 16, "4.0 Submission", "Form Lock & Timestamp")
    draw_proc(52, 5, 27, 16, "5.0 Status Mgmt", "Review, Remarks & CSV")

    # Data Stores
    draw_store(2, 5, 17, 16, "D1: App Data", "Users & Records")
    draw_store(81, 5, 17, 16, "D2: Files", "PDF Storage")

    # Connectors
    ax.annotate("", xy=(41.5, 37.5), xytext=(39.2, 37.5), arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.8), zorder=2)
    ax.annotate("", xy=(61.5, 37.5), xytext=(59.2, 37.5), arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.8), zorder=2)
    ax.annotate("", xy=(21.5, 37.5), xytext=(19.2, 37.5), arrowprops=dict(arrowstyle="-|>", color="#15803d", lw=1.8), zorder=2)
    ax.annotate("", xy=(80.8, 37.5), xytext=(79.2, 37.5), arrowprops=dict(arrowstyle="<|-", color="#be185d", lw=1.8), zorder=2)

    ax.annotate("", xy=(19.2, 13), xytext=(21.8, 13), arrowprops=dict(arrowstyle="-|>", color="#ca8a04", lw=1.6), zorder=2)
    ax.annotate("", xy=(80.8, 13), xytext=(79.2, 13), arrowprops=dict(arrowstyle="-|>", color="#ca8a04", lw=1.6), zorder=2)

    plt.tight_layout()
    plt.savefig(out_path, format="png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"DFD diagram saved to {out_path}")

def generate_deployment_graphic(out_path):
    # Expanded Canvas to give ample horizontal gaps between nodes (No compression, no overlap)
    fig, ax = plt.subplots(figsize=(10.5, 3.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    def draw_node(x, y, w, h, title, sub, bg, border):
        box = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.7,rounding_size=1.6",
            facecolor=bg, edgecolor=border, linewidth=1.8, zorder=3
        )
        ax.add_patch(box)
        # Larger fonts
        ax.text(x + w/2, y + h*0.66, title, ha='center', va='center',
                fontsize=11.2, fontweight='bold', color="#0f172a", fontfamily=font_family, zorder=4)
        ax.text(x + w/2, y + h*0.30, sub, ha='center', va='center',
                fontsize=8.8, color="#334155", fontfamily=font_family, zorder=4)

    # 4 Nodes with GENEROUS horizontal spacing (Width 17.5 units, Gaps 9.0 units)
    # Node 1: 3 to 20.5 (w=17.5)
    # Gap 1: 20.5 to 29.5 (gap=9.0)
    # Node 2: 29.5 to 47.0 (w=17.5)
    # Gap 2: 47.0 to 56.0 (gap=9.0)
    # Node 3: 56.0 to 73.5 (w=17.5)
    # Gap 3: 73.5 to 82.5 (gap=9.0)
    # Node 4: 82.5 to 100.0 (w=17.5) -> adjust slightly to 81.5 to 98.5
    draw_node(2.0, 10, 18.0, 28, "Client Tier", "Chrome / Edge (Win11)\nResponsive SPA", "#f0fdf4", "#059669")
    draw_node(28.0, 10, 19.5, 28, "Vercel Edge CDN", "Global Anycast Edge\nHTTPS / TLS 1.3 Term", "#eff6ff", "#0284c7")
    draw_node(55.5, 10, 19.5, 28, "Serverless Python", "FastAPI ASGI Engine\napi/index.py Handler", "#eef2ff", "#4f46e5")
    draw_node(82.5, 10, 16.0, 28, "Data Tier", "MongoDB Atlas Cloud\n+ SQLite3 Failover", "#fefce8", "#d97706")

    # Connectors at y=24, with Pill Badges at y=32 (completely isolated from node borders)
    # Arrow 1: Client -> Vercel Edge (Gap is from 20.0 to 28.0 = 8.0 units)
    ax.annotate("", xy=(27.5, 24), xytext=(20.5, 24),
                arrowprops=dict(arrowstyle="<|-|>", color="#1e293b", lw=2.0, mutation_scale=14), zorder=2)
    ax.text(24.0, 31.0, "HTTPS / JSON", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#0284c7",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#bae6fd", lw=1.0, zorder=5))

    # Arrow 2: Vercel Edge -> Serverless Python (Gap is from 47.5 to 55.5 = 8.0 units)
    ax.annotate("", xy=(55.0, 24), xytext=(48.0, 24),
                arrowprops=dict(arrowstyle="<|-|>", color="#1e293b", lw=2.0, mutation_scale=14), zorder=2)
    ax.text(51.5, 31.0, "ASGI Gateway", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#4f46e5",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#c7d2fe", lw=1.0, zorder=5))

    # Arrow 3: Serverless Python -> Data Tier (Gap is from 75.0 to 82.5 = 7.5 units)
    ax.annotate("", xy=(82.0, 24), xytext=(75.5, 24),
                arrowprops=dict(arrowstyle="<|-|>", color="#1e293b", lw=2.0, mutation_scale=14), zorder=2)
    ax.text(78.8, 31.0, "TLS / pymongo", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#d97706",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#fde68a", lw=1.0, zorder=5))

    plt.tight_layout()
    plt.savefig(out_path, format="png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Enhanced deployment diagram saved to {out_path}")

if __name__ == "__main__":
    docs_dir = os.path.dirname(os.path.abspath(__file__))
    generate_state_machine_graphic(os.path.join(docs_dir, "slide_state_machine.png"))
    generate_dfd_graphic(os.path.join(docs_dir, "slide_dfd_diagram.png"))
    generate_deployment_graphic(os.path.join(docs_dir, "slide_deployment_diagram.png"))
