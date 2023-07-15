import io
import cProfile
import logging
import pstats

# Configure logging to your cloud-based logging service
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cProfile")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

def slow_function():
    for _ in range(10000000):
        pass

def fast_function():
    for _ in range(100000):
        pass

def main():
    # Create a profile object
    profiler = cProfile.Profile()

    # Start profiling
    profiler.enable()

    # Run your code
    slow_function()
    fast_function()

    # Stop profiling
    profiler.disable()

    # Create a stream handler to log to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Create a file handler to log to a file
    log_file = './logs/stats.log'
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a statistics object from the profiler
    stats_stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stats_stream)

    # Print the statistics by function name
    # (output will be redirected to the stream buffer)
    stats.strip_dirs().sort_stats('tottime').print_stats()

    # Split the stats string into lines and log each line
    for line in stats_stream.getvalue().split('\n'):
        logger.info(line.rstrip())
        
if __name__ == "__main__":
    main()