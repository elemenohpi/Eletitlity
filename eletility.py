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
        return self.cursor.fetchall()

    def tableExists(self, key):
        """ returns true if the given table name exists"""
        tables = self.tables()
        for name in tables:
            if name[0] == key:
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

    def selectOne(self, table, condition=""):
        """ returns one rows of a given table which meets a given condition """
        cmd = "SELECT 1 from {0} WHERE {1}".format(table, condition)
        self.cursor.execute(cmd)
        return self.cursor.fetchone()
        
    def selectAll(self, table, condition="TRUE"):
        """ returns all the rows of a given table which meet a given condition """
        cmd = "SELECT * from {0} WHERE {1}".format(table, condition)
        self.cursor.execute(cmd)
        return self.cursor.fetchall()
    
    def rowExists(self, table, condition="TRUE"):
        """ determines if a row exits in a table with a given condition """
        cmd = "SELECT * from {0} WHERE {1}".format(table, condition)
        self.cursor.execute(cmd)
        if len(self.cursor.fetchall()) < 1:
            return False
        return True
       
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

    def update(self, table, values, condition):
        """ inserts a row to a table """
        keyval = ""
        for key in values:
            keyval += "{} = '{}',".format(key, values[key])
        keyval = keyval[:len(keyval)-1]
        cmd = "UPDATE {} SET {} WHERE {}".format(table, keyval, condition)

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
        """ returns the absolute path to a given relative path """
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
                return False
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

########################## FILES ##########################

class Files:
    def __init__(self):
        pass

    def truncate(self, file, create=True):
        """ truncates a given file (creates a file if it doesn't exist) """
        try:
            f = open(file)
            f.truncate()
        except IOError:
            if create:
                f = open(file, "w+")
                f.close()
                return 1
            return 0
        return 1

    def write_line(self, file, str, create=True):
        """ appends a line to a file """
        try:
            f = open(file, "a")
            f.write(str)
            f.write("\n")
        except IOError:
            if create:
                f = open(file, "w+")
                f.write(str)
                f.write("\n")
                f.close()
                return 1
            return 0
        finally:
            f.close()
        return 1

    def write(self, file, str, create=True):
        """ writes into a file (doesn't end the line)"""
        try:
            f = open(file, "a")
            f.write(str)
        except IOError:
            if create:
                f = open(file, "w+")
                f.write(str)
                f.close()
                return 1
            return 0
        finally:
            f.close()
        return 1

    def writeTruncate(self, file, str, create=True):
        """ truncates a file and writes into it """
        self.truncate(file, create)
        self.write(file, str)

    def lbreak(self, file, create=False):
        """ appends a line break to a file """
        try:
            f = open(file, "a")
            f.write("\n")
        except IOError:
            if create:
                f = open(file, "w+")
                f.write("\n")
                f.close()
                return 1
            return 0
        finally:
            f.close()
        return 1
        pass
