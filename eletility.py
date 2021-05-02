import os
import datetime
import sqlite3
from sqlite3 import Error

######################## DB ########################
class DB:
    def __init__(self):
        pass

    def connect(self, db_file):
        """ connects to or creates a database connection to a SQLite database """
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
        """ returns a list containing all the table names """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cursor.fetchall()[0]

    def tableExists(self, key):
        """ returns true if the given table name exists"""
        tables = self.tables()
        for name in tables:
            if name == key:
                return True
        return False
    
    def createTable(self, name, conf):
        """ creates a table """
        cmd = "CREATE TABLE IF NOT EXISTS {}(".format(name)
        for key, value in conf.items():
            cmd += "{} {}, ".format(key, value)
        cmd = cmd[:len(cmd)-2]
        cmd += ")"
        self.cursor.execute(cmd)
        self.conn.commit()

    def insertUnique(self, table, col, values):
        """ inserts a row to a table if a condition is met """
        uniqueVal = None
        keys = "("
        vals = "("
        for key in values:
            if key == col:
                uniqueVal = values[key]
            vals += "'{}', ".format(values[key])
            keys += "{}, ".format(key)
        vals = vals[:len(vals)-2] + ")"
        keys = keys[:len(keys)-2] + ")"
        cmd = "INSERT INTO {0} {1} SELECT {2} WHERE NOT EXISTS (SELECT 1 FROM {0} WHERE {3}='{4}')".format(table, keys, vals, col, uniqueVal)        
        self.cursor.execute(cmd)
        self.conn.commit()

    # def selectOne(self, table, condition=""):
    #     cmd = "SELECT 1 from {table} WHERE {condition}".format(table, condition)
        

    def selectAll(self, table, condition="TRUE"):
        """ returns all the rows of a given table which meet a given condition """
        cmd = "SELECT * from {0} WHERE {1}".format(table, condition)
        self.cursor.execute(cmd)
        return self.cursor.fetchall()
        
       
    def insert(self, table, values, condition=""):
        """ inserts a row to a table """
        keys = "("
        vals = "("
        for key in values:
            vals += "'{}', ".format(values[key])
            keys += "{}, ".format(key)
        vals = vals[:len(vals)-2] + ")"
        keys = keys[:len(keys)-2] + ")"
        cmd = "INSERT INTO {} {} VALUES {}".format(table, keys, vals)
        if condition != "":
            cmd += condition

        self.cursor.execute(cmd)
        self.conn.commit()

    def delete(self, table, condition):
        """ deletes row(s) from a given table which meet a given condition """
        cmd = "DELETE FROM {} WHERE {}".format(table, condition)
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

