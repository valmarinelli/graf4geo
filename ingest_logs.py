#! /usr/bin/env python3
'''
Python 3 script that manages the data insertion into the PostgreSQL DB
'''
import os
import csv
# import time
import psycopg2 # Python module for PostgreSQL
from configparser import ConfigParser

## MAIN ##

def main():
    
    Date = strftime("%Y-%m-%d", localtime())
    # Get the absolute path where logs reside (LOCAL ARCHIVE)
    datapath = paramreader(section='datapath')['path']
    # Read DB parameters
    dbconfig = paramreader()
    table = paramreader(section='database')['table']
    # List CSV files
    csv_list = sorted( [ f for f in os.listdir(datapath) if f.endswith('.csv') ] )
    
    for FILE in csv_list:
        print('Working on ' + FILE)
        conn = None
        try:
            # Connect to the DB instance
            conn = psycopg2.connect(**dbconfig)
            # create a cursor
            cur = conn.cursor()
            
            with open(datapath + FILE, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', dialect='unix')
                for row in reader:
                    row_all = next(reader) # Read line after line, till the end of file
                    # Convert Date&Time to UNIX timestamp (epoch)
                    # T = time.mktime(time.strptime(row[0],'%Y-%m-%d %H:%M:%S'))
                    cur.execute(\
                        'INSERT INTO ' + table + 'VALUES (' + row_all + ') '\
                            'ON CONFLICT (time) DO NOTHING;')
                    cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    
    
def paramreader(filename='database.ini', section='postgresql'):
    """ Read the database.ini file and returns specific data, depending on section"""
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to datapath
    result = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            result[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return result
        
#def dbconnect():
    #""" Connect to the PostgreSQL database server """
    #conn = None
    #try:
        ## read connection parameters
        #params = paramreader()
        ## connect to the PostgreSQL server
        #print('Connecting to the PostgreSQL database...')
        #conn = psycopg2.connect(**params)	
        ## create a cursor
        #cur = conn.cursor()
    	## execute a test statement
        #print('PostgreSQL database version:')
        #cur.execute('SELECT version()')
        ## display the PostgreSQL database server version
        #print(cur.fetchone())       
        ## close the communication with the PostgreSQL
        #cur.close()
    #except (Exception, psycopg2.DatabaseError) as error:
        #print(error)
    #finally:
        #if conn is not None:
            #conn.close()
            #print('Database connection closed.')

if __name__ == '__main__':
    main()
