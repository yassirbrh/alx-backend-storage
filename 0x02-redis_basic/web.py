#!/usr/bin/env python3
'''
    get_page function that it uses the requests module
    to obtain the HTML content of a particular URL and returns it.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_inst = redis.Redis()


def access_count(func: Callable) -> Callable:
    '''
        access_count: decorator
        @func: Function to count the access to it.
        return: Callable.
    '''
    @wraps(func)
    def method(url) -> str:
        '''
            method: function
            @url: Url link.
            return: Any.
        '''
        redis_inst.incr('count:{}'.format(url))
        result = redis_inst.get('result:{}'.format(url))
        if result:
            return result.decode('utf-8')
        result = func(url)
        redis_inst.set('count:{}'.format(url), 0)
        redis_inst.setex('result:{}'.format(url), 10, result)
        return result
    return method


@access_count
def get_page(url: str) -> str:
    '''
        get_page: function
        @url: Url of the page.
        return: the HTML content of the particular url
    '''
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
