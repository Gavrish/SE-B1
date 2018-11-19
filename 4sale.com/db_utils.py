import psycopg2
import psycopg2.extras
from utils import *

# A singleton class for maintainign Database connections
class db:
    __instance = None
     
    #initialize given hostname, database name, username and password, generates connection and cursor objects
    def __init__(self,host, database, user, password):
        if db.__instance!=None:
            raise Exception("The db class is a singleton class")
        else:
            db.__instance=self
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self.connection = psycopg2.connect(database=database, user=user, password=password, host=host)
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
         
    # A getter function to get the db connection object
    def get_connection(self):
        return self.connection
    
    # A getter function to get the db cursor object
    def get_cursor(self):
        return self.cursor
    
    # A function to query the database given the tablename,columns and conditions(in the form of variable length keyword arguments)
    def query(self,table,cols=['*'],**kwargs):
        query = "select " + ",".join(cols) + " from " + table 
        if(len(kwargs)>0):
            query += " where " + " and ".join([ column + "=" + str(value) if not(isinstance(value, str)) else column + "=" + "'"+ normalize(value) + "'" for column,value in kwargs.items() ])
        print(query)
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # A function to query the database given the tablename,columns and conditions(in the form of a dictionary)
    def query_from_dict(self,table,d,cols=['*']):
        query = "select " + ",".join(cols) + " from " + table
        if(len(d)>0):
            query += " where " + " and ".join([ column + "=" + str(value) if not(isinstance(value, str)) else column + "=" + "'"+ normalize(value) + "'" for column,value in d.items() ])
        print(query)
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # A function to return a query string, given the table name, columns and conditions(in the form of a dictionary)
    def query_string_from_dict(self,table,d,cols=['*']):
        query = "select " + ",".join(cols) + " from " + table
        if(len(d)>0):
            query += " where " + " and ".join([ column + "=" + str(value) if not(isinstance(value, str)) else column + "=" + "'"+ normalize(value) + "'" for column,value in d.items() ])
        print(query)
        return query 
    
    # A function to execute and return the results of a given query string
    def execute_query_string(self,string):
        self.cursor.execute(string)
        return self.cursor.fetchall()
    
    # A function to insert values into a table of a database (values given in the form of a variable length keyword arguments)
    def insert(self,table,**kwargs):
        query = "insert into " + table + "(" + ",".join([column for column,_ in kwargs.items()]) + ") " + "values(" + ",".join([str(value) if not(isinstance(value, str)) else "'" + normalize(value) + "'" for _,value in kwargs.items()]) + ")"
        #print(query)
        self.cursor.execute(query)
        self.connection.commit()
        
    # A function to insert values into a table of a database (values given in the form of a dictionary)
    def insert_from_dict(self,table,d):
        query = "insert into " + table + "(" + ",".join([key for key,_ in d.items()]) + ") " + "values(" + ",".join([str(value) if not(isinstance(value, str)) else "'" + normalize(value) + "'" for _,value in d.items()]) + ")"
        print(query)
        self.cursor.execute(query)
        self.connection.commit()
        
    # A function to insert values into a table of a database (values given in the form of a dictionary as well as variable length keyword arguments)
    def insert_from_dict_and_kw(self,table,d,**kwargs):
        query = "insert into " + table + "(" + ",".join([key for key,_ in d.items()]) + "," + ",".join([column for column,_ in kwargs.items()]) +  ") " + "values(" + ",".join([str(value) if not(isinstance(value, str)) else "'" + normalize(value) + "'" for _,value in d.items()]) + "," + ",".join([str(value) if not(isinstance(value, str)) else "'" + normalize(value) + "'" for _,value in kwargs.items()]) + ")"
        print(query)
        self.cursor.execute(query)
        self.connection.commit()