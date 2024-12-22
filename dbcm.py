import sqlite3
import logging

class OpenDatabase:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.dbname)
            return self.conn.cursor()
        except Exception:
            logging.exception("Database Context Manager - __enter__ error: ")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            self.conn.commit()
            self.conn.close()
        except Exception:
            logging.exception("Database Context Manager - __exit__ error: ")
