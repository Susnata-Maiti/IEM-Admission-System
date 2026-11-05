"""
One-click runner for the IEM Admission System
Starts FastAPI server serving both REST API and Interactive Web Frontend on Windows 11.
"""

import sys
import os
import webbrowser

# Add backend directory to sys.path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
sys.path.insert(0, backend_dir)

from database import init_db
import uvicorn

if __name__ == "__main__":
    print("=" * 65)
    print("  INSTITUTE OF ENGINEERING & MANAGEMENT (IEM), SALT LAKE")
    print("  IEM Admission System - Nexus P4 (Susnata, Sreejita, Swapnil, Debadrita)")
    print("=" * 65)
    print("Initializing Database and seed data...")
    init_db()
    
    port = 8000
    host = "127.0.0.1"
    url = f"http://{host}:{port}"
    print(f"\n[+] Server running successfully at: {url}")
    print("=================================================================")
    print("  Default Demo Credentials for in-lab presentation:")
    print("  - Student:  priya.sharma@example.com   /  Student@2026!")
    print("  - Admin:    admin@iem.edu.in           /  Admin@2026!")
    print("  - Director: director@iem.edu.in        /  Director@2026!")
    print("=================================================================\n")

    try:
        # Automatically launch default browser (Edge/Chrome on Windows 11)
        webbrowser.open(url)
    except Exception:
        pass

    uvicorn.run("app:app", host=host, port=port, reload=False, app_dir=backend_dir)
