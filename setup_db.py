"""
Database Initialization & Connection Verification Script for Glow & Care Skincare.
This script checks connection to your local MongoDB server (port 27017),
starts mongod if not already running, applies Django migrations,
and imports existing products/orders into MongoDB.
"""

import os
import sys
import socket
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', os.getenv('DB_NAME', 'simple_db'))

def is_mongo_running():
    try:
        s = socket.create_connection((MONGO_HOST, MONGO_PORT), timeout=2)
        s.close()
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def check_and_start_mongo():
    print("=" * 65)
    print("[*] GLOW & CARE - LOCAL MONGODB SETUP & CONNECTION CHECK")
    print("=" * 65)

    if is_mongo_running():
        print(f"[+] Connected to local MongoDB server on {MONGO_HOST}:{MONGO_PORT} successfully!")
        return True

    print(f"[!] MongoDB is not currently running on {MONGO_HOST}:{MONGO_PORT}.")

    # Check known local mongod locations
    mongod_candidates = [
        Path(r"C:\Users\LENOVO\mongodb\bin\mongod.exe"),
        Path(r"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe"),
        Path(r"C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe"),
        Path(r"C:\Program Files\MongoDB\Server\8.0\bin\mongod.exe"),
    ]

    found_mongod = None
    for cand in mongod_candidates:
        if cand.exists():
            found_mongod = cand
            break

    if not found_mongod:
        # Check PATH
        import shutil
        path_mongod = shutil.which("mongod")
        if path_mongod:
            found_mongod = Path(path_mongod)

    if found_mongod:
        print(f"[*] Found mongod at: {found_mongod}")
        data_dir = found_mongod.parent.parent / "data"
        if not data_dir.exists():
            data_dir = Path(r"C:\Users\LENOVO\mongodb\data")
        data_dir.mkdir(parents=True, exist_ok=True)

        print(f"[*] Starting local MongoDB server with dbpath: {data_dir}...")
        try:
            subprocess.Popen(
                [str(found_mongod), "--dbpath", str(data_dir), "--port", str(MONGO_PORT), "--bind_ip", "127.0.0.1"],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
            )
            import time
            time.sleep(3)
            if is_mongo_running():
                print(f"[+] MongoDB server started successfully on {MONGO_HOST}:{MONGO_PORT}!")
                return True
        except Exception as e:
            print(f"[-] Failed to start mongod automatically: {e}")

    print("\n[-] Please ensure your local MongoDB server is running:")
    print("    Command:")
    print(r'    & "C:\Users\LENOVO\mongodb\bin\mongod.exe" --dbpath "C:\Users\LENOVO\mongodb\data"')
    return False

if __name__ == '__main__':
    if check_and_start_mongo():
        print("\n[*] Applying database migrations to MongoDB...")
        migrate_res = subprocess.run([sys.executable, 'manage.py', 'migrate'])
        if migrate_res.returncode == 0:
            print("\n[+] Database migrations applied successfully to MongoDB!")

            print("\n[*] Importing / seeding skincare categories and products...")
            migrate_data = subprocess.run([sys.executable, 'migrate_mysql_to_mongodb.py'])
            if migrate_data.returncode == 0:
                print("\n[+] ALL SETUP COMPLETE! Your MongoDB-powered website is ready.")
                print("Run your server with:")
                print("   py manage.py runserver")
                print("Then open in your browser: http://127.0.0.1:8000/\n")
            else:
                print("\n[!] Migrations complete, but data import encountered an issue.")
        else:
            print("\n[!] Django migrate command encountered an issue.")
    else:
        sys.exit(1)
