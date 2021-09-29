#! /usr/bin/env python3
import os
import psycopg2 # Python module for PostgreSQL
from configparser import ConfigParser

datapath = paramreader(section='datapath')

def main():
    
    # Read DB parameters
    dbconfig = paramreader()
    # List CSV files
    csv_list = sorted( [ f for f in os.listdir(datapath) if f.endswith('.csv') ] )
    
    for FILE in csv_list:
        print(FILE)
        # leggere riga per riga i CSV e poi fare l'"INSERT ... ON CONFLICT ..."
    
    
def paramreader(filename='database.ini', section='postgresql'):
    """ Read the database.ini file and returns specific data, depending on section"""
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to datapah
    result = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            result[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return result
        
def dbconnect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = dbconfig()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)	
        # create a cursor
        cur = conn.cursor()
    	# execute a test statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        print(cur.fetchone())       
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    main()
