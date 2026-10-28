import os
import json
from decimal import Decimal
from datetime import datetime, date
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

import pymysql
import pymysql.cursors

def backup_mysql():
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    port = int(os.getenv('DB_PORT', '3306'))
    db = os.getenv('DB_NAME', 'simple_db')

    print(f"[*] Connecting to MySQL ({host}:{port}, db={db})...")
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=db,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    def serialize_val(val):
        if isinstance(val, (Decimal, datetime, date)):
            return str(val)
        return val

    tables = ['simpleapp_category', 'simpleapp_product', 'auth_user', 'simpleapp_order', 'simpleapp_orderitem']
    data = {}
    for t in tables:
        cursor.execute(f"SELECT * FROM `{t}`")
        rows = cursor.fetchall()
        serialized_rows = []
        for row in rows:
            serialized_rows.append({k: serialize_val(v) for k, v in row.items()})
        data[t] = serialized_rows
        print(f"  [+] Exported {len(serialized_rows)} rows from {t}")

    out_file = BASE_DIR / 'mysql_data_backup.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dumps(data, indent=2)
        f.write(json.dumps(data, indent=2))

    print(f"[+] All data exported safely to: {out_file}")
    cursor.close()
    conn.close()

if __name__ == '__main__':
    backup_mysql()
