#!/usr/bin/env python3
'''
    class Cache.
'''
import redis
from typing import Callable, Union
import uuid


class Cache:
    '''
        Class Cache.
    '''
    union: Union[str, bytes, int, float]
    
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

    def get(self, key: str, fn: Callable = None) -> "Cache.union":
        '''
            Function that returns the data after being type casted using
            the Callable.
        '''
        data = self._redis.get(key)
        if fn:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> Union[str, bytes, int, float]:
        '''
            Function that returns the data in a string format.
        '''
        data = self.get(key, lambda x: x.decode("utf-8"))
        return data

    def get_int(self, key: str) -> Union[str, bytes, int, float]:
        '''
            Function that returns the data in an integer format.
        '''
        data = self.get(key, lambda x: int(x))
        return data
