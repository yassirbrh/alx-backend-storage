#!/usr/bin/env python3
'''
    Function that inserts a new document in a collection based on kwargs.
'''


def insert_school(mongo_collection, **kwargs):
    '''
        insert_school: function
        @mongo_collection: Collection object.
        @kwargs: list of keyworded arguments to insert in the collection
        return: the new _id.
    '''
    result = mongo_collection.insert_one(kwargs)
    new_id = result.inserted_id
    return new_id
