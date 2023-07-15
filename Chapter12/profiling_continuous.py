import io
import time
import cProfile
import logging
import pstats

# Configure logging to your cloud-based logging service
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cProfile")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# Create a file handler to log to a file
log_file = './logs/checkpoint_stats.log'
file_handler = logging.FileHandler(log_file, mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def slow_function(profiler, n_iterations=100_000_000, n_checkpoint=50_000_000):
    assert(n_checkpoint <= n_iterations)
    
    for i in range(n_iterations):
        # Perform your task here
        # ...
        # Call profile_and_log_stats every  iterations
        if (i+1) % n_checkpoint == 0:
            profile_and_log_stats(profiler)
    
    # Generate and log the final statistics
    profile_and_log_stats(profiler)

def fast_function(profiler, n_iterations=1_000_000, n_checkpoint=50_000):
    assert(n_checkpoint <= n_iterations)
    
    for i in range(n_iterations):
        # Perform your task here
        # ...
        # Call profile_and_log_stats every 50,000 iterations
        if (i+1) % n_checkpoint == 0:
            profile_and_log_stats(profiler)
    
    # Generate and log the final statistics
    profile_and_log_stats(profiler)

def profile_and_log_stats(profiler):
    profiler.disable()

    # Create a statistics object from the profiler
    stats_stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stats_stream)

    # Print the statistics by function name
    # (output will be redirected to the stream buffer)
    stats.strip_dirs().sort_stats('tottime').print_stats()

    # Split the stats string into lines and log each line
    for line in stats_stream.getvalue().split('\n'):
        logger.info(line.rstrip())

    profiler.enable()

if __name__ == "__main__":
    with cProfile.Profile(subcalls=False, builtins=False) as global_pr:
        global_pr.enable()

        with cProfile.Profile(subcalls=False, builtins=False) as local_pr:
            local_pr.enable()
            slow_function(local_pr, n_checkpoint=50_000_000)
            local_pr.disable()

        with cProfile.Profile(subcalls=False, builtins=False) as local_pr:
            local_pr.enable()
            fast_function(local_pr, n_checkpoint=500_000)
            local_pr.disable()

        profile_and_log_stats(global_pr)
        
        global_pr.disable()
