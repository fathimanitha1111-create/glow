"""
Safe Diagnostic Utility to verify Database Connectivity for Glow & Care Skincare.
Prints only the database vendor and connection success/failure.
Never displays database URLs, passwords, or credentials.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple.settings')

import django
django.setup()

from django.db import connection

def check_connection():
    vendor = connection.vendor
    has_db_url = bool(os.getenv('DATABASE_URL', '').strip())

    print("=" * 60)
    print(" GLOW & CARE - DATABASE CONNECTIVITY CHECK")
    print("=" * 60)
    print(f"[*] Configured Vendor : {vendor}")
    print(f"[*] Configuration     : {'DATABASE_URL' if has_db_url else 'Local SQLite fallback'}")
    print("\n[*] Testing connection to database...")

    try:
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()

        print(f"[+] SUCCESS: Successfully connected to {vendor} database!")
        return True
    except Exception as e:
        # Sanitize exception message to ensure no connection URLs or passwords leak
        err_msg = str(e)
        import re
        sanitized = re.sub(r'//[^@]+@', '//***:***@', err_msg)
        print(f"[-] FAILED: Could not connect to {vendor} database.")
        print(f"    Details: {sanitized}")
        return False

if __name__ == '__main__':
    success = check_connection()
    sys.exit(0 if success else 1)
