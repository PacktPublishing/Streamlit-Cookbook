import time
import diskcache as dc

def timing_decorator(func):
    '''
    The timing_decorator function is a decorator that can be applied to any function.
    It measures the execution time of the function by calculating the difference
    between the start time and end time using the time module. To use the decorator, 
    simply apply it to the function you want to time and it will print the execution time
    in seconds after the function finishes running.
    '''
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' took {execution_time:.4f} seconds to execute.")
        return result
    return wrapper

# -----------------------------------------------------------------------------
# Example 1: General-Purpose Disk Cache with Default Configuration
def example_1():
    # Create a cache object
    cache = dc.Cache("./cache")

    key = input("Enter a key name? ")

    # Retrieve data from the cache
    data = cache.get(key)

    if data is not None:
        print(f"Startup: ({key},{data}) found in cache")
        val = input(f"Enter a new value for '{key}'? ")
    else:
        print(f"Startup: Key '{key}' not found in cache")
        val = input(f"Enter a value for '{key}'? ")

    # Store data in the cache
    cache.set(key, val)

    if input(f"Delete key '{key}' (Y/N)? ").lower() == "y":
        # Delete data from the cache
        cache.delete(key)
        print(f"({key},{val}) deleted")

    # Retrieve data from the cache
    data = cache.get(key)

    if data is not None:
        print(f"Completion: ({key},{data}) found in cache")
        print("(This data will be available from the cache when the program is rerun)")
    else:
        print(f"Completion: Key '{key}' not found in cache")
        print("(This data will NOT be available from the cache when the program is rerun)")

    # Close the cache to release resources
    cache.close()

# -----------------------------------------------------------------------------
# Example 2: Memoizing an Expensive Function
def example_2(clear_cache=False):
    # Create a cache object
    cache = dc.Cache("./cache", disk=dc.JSONDisk, size_limit=100, eviction_policy='none')

    # Define a function to be memoized
    @timing_decorator
    @cache.memoize()
    def expensive_function(n):
        print(f"Computing ({n})...")
        # Perform expensive computation here
        time.sleep(2)
        result = n ** 2
        return result

    # Call the memoized function
    
    # Computation is performed (slow if not cached)
    print(f"Result = {expensive_function(2)}")
    # Cached result is returned (fast if cached)
    print(f"Result = {expensive_function(2)}")
    
    # Computation is performed (slow if not cached)
    print(f"Result = {expensive_function(7)}")
    # Cached result is returned (fast if cached)
    print(f"Result = {expensive_function(7)}")
    
    if clear_cache:
        if input(f"Clear cache (Y/N)? ").lower() == "y":
            # Clear the cache
            cache.clear()
            print("(Data will NOT be available from the cache when the program is rerun)")
        else:
            print("(Data will be available from the cache when the program is rerun)")

    # Close the cache to release resources
    cache.close()

# RUN THE EXAMPLES ------------------------------------------------------------

# example_1()
example_2(clear_cache=True)

