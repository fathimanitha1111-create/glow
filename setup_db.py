"""
Database Initialization & Connection Verification Script for Glow & Care Skincare.
This script securely connects to your local MySQL 8.4 Server using .env credentials,
creates the database 'simple_db' if it does not exist, runs Django migrations,
and seeds the 12 gentle skincare products.
"""

import os
import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from dotenv import load_dotenv

# Load .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

DB_NAME = os.getenv('DB_NAME', 'simple_db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))

def check_and_create_db():
    print("=" * 65)
    print("[*] GLOW & CARE - MYSQL DATABASE SETUP & CONNECTION CHECK")
    print("=" * 65)

    if DB_PASSWORD == 'YOUR_MYSQL_PASSWORD_HERE':
        print("\n[!] ACTION REQUIRED: Set your local MySQL password.")
        print(f"1. Open the file: {BASE_DIR / '.env'}")
        print("2. Update the line:")
        print("   DB_PASSWORD=YOUR_MYSQL_PASSWORD_HERE")
        print("   with your actual local MySQL password (or leave empty if no password).")
        print("3. Save the file and re-run: py setup_db.py\n")
        return False

    try:
        import MySQLdb
    except ImportError:
        print("[-] Error: 'mysqlclient' (MySQLdb) is not installed in Python.")
        return False

    print(f"[*] Connecting to MySQL Server at {DB_HOST}:{DB_PORT} as user '{DB_USER}'...")
    try:
        # Connect to MySQL Server without specifying db name first
        conn = MySQLdb.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        print("[+] Connected to MySQL Server successfully!")

        # Create database simple_db if not exists
        sql = f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        cursor.execute(sql)
        print(f"[+] Database '{DB_NAME}' created or verified successfully!")
        
        cursor.close()
        conn.close()
        return True
    except MySQLdb.OperationalError as e:
        error_code, error_msg = e.args
        print(f"\n[-] MySQL Connection Error [{error_code}]: {error_msg}")
        if error_code == 1045:
            print(">>> Access denied: The username or password in '.env' does not match your MySQL Server.")
            print("    Please check your MySQL password and update DB_PASSWORD in .env.")
        elif error_code == 2003:
            print(">>> Can't connect: Is MySQL service running on your machine?")
        return False
    except Exception as e:
        print(f"\n[-] Unexpected error: {e}")
        return False

if __name__ == '__main__':
    success = check_and_create_db()
    if success:
        print("\n[*] Applying database migrations to simple_db...")
        migrate_res = subprocess.run([sys.executable, 'manage.py', 'migrate'])
        if migrate_res.returncode == 0:
            print("\n[+] Database migrations applied successfully!")
            
            print("\n[*] Seeding initial skincare categories and products...")
            seed_res = subprocess.run([sys.executable, 'seed_data.py'])
            if seed_res.returncode == 0:
                print("\n[+] ALL SETUP COMPLETE! Your full-stack website is ready.")
                print("Run your server with:")
                print("   py manage.py runserver")
                print("Then open in your browser: http://127.0.0.1:8000/\n")
            else:
                print("\n[!] Database created & migrated, but product seeding encountered an issue.")
        else:
            print("\n[!] Django migrate command encountered an issue. See details above.")
    else:
        sys.exit(1)
