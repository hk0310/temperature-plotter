import logging
import sqlite3
from dbcm import OpenDatabase

class DBOperations:
    def __init__(self):
        self.dbname = "temperature.sqlite"

    def initialize_db(self):
        try:
            with OpenDatabase(self.dbname) as cursor:
                cursor.execute(""" CREATE TABLE IF NOT EXISTS temperatures
                                (
                                    id integer primary key autoincrement not null,
                                    sample_date text,
                                    location text,
                                    min_temp real,
                                    max_temp real,
                                    avg_temp real,
                                    unique (sample_date, location)
                                )""")
        except Exception:
            logging.exception("DBOperations - initialize_db error: ")

    def save_data(self, data):
        try:
            with OpenDatabase(self.dbname) as cursor:
                try:
                    query = """INSERT INTO temperatures
                    (sample_date, location, min_temp, max_temp, avg_temp) values
                    (?, 'Winnipeg, MB', ?, ?, ?)"""

                    for key, value in data.items():
                        query_vars = (key, value["Min"], value["Max"], value["Mean"])
                        cursor.execute(query, query_vars)
                except sqlite3.IntegrityError:
                    print("Duplicate data detected, did not update database.")
        except Exception:
            logging.exception("DBOperations - save_data error: ")

    def purge_data(self):
        try:
            with OpenDatabase(self.dbname) as cursor:
                cursor.execute("DELETE FROM temperatures")
        except Exception:
            logging.exception("DBOperations - purge_data error: ")

    def fetch_data(self):
        try:
            with OpenDatabase(self.dbname) as cursor:
                rows = ()

                for row in cursor.execute("SELECT * FROM temperatures"):
                    rows += (row, )

                return rows
        except Exception:
            logging.exception("DBOperations - fetch_data error: ")

    def get_latest_date(self):
        try:
            with OpenDatabase(self.dbname) as cursor:
                for row in cursor.execute(
                    "SELECT sample_date FROM temperatures ORDER BY sample_date DESC LIMIT 1"):
                    return row
        except Exception:
            logging.exception("DBOperations - get_latest_date error: ")
    