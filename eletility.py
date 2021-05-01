import os
import datetime
import sqlite3
from sqlite3 import Error

######################## DB ########################
class DB:
    def __init__(self):
        pass

    def connect(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
            return False
        self.conn = conn
        self.cursor = self.conn.cursor()
        return True
    
    def tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cursor.fetchall()
    
    def createTable(self, name, conf):
        cmd = "CREATE TABLE {}(".format(name)
        for key, value in conf.items():
            cmd += "{} {}, ".format(key, value)
        cmd = cmd[:len(cmd)-2]
        cmd += ")"
        self.cursor.execute(cmd)
        self.conn.commit()

    def insert(self, table, values):
        list = "("
        for value in values:
            list += "`{}`, "
        list = list[:len(list)-2] + ")"
        cmd = "INSERT INTO {} VALUES{}".format(table, list)
        self.cursor.execute(cmd)
        self.conn.commit()

######################## PATHHELPER ########################

class PathHelper:
    def __init__(self):
        pass

    def absPath(self, file):
        return os.path.abspath(file)

######################## VALIDATOR ########################

class Validator:
    def __init__(self):
        pass

    def isTitle(self, title, required=False):
        if not required:
            return True
        elif len(title) > 1:
            return True
    
    def isDesc(self, desc, required=False):
        if not required:
            return True
        elif len(desc) > 1:
            return True
    
    def isStrDate(self, date, format, required=False):
        if not required:
            if len(date) < 1:
                return True
        try:
            datetime.datetime.strptime(date, format)
        except ValueError:
            return False
        return True
    
    def isStrYN(self, str, required=False):
        print(str)
        if not required:
            if len(str) < 1:
                return True
        elif str.lower() == "y" or str.lower() == "n":
            return True
        return False
    
    def isNum(self, str, required=False):
        if not required:
            if len(str) < 1:
                return True
        elif str.isnumeric():
            return True
        return False

######################## STRINGPROC ########################

class StringProc:
    pass        

# def create_connection(path):
#     connection = None
#     try:
#         connection = sqlite3.connect(path)
#         print("Successfully Connected")

