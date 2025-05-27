import sqlite3
import os
import requests

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
                year INTEGER,
                month INTEGER,
                day INTEGER,
                uuid TEXT NOT NULL,
                custom_url TEXT,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("[INFO] Database initialized.")

    def insert_file_record(self, filename, url, year, month, day, file_uuid, custom_url):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO files (filename, url, year, month, day, uuid, custom_url) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                  (filename, url, year, month, day, file_uuid, custom_url))
        conn.commit()
        conn.close()

    def get_all_records(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM files')
        records = c.fetchall()
        conn.close()
        return records

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

    def get_file_record(self, year, month, day, uuid):
        """
        Query the database for a file record based on year, month, day, and uuid.
        :param year: The year of the record.
        :param month: The month of the record.
        :param day: The day of the record.
        :param uuid: The UUID of the record.
        :return: The file record if found, otherwise None.
        """
        print(f"[INFO] Querying record for {year}-{month}-{day} with UUID: {uuid}")
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        query = "SELECT * FROM files WHERE year = ? AND month = ? AND day = ? AND uuid = ?"
        params = (year, month, day, uuid)
        c.execute(query, params)
        record = c.fetchone()
        print(f"[INFO] Record found: {record}" if record else "[INFO] No record found.")
        conn.close()
        return record

    def get_record_content(self, year, month, day, uuid):
        """
        Fetch the binary content of the file from the URL stored in the database record.
        :param year: The year of the record.
        :param month: The month of the record.
        :param day: The day of the record.
        :param uuid: The UUID of the record.
        :return: The binary content of the file.
        """
        record = self.get_file_record(year, month, day, uuid)
        if not record:
            raise ValueError("Record not found")

        url = record[2]  # Assuming the URL is the third column in the record
        print(f"[INFO] Fetching content from URL: {url}")
        response = requests.get(url)  # Changed from POST to GET
        print(f"[INFO] Response status code: {response.status_code}")
        if response.status_code != 200:
            raise Exception(f"Failed to fetch content from URL: {url}")

        return response.content
