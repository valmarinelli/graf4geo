#!/bin/env python3
'''
This script makes an automatic pull of logs to the Carbon/Graphite server defined
by the user, by editing the *carbon.ini* configuration file
'''

from time import mktime, strptime
import os
#import sys
from configparser import ConfigParser

def main():
    carbonserver = list(paramreader(section='carbonserver').values())
    metrics_keys = list(paramreader(section='metrics').keys())
    datapath = paramreader(filename='database.ini', section='datapath').__getitem__('archive')
    archive = datapath + 'panels_timeseries_2021.csv'

with open(archive, 'r') as f:
    lines = f.readlines()
    header = lines[0].strip().split(',')
    print(header)
    for line in lines[1:20]:
        fields = line.strip().split(',')
        # Get timestamp in UNIX format (seconds from Epoch)
        epoch = mktime(strptime(fields[0],'%Y-%m-%d %H:%M:%S'))
        print(epoch)
            
                           
    #for mk in metrics_keys:
        #print(mk + ' : ' + paramreader(section='metrics')[mk] + '  @' + str(now))
        
    #filename = sys.argv[1]
    #yyyy = filename.split('_')[0]
    
    #with open(sys.argv[1], 'r') as f:
        #lines = f.readlines()
        #for line in lines[2:]:
            #words = (line.strip().split())
            #if len(words) != 10:
                #return
            #words[0] = '{} {}'.format(yyyy, words[0])
            #csv_words = ['"{}"'.format(w) for w in words]
            #print(','.join(csv_words))

def paramreader(filename='carbon.ini', section='carbonserver'):
    """ Read the carbon.ini file and returns specific data, depending on section"""
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
            
            
            
if __name__ == '__main__':
    main()
            

### RUBBISH ##

#TIMESTAMP=`date +%s`

#SOL_V=``
#NUMBER_OF_ROOT_PROCS=`ps aux | grep root | wc -l`
#NUMBER_OF_DOCKER_PROCS=`ps aux | grep docker | wc -l`

#echo ${METRIC_011} ${NUMBER_OF_USER_PROCS} ${TIMESTAMP} | nc ${CARBON_HOST} ${CARBON_PORT}

#echo ${METRIC_02} ${NUMBER_OF_ROOT_PROCS} ${TIMESTAMP} | nc ${CARBON_HOST} ${CARBON_PORT}

#echo ${METRIC_03} ${NUMBER_OF_DOCKER_PROCS} ${TIMESTAMP} | nc ${CARBON_HOST} ${CARBON_PORT}

## Client

#import socket
#import sys

#HOST, PORT = "localhost", 9999
#data = " ".join(sys.argv[1:])

## Create a socket (SOCK_STREAM means a TCP socket)
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    ## Connect to server and send data
    #sock.connect((HOST, PORT))
    #sock.sendall(bytes(data + "\n", "utf-8"))
    
    ## Receive data from the server and shut down
    #received = str(sock.recv(1024), "utf-8")
    
    #print("Sent:     {}".format(data))
    #print("Received: {}".format(received))
    
