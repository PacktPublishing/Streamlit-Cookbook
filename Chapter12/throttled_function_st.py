# Example 3: Throttled Streamlit Application Function
import time
import diskcache as dc

import streamlit as st

message = st.empty()
sub_message = st.empty()

@st.cache_resource
def init_cache() -> dc.Cache:
    # Create a cache object
    cache = dc.Cache("./cache")
    print(f"Cache cleared: {cache.clear(retry=True)} items removed")
    cache.stats(reset=True)
    if not (throttle_rate := cache.get("throttle_rate")):
        cache.set("throttle_rate", 1)
    if not (counter := cache.get("counter")):
        cache.set("counter", 1)
    return cache

# Initialize the DiskCache cache, memoized as a Streamlit cached resource
cache: dc.Cache = init_cache()
message.info("Cache initialized")

# Define the throttle rate (in seconds)
throttle_rate = st.sidebar.slider("Throttle Rate (seconds)", 1, 10, cache.get("throttle_rate"))
cache.set("throttle_rate", throttle_rate)
sub_message.info(f'Throttle rate is set to **{throttle_rate} second(s)**')

# Define the function to be throttled
@cache.memoize()
def throttled_function(arg1, arg2):
    # Perform some action here
    return (arg1, arg2)

# Throttle the function execution
def throttle(counter):
    (hits, misses) = cache.stats()
    last_call_time = cache.get("last_call_time")
    current_time = time.time()
    if last_call_time is None or current_time - last_call_time >= throttle_rate:
        # Call the throttled function
        throttled_function(1,2)
        # Get the number of cache hits
        if hits > 0:
            msg = f"[{counter}] cache hit | {hits} hits | {misses} misses"
            message.info(msg)
            print(msg)
        else:
            msg = f"[{counter}] memoized | {hits} hits | {misses} misses"
            message.success(msg)
            print(msg)
        # Update the last call time in the cache
        cache.set("last_call_time", current_time)
    else:
        msg = f"[{counter}] throttled | {hits} hits | {misses} misses"
        message.error(msg)
        sub_message.warning(f"Please wait at least **{throttle_rate} second(s)** before trying again!")
        print(msg)
        cache.stats(reset=True)

if st.button('⚡Call Function⚡'):
    message.empty()
    sub_message.empty()
    counter = cache.get("counter")
    # Call the throttle function multiple times
    throttle(counter)
    cache.set("counter", counter + 1)
