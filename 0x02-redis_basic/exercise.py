#!/usr/bin/env python3
'''
    class Cache.
'''
import redis
from typing import Any, Callable, Union
from functools import wraps
import uuid


def count_calls(method: Callable) -> Callable:
    '''
        Decorator count_calls.
    '''
    @wraps(method)
    def func(self, *args, **kwargs) -> Any:
        '''
            func: function
            @self: redis object.
            @args: list of arguments.
            @kwargs: list of keyworded arguments.
            return: method
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return func


def call_history(method: Callable) -> Callable:
    '''
        Decorator call_history
    '''
    @wraps(method)
    def func(self, *args, **kwargs) -> Any:
        '''
            func: function
            @self: redis object.
            @args: list of arguments.
            @kwargs: list of keyworded arguments.
            return: method
        '''
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
            final_output = method(self, *args, **kwargs)
            self._redis.rpush(output_key, final_output)
        return final_output
    return func


def replay(func: Callable) -> None:
    '''
        replay function.
    '''
    if func is not None and hasattr(func, '__self__'):
        redis_inst = getattr(func.__self__, '_redis', None)
        if isinstance(redis_inst, redis.Redis):
            func_class_nm = func.__qualname__
            call_count = 0
            if redis_inst.exists(func_class_nm) != 0:
                call_count = int(redis_inst.get(func_class_nm))
            print('{} was called {} times:'.format(func_class_nm, call_count))
            input_key = "{}:inputs".format(func.__qualname__)
            func_inputs = redis_inst.lrange(input_key, 0, -1)
            output_key = "{}:outputs".format(func.__qualname__)
            func_outputs = redis_inst.lrange(output_key, 0, -1)
            for func_input, func_output in zip(func_inputs, func_outputs):
                print('{}(*{}) -> {}'.format(
                    func_class_nm,
                    func_input.decode('utf-8'),
                    func_output,
                    ))


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

    @count_calls
    @call_history
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
