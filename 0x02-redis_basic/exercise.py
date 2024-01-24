#!/usr/bin/env python3
'''
    class Cache.
'''
import redis
from typing import Union
import uuid


class Cache:
    '''
        Class Cache.
    '''
    def __init__(self):
        '''
            The constructor of the class Cache.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
            Method that takes a data argument and returns a string.
            The method should generate a random key
            store the input data in Redis using the random key
            and return the key.
        '''
        uid = str(uuid.uuid4())
        self._redis.set(uid, data)
        return uid
