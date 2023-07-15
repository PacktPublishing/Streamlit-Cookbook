import cProfile
import pstats

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

    # Create a statistics object from the profiler
    stats = pstats.Stats(profiler)

    # Print the statistics by function name
    stats.strip_dirs().sort_stats('tottime').print_stats()

if __name__ == "__main__":
    main()
