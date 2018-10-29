import mysql.connector
from mysql.connector import errorcode, pooling
import copy
import sys
import time

dbConfig = {
    'user': 'root',
    'password': 'test',
    'host': 'db',
}

isLocal = False
if len(sys.argv) >= 2 and sys.argv[1] == "local":
    isLocal = True
    dbConfig['host'] = "127.0.0.1"

dbName = "pdf_to_txt"
dbConfigWithDB = copy.deepcopy(dbConfig)
dbConfigWithDB['database'] = dbName

tables = {}
# Add tables here
tables['buckets'] = (
    "CREATE TABLE `buckets` ("
    "  `bucket_name` VARCHAR(100) BINARY NOT NULL,"
    "  `delete_flag` BOOL NOT NULL,"
    "  PRIMARY KEY (`bucket_name`)"
    ") ENGINE=InnoDB")
tables['buckets_meta'] = (
    "CREATE TABLE `buckets_meta` ("
    "  `bucket_name` VARCHAR(100) BINARY NOT NULL,"
    "  `created` BIGINT(11) NOT NULL,"
    "  `modified` BIGINT(11) NOT NULL,"
    "  PRIMARY KEY (`bucket_name`),"
    "  FOREIGN KEY (`bucket_name`) REFERENCES buckets(`bucket_name`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")
tables['objects'] = (
    "CREATE TABLE `objects` ("
    "  `object_name` VARCHAR(100) BINARY NOT NULL,"
    "  `bucket_name` VARCHAR(100) BINARY NOT NULL,"
    "  `md5` VARCHAR(40) NULL DEFAULT NULL,"
    "  `complete_flag` BOOL NOT NULL,"
    "  `delete_flag` BOOL NOT NULL,"
    "  PRIMARY KEY (`object_name`, `bucket_name`),"
    "  FOREIGN KEY (`bucket_name`) REFERENCES buckets(`bucket_name`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")
tables['objects_parts'] = (
    "CREATE TABLE `objects_parts` ("
    "  `object_name` VARCHAR(100) BINARY NOT NULL,"
    "  `bucket_name` VARCHAR(100) BINARY NOT NULL,"
    "  `part_number` INT(5) NOT NULL,"
    "  `md5` VARCHAR(40) NOT NULL,"
    "  PRIMARY KEY (`object_name`, `bucket_name`, `part_number`),"
    "  FOREIGN KEY (`object_name`) REFERENCES objects(`object_name`) ON DELETE CASCADE,"
    "  FOREIGN KEY (`bucket_name`) REFERENCES buckets(`bucket_name`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")
tables['objects_meta'] = (
    "CREATE TABLE `objects_meta` ("
    "  `object_name` VARCHAR(100) BINARY NOT NULL,"
    "  `bucket_name` VARCHAR(100) BINARY NOT NULL,"
    "  `key` VARCHAR(100) BINARY NOT NULL,"
    "  `value` VARCHAR(500) NOT NULL,"
    "  PRIMARY KEY (`object_name`, `bucket_name`, `key`),"
    "  FOREIGN KEY (`object_name`) REFERENCES objects(`object_name`) ON DELETE CASCADE,"
    "  FOREIGN KEY (`bucket_name`) REFERENCES buckets(`bucket_name`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

def connectRootDB():
    return mysql.connector.connect(**dbConfig)

def createDB():
    conn = connectRootDB()
    cur = conn.cursor()
    query = "CREATE DATABASE IF NOT EXISTS {}".format(dbName)
    cur.execute(query)
    cur.close()
    conn.close()

def getConnFromPool():
    try:
        return dbPool.get_connection()
    except mysql.connector.PoolError:
        return connectDB()

def connectDB():
    return mysql.connector.connect(**dbConfigWithDB)

def createTables():
    conn = getConnFromPool()
    cur = conn.cursor()
    for name, query in tables.items():
        try:
            print("Creating table {}: ".format(name), end='')
            cur.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Already exists")
            else:
                print(err.msg)
        else:
            print("OK")
    cur.close()
    conn.close()

dbPool = None
if isLocal:
    print("Running locally")
    print("Initialization start")
    print("Creating the database")
    createDB()
    dbPool = pooling.MySQLConnectionPool(pool_name="myPool",
                                                pool_size=10,  # Assume each thread will produce 10 connections each
                                                **dbConfigWithDB)
    print("Creating the tables")
    createTables()
    print("Initialization complete")
else: # On prod, use the init.sql to create database schema
    while True:
        try:
            print("Trying to set up database pool")
            dbPool = pooling.MySQLConnectionPool(pool_name = "myPool",
                                                 pool_size = 10, # Assume each thread will produce 10 connections each
                                                 **dbConfigWithDB)
        except Exception as e:
            print(str(e))
            print("Retrying...")
            time.sleep(1)
        else:
            break

# Add functions to get/update/insert/remove here