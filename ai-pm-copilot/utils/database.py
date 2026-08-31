import sqlite3
from pathlib import Path
import pandas as pd

SCHEMA = '''
CREATE TABLE IF NOT EXISTS theme_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme_id INTEGER,
    original_name TEXT,
    updated_name TEXT,
    action TEXT,
    timestamp TEXT
);
CREATE TABLE IF NOT EXISTS prd_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme_id INTEGER,
    generated_prd TEXT,
    edited_prd TEXT,
    status TEXT,
    timestamp TEXT
);
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    operation TEXT,
    provider TEXT,
    theme TEXT,
    status TEXT
);
'''


def init_db(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executescript(SCHEMA)
    conn.commit()
    conn.close()


def record_audit(db_path, operation, provider, theme, status):
    import datetime
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO audit_log(timestamp,operation,provider,theme,status) VALUES (?,?,?,?,?)',
              (datetime.datetime.utcnow().isoformat(), operation, provider, theme, status))
    conn.commit()
    conn.close()


def fetch_audit(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query('SELECT * FROM audit_log ORDER BY id DESC LIMIT 200', conn)
    conn.close()
    return df
