#!/usr/bin/env python3
'''A module with tools for request caching and tracking.'''

import redis
import requests
from functools import wraps
from typing import Callable

# Create a Redis connection instance
redis_store = redis.Redis()

def cache_page(method: Callable) -> Callable:
    '''Decorator to cache the result of a URL request.'''
    @wraps(method)
    def wrapper(url: str) -> str:
        '''Wrapper function to manage caching and counting.'''
        # Increment the count of the URL access
        redis_store.incr(f'count:{url}')
        
        # Try to get the cached result
        cached_result = redis_store.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')
        
        # If not cached, fetch the content from the URL
        result = method(url)
        
        # Cache the result with an expiration time of 10 seconds
        redis_store.setex(f'result:{url}', 10, result)
        
        return result
    return wrapper

@cache_page
def get_page(url: str) -> str:
    '''Fetches the HTML content of a URL and caches it.'''
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Test with a slow URL to check caching
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    print(get_page(test_url))
    print(get_page(test_url))  # Should return the cached result
