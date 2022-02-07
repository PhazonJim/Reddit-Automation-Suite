import os
import sqlite3
from sqlite3 import Error
import yaml

from .tables import sql_create_comments_table, sql_create_redditors_table, sql_create_submissions_table

class DataLogger:
    def __init__(self):
        self.db_file = self.get_db_file()
        self.conn = self.create_connection()
        self.cur = self.conn.cursor()
        self.create_tables()

    def get_db_file(self):
        with open(os.path.join(os.getcwd(), "reddit-automation-suite/config.yaml")) as f:
            config = yaml.load(f.read(),  Loader=yaml.FullLoader)
            return config["database"]

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)
        return conn
    
    def create_tables(self):
        for sql in [ sql_create_comments_table, sql_create_redditors_table, sql_create_submissions_table ]:
            self.create_table(sql)

    def create_table(self, sql):
        try:
            self.cur.execute(sql)
        except Error as e:
            print(e)

datalogger = DataLogger()

def create_entry(sql, params):
    try:
        with datalogger.conn:
            datalogger.cur.execute(sql, params)
            return datalogger.cur.lastrowid
    except Error as e:
        print(e)
