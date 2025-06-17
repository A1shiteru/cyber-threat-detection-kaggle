# utils.py
import time
from functools import wraps
import logging
from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO)

def rate_limited(max_per_minute):
    min_interval = 60.0 / float(max_per_minute)
    
    def decorate(func):
        last_time_called = 0.0
        
        @wraps(func)
        def rate_limited_function(*args, **kwargs):
            nonlocal last_time_called
            elapsed = time.monotonic() - last_time_called
            wait = min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
            last_time_called = time.monotonic()
            return func(*args, **kwargs)
        return rate_limited_function
    return decorate

def retry(max_retries=3, backoff_factor=0.5, exceptions=(RequestException,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries >= max_retries:
                        raise
                    wait = backoff_factor * (2 ** (retries - 1))
                    logging.warning(f"Retry {retries}/{max_retries} after error: {e}. Waiting {wait} seconds")
                    time.sleep(wait)
        return wrapper
    return decorator