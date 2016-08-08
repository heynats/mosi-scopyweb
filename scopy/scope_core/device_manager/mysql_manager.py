"""
MOSi Scope Device Framework:
Make real world manufacturing machines highly interoperable with different IT 
solutions. Implemented using python and django framework.

(C) 2016 - Stanley Yeh - ihyeh@mosi.com.tw
(C) 2016 - MOSi Technologies, LLC - http://www.mosi.com.tw

mysql_manager.py
    A connection manager to query a MySQL server using Oracle's python connector
"""

import mysql.connector
import mysql.connector.pooling
from mysql.connector import errorcode
from abstract_manager import AbstractConnectionManager
from scope_core.config import settings

class MySqlConnectionManager(AbstractConnectionManager):
    cnxpool = None
    connection = None    
    
    def __init__(self):
        try:
            self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="fcsdb", **settings.MYSQL_CONFIG)
        except mysql.connector.Error as err:
            print(err)

    def connect(self):
        result = False
        try:
            if self.cnxpool:
                self.connection = self.cnxpool.get_connection()
                cursor = self.connection.cursor()
                #self.connection.set_character_set('utf8');
                cursor.execute('SET NAMES utf8;');
                cursor.execute('SET CHARACTER SET utf8;');
                cursor.execute('SET character_set_connection=utf8;');
                cursor.close()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Invalid username or password!")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist!")
            else:
                print(err)
        else:
            result = True
            return result
            
    def disconnect(self):
        if self.connection:
            self.connection.close()
        
    def query(self, queryString):
        try:
            cursor = None
            if self.connection:
                self.connect()
                cursor = self.connection.cursor()
        except mysql.connector.Error:
            if self.cnxpool:
                self.connection = self.cnxpool.get_connection()
                cursor = self.connection.cursor()
            
        if cursor:
            cursor.execute(queryString)
            result = cursor.fetchone()
            cursor.close()
            self.disconnect()
            return result