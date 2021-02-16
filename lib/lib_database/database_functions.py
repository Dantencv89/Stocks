import psycopg2
import os

stockhost = os.environ.get('STOCKS_DATABASE_LOCALHOST')
#stockhost = os.environ.get('STOCKS_DATABASE_HOST')
stockdb = os.environ.get('STOCKS_DATABASE_DB')
stockuser = os.environ.get('STOCKS_DATABASE_USER')
stockpwd = os.environ.get('STOCKS_DATABASE_PWD')

## Global Connect
connect = None
## Global Cursor
cursor = None

def connect(autocommit=True):
    global connect
    global cursor
    print('Connection to Database')
    try:
        conn = psycopg2.connect(
            host=stockhost,
            user=stockuser,
            database=stockdb,
            password=stockpwd
        )
        conn.set_session(autocommit=autocommit)   
        connect= conn  
    except psycopg2.Error as e:
        print("Error could not make connection to postgres database")
        print(e)
    try:
        cur= conn.cursor()
        cursor = cur
    except psycopg2.Error as e:
        print("Error could not get curser to postgres database")
        print(e)

def get_connector():
    global connect
    print('Returning Connector')
    return connect

def get_cursor():
    global cursor
    print('Returning Cursor')
    return cursor


def create_companies():
    global cursor
    print('Creating Companies Table...')
    cursor.execute('DROP TABLE  IF EXISTS companies');
    try:
        cursor.execute(
        "CREATE TABLE IF NOT EXISTS companies ( \
        symbol varchar PRIMARY KEY, \
        name varchar NOT NULL,\
        exchange varchar NOT NULL,\
        sector varchar,\
        summary varchar, \
        timestamp timestamp default current_timestamp);")
        
    except psycopg2.Error as e:
        print("Error Issue creating a table")
        print(e)


def create_dailystocks():
    global cursor
    print('Creating dailystocks Table...')
    cursor.execute('DROP TABLE  IF EXISTS dailystocks');
    try:
        cursor.execute(
        "CREATE TABLE IF NOT EXISTS dailystocks ( \
        date date, \
        symbol varchar REFERENCES companies , \
        open numeric NOT NULL,\
        high numeric NOT NULL,\
        low numeric NOT NULL,\
        close numeric NOT NULL,\
        volume numeric NOT NULL ,\
        splits numeric,\
        dividends numeric, \
        timestamp timestamp default current_timestamp, \
        PRIMARY KEY (date, symbol));")
        
    except psycopg2.Error as e:
        print("Error Issue creating a table")
        print(e)
        
def close_connections():
    print('Closing Variables ...')
    global connect
    global cursor
    cursor.close()
    connect.close()