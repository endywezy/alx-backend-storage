#!/usr/bin/env python3
"""
Caching request module with Redis
"""
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize the Redis client outside the functions to reuse the connection
client = redis.Redis()


def track_get_page(fn: Callable) -> Callable:
    """ Decorator for get_page to track URL access and cache responses """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper function to:
            - Track how many times a URL's data is accessed
            - Cache the response for 10 seconds
        """
        # Increment the access count
        client.incr(f'count:{url}')
        # Check if the page is already cached
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        # Fetch the page if not cached
        response = fn(url)
        # Cache the response for 10 seconds
        client.setex(f'{url}', 10, response)
        return response
    return wrapper

# Fetch the HTML content of http://google.com
response = get_page("http://google.com")
print(response)

# Check if the response is cached in Redis
cached_page = client.get("http://google.com")
if cached_page:
    print("Cached response:", cached_page.decode('utf-8'))
else:
    print("No cached response found")

# Wait for 10 seconds
import time
time.sleep(10)

# Check if the cached response has been removed from Redis
cached_page = client.get("http://google.com")
if cached_page:
    print("Cached response still exists")
else:
    print("Cached response has been removed")
@track_get_page
def get_page(url: str) -> str:
    """ Fetches the HTML content of a URL """
    response = requests.get(url)
    return response.text
