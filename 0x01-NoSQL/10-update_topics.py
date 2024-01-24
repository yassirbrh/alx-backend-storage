#!/usr/bin/env python3
'''
    Function that changes all topics of a school document based on the name.
'''


def update_topics(mongo_collection, name, topics):
    '''
        update_topics: function
        @mongo_collection: Collection object.
        @name: name of the collection to update.
        @topics: list of topics to add to the topics attribute
        return: void function
    '''
    condition = {"name": name}
    update = {"$set": {"topics": topics}}
    mongo_collection.update_many(condition, update)
