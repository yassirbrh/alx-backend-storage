#!/usr/bin/env python3
'''
    Script that provides some stats about Nginx logs stored in MongoDB.
'''
from pymongo import MongoClient


def print_log_data(collection):
    '''
        print_log_data: function
        description: provides some stats about Nginx logs stored in MongoDB.
        @collection: collection object.
        return: void function.
    '''
    log_collection = list(collection)
    methods = {
            'GET': 0,
            'POST': 0,
            'PUT': 0,
            'PATCH': 0,
            'DELETE': 0
    }
    num_of_logs = len(log_collection)
    check_status = 0
    for log in log_collection:
        if log.get('method') == 'GET' and log.get('path') == '/status':
            check_status += 1
        if log.get('method') in methods:
            methods[log.get('method')] += 1
    print('{} logs'.format(num_of_logs))
    print('Methods:')
    for key, value in methods.items():
        print('\tmethod {:s}: {:d}'.format(key, value))
    print('{} status check'.format(check_status))

if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print_log_data(nginx_collection.find())
