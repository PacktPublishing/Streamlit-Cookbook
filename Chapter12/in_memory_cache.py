import time
import functools

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
# Example 1: Caching a Function with Default Configuration
@functools.lru_cache()
def expensive_function_ex1(arg1, arg2):
    # Perform expensive computations
    time.sleep(1)
    return [arg1, arg2]

# -----------------------------------------------------------------------------
# Example 2: Caching a Function with Custom Configuration
@functools.lru_cache(maxsize=20, typed=False)
def expensive_function_ex2(arg1, arg2):
    # Perform expensive computations
    time.sleep(1)
    return [arg1, arg2]

# RUN THE EXAMPLES (PART 1) ---------------------------------------------------

# First iteration will cache and remainder will use cache
# See this in the timing output
def run_ex1():
    print("Running Example 1 ---------------------------------------------------")
    for _ in range(3):
        timing_decorator(expensive_function_ex1)(1, 2)

# First and every third iteration will cache and others will use cache
# See this in the timing output
def run_ex2():
    print("Running Example 2 ---------------------------------------------------")
    for i in range(5):
        for _ in range(3):
            timing_decorator(expensive_function_ex2)(1, i)

run_ex1()
run_ex2()

result = expensive_function_ex1(1, 2)
print(f"Calling expensive_function_ex1(1, 2). Result = {result}")
result[1] = 3
print(f"Modifying cache result EXTERNALLY. Modified result = {result}")
result = expensive_function_ex1(1, 2)
print(f"Calling expensive_function_ex1(1, 2). Result result: {result}... not [1, 2]")
print(f"WARNING: cached data has been externally mutated... take care!")

# -----------------------------------------------------------------------------
# Example 3: Accessing Cache Information
print("Running Example 3 ---------------------------------------------------")
cache_info = expensive_function_ex1.cache_info()
print(f"expensive_function_ex1 cache info: {cache_info}")

cache_info = expensive_function_ex2.cache_info()
print(f"expensive_function_ex2 cache info: {cache_info}")

# -----------------------------------------------------------------------------
# Example 4: Clearing the Cache
print("Running Example 4 ---------------------------------------------------")
expensive_function_ex1.cache_clear()
expensive_function_ex2.cache_clear()
print(f"Caches cleared")

# -----------------------------------------------------------------------------
# Example 5: Caching a Method
class MyClass:
    @functools.lru_cache()
    def expensive_method(self, arg1, arg2):
        # Perform expensive computations
        time.sleep(5)
        return [arg1, arg2]

# RUN THE EXAMPLES (PART 2) ---------------------------------------------------

# First iteration will cache and remainder will use cache
# See this in the timing output
def run_ex5():
    print("Running Example 5 ---------------------------------------------------")
    my_class = MyClass()
    for _ in range(5):
        timing_decorator(my_class.expensive_method)(1, 2)

run_ex5()
