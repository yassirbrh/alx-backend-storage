#!/usr/bin/env python3
'''
    Function that lists all documents in a collection.
'''


def list_all(mongo_collection):
    '''
        list_all: function
        @mongo_collection: Collection object.
        return: all the documents in a collection.
    '''
    result = list(mongo_collection.find())
    if len(result) != 0:
        return result
    return []
