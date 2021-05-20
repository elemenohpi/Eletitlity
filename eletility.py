import os
import datetime, time
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
    
    def insertUnique(self, table, values, condition = True):
        """ inserts a row to a table if a condition is met """
        keys = "("
        vals = ""
        for key in values:
            vals += "'{}', ".format(values[key])
            keys += "{}, ".format(key)
        vals = vals[:len(vals)-2] + ""
        keys = keys[:len(keys)-2] + ")"
        cmd = "INSERT INTO {0} {1} SELECT {2} WHERE NOT EXISTS (SELECT 1 FROM {0} WHERE {3})".format(table, keys, vals, condition)       
        self.cursor.execute(cmd)
        self.conn.commit()

    def insertUniqueCol(self, table:str, col:str, values:list):
        """ inserts a row to a table if a single condition is met """
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
       
    def insert(self, table, values, condition="TRUE"):
        """ inserts a row to a table """
        keys = "("
        vals = "("
        for key in values:
            vals += "'{}', ".format(values[key])
            keys += "{}, ".format(key)
        vals = vals[:len(vals)-2] + ")"
        keys = keys[:len(keys)-2] + ")"
        cmd = "INSERT INTO {} {} VALUES {} WHERE {}".format(table, keys, vals, condition)

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

    def writeLine(self, file, str, create=True):
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

########################## Times ##########################

class Times:
    def __init__(self):
        """ Date time helper functions"""
        pass
    
    def monthS2N(self, month):
        """ converts a month string to its corresponding numberical value """
        month = month.lower()
        if month == "jan" or month == "january":
            return "01"
        elif month == "feb" or month == "february":
            return "02"
        elif month == "mar" or month == "march":
            return "03"
        elif month == "apr" or month == "april":
            return "04"
        elif month == "may" or month == "may":
            return "05"
        elif month == "jun" or month == "june":
            return "06"
        elif month == "jul" or month == "july":
            return "07"
        elif month == "aug" or month == "august":
            return "08"
        elif month == "sep" or month == "september":
            return "09"
        elif month == "oct" or month == "october":
            return "10"
        elif month == "nov" or month == "november":
            return "11"
        elif month == "dec" or month == "december":
            return "12"
        else:
            raise "invalid month"

    def now(self):
        now = datetime.datetime.now().time()
        return now
        pass

    def substract(self, endtime, starttime):
        date = datetime.date(1, 1, 1)
        startDateTime = datetime.datetime.combine(date, starttime)
        endDateTime = datetime.datetime.combine(date, endtime)
        diff = endDateTime - startDateTime
        return diff

########################## ConfigParser ##########################

class ConfigParser:
    """ Config parser constructor """
    def __init__(self):
        pass
    
    """ reads from a given config file and returns a list of the arguements """
    def read(self, path):
        config = {}
        try:
            file = open(path, 'r')
        except IOError as e:
            raise Exception(e.strerror)
        
        lines = file.readlines()
        for num, line in enumerate(lines):
            line = line.split("#")[0].strip()
            
            if len(line) == 0:
                # empty line, ignore
                continue
            elif line[0] == "#":
                # comment
                continue
            else:
                tokens = line.split("=")
                if len(tokens) != 2:
                    # illegal length
                    raise Exception("Illegal format on line " + repr(num) + " of " + file)
                else:
                    # legal format
                    config[tokens[0].strip()] = tokens[1].strip()
        
        return config

########################## Colors ##########################

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    DEBUG = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

########################## Log ##########################

class Log:
    def __init__(self, level="info", prefix=None) -> None:
        # if level == "warning":
        #     level = logging.WARNING
        # elif level == "debug":
        #     level = logging.DEBUG
        # else:
        #     level = logging.WARNING
        self.level = level
        self.prefix = prefix
        pass

    def D(self, message):
        time = Times().now() 
        if not self.prefix is None:
            message = "{}:{}".format(self.prefix, message)
        message = "{}:{}".format(time, message)
        if self.level == "debug":
            print(Colors.DEBUG, message, Colors.ENDC)
    
    def W(self, message):
        time = Times().now() 
        if not self.prefix is None:
            message = "{}:{}".format(self.prefix, message)
        message = "{}:{}".format(time, message)
        if self.level == "warning" or "debug" or "info":
            print(Colors.WARNING, message, Colors.ENDC)
    
    def I(self, message):
        time = Times().now() 
        if not self.prefix is None:
            message = "{}:{}".format(self.prefix, message)
        message = "{}:{}".format(time, message)
        if self.level == "warning" or "debug" or "info":
            print(Colors.OKGREEN, message, Colors.ENDC)
    
    def E(self, message):
        time = Times().now() 
        if not self.prefix is None:
            message = "{}:{}".format(self.prefix, message)
        message = "{}:ERROR:{}".format(time, message)
        if self.level == "warning" or "debug" or "info":
            print(Colors.ERROR, message, Colors.ENDC)
        exit()

########################## List ##########################

class List:
    def __init__(self) -> None:
        pass

    def sort_list_by_obj_pos(self, list):
        for element in list:
            pos = 
        pass