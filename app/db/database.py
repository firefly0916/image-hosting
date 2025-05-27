import sqlite3
import os

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'db.db')
        self._init_db()

    def _init_db(self):
        if os.path.exists(self.db_path):
            print("[INFO] Database already exists.")
            return

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                url TEXT NOT NULL,
                file_id TEXT,
                message_id TEXT,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("[INFO] Database initialized.")

    def insert_file_record(self, filename, url, file_id=None, message_id=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO files (filename, url, file_id, message_id) VALUES (?, ?, ?, ?)', (filename, url, file_id, message_id))
        conn.commit()
        conn.close()

    def get_all_records(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM files')
        records = c.fetchall()
        conn.close()
        return records

    def get_file_record(self, record_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM files WHERE id = ?', (record_id,))
        record = c.fetchone()
        conn.close()
        return record

    def update_file_record(self, record_id, filename=None, url=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        if filename and url:
            c.execute('UPDATE files SET filename = ?, url = ? WHERE id = ?', (filename, url, record_id))
        elif filename:
            c.execute('UPDATE files SET filename = ? WHERE id = ?', (filename, record_id))
        elif url:
            c.execute('UPDATE files SET url = ? WHERE id = ?', (url, record_id))
        conn.commit()
        conn.close()

    def delete_file_record(self, record_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM files WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
