"""
Diagnostic utility to verify PostgreSQL (Neon) or SQLite database connectivity for Glow & Care.
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
from django.conf import settings

def check_connection():
    db_config = settings.DATABASES['default']
    engine = db_config.get('ENGINE', '')
    name = db_config.get('NAME', '')
    host = db_config.get('HOST', 'localhost')
    port = db_config.get('PORT', '')

    print("=" * 60)
    print(" GLOW & CARE - DATABASE CONNECTIVITY CHECK")
    print("=" * 60)
    print(f"[*] Engine   : {engine}")
    print(f"[*] Database : {name}")
    if host:
        print(f"[*] Host     : {host}")
    if port:
        print(f"[*] Port     : {port}")

    database_url = os.getenv('DATABASE_URL', '').strip()
    if database_url:
        # Mask password in DATABASE_URL for display
        import re
        masked_url = re.sub(r':([^@]+)@', ':****@', database_url)
        print(f"[*] Source   : DATABASE_URL ({masked_url})")
    else:
        print("[*] Source   : Local SQLite fallback (DATABASE_URL not set)")

    print("\n[*] Attempting database connection...")
    try:
        connection.ensure_connection()
        with connection.cursor() as cursor:
            if 'postgresql' in engine:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                print(f"[+] Connection SUCCESSFUL to PostgreSQL!")
                print(f"    Version: {version[:80]}...")
            elif 'sqlite' in engine:
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()[0]
                print(f"[+] Connection SUCCESSFUL to SQLite!")
                print(f"    Version: {version}")
            else:
                cursor.execute("SELECT 1;")
                print(f"[+] Connection SUCCESSFUL to database!")

        return True
    except Exception as e:
        print(f"[-] Connection FAILED: {e}")
        return False

if __name__ == '__main__':
    success = check_connection()
    sys.exit(0 if success else 1)
