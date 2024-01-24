#!/usr/bin/env python3
'''
    Function that returns the list of school having a specific topic.
'''


def schools_by_topic(mongo_collection, topic):
    '''
        update_topics: function
        @mongo_collection: Collection object.
        @topic: topic to look for in the topics list
        return: list of schools containig the topic in the topics list.
    '''
    result = []
    coll_list = list(mongo_collection.find())
    for elem in coll_list:
        if elem.get('topics') is not None and topic in elem.get('topics'):
            result.append(elem)
    return result
